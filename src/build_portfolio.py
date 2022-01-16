"""
This renders the webpage which allows the user to build their own portfolio
"""
from functools import reduce
import streamlit as st
import pandas as pd
from binance import Client

client = Client()
fiat = 'USDT'

def app():
    st.title('Build your Portfolio')
    if 'weightings' not in st.session_state:
        # Set the default portfolio
        st.session_state.weightings = {
            'BTC': 60,
            'ETH': 20,
            'SOL': 20,
        }
    # Set the message informing the user of the chosen portfolio's weightings
    update_weightings_msg(st.session_state.weightings)

    if 'coin_list' not in st.session_state:
        st.session_state.coin_list = get_coin_list()
    coin_list = st.session_state.coin_list

    # If no assets are chosen, set chosen_assets to None
    chosen_assets = st.session_state.weightings.keys()
    if not chosen_assets:
        chosen_assets = None

    # Allow users to select multiple assets using the multiselect widget
    assets = st.multiselect(
        'What would you like in your portfolio?',
        coin_list,
        chosen_assets,
    )

    # Create sliders for portfolio asset weightings
    for x in assets:
        try:
            st.session_state.weightings[x] = st.slider(x, 0, 100, st.session_state.weightings[x])
        except KeyError:
            st.session_state.weightings[x] = st.slider(x, 0, 100, 0)

    # Delete assets that are no longer in the portfolio
    for x in set(coin_list) - set(assets):
        st.session_state.weightings.pop(x, None)

    # Create button that updates the weightings information message
    st.button(
        'Build Portfolio',
        on_click=cb_build_portfolio,
    )

    # Write the weightings information message
    st.write(st.session_state.weightings_info)


def update_weightings_msg(weightings):
    """
    Callback function to update the message informing the user of the chosen portfolio's weightings
    """
    st.session_state.weightings_info = f"Your portfolio's part-to-part ratio is: {weightings}"


def get_coin_list():
    exchange_info = client.get_exchange_info()
    # get coins paired with USDT
    symbols = (s for s in exchange_info['symbols'] if s['symbol'].endswith(fiat))
    # Ensure no duplicates by using sets
    coin_set = {s['baseAsset'] for s in symbols} | {s['quoteAsset'] for s in symbols}
    coin_set.discard(fiat)
    coin_list = sorted(coin_set)

    return coin_list


def cb_build_portfolio():
    """
    Download and cache the data needed for the portfolio
    """
    weightings = st.session_state.weightings
    update_weightings_msg(weightings)

    if not weightings: return

    asset_list = weightings.keys()
    if 'df_cached' not in st.session_state:
        df_cached = st.session_state.df_cached = reduce(
            lambda left, right: pd.merge(
                left,
                right,
                left_index=True,
                right_index=True,
                how='outer'),
            map(get_historical_data, list(asset_list) + ['BTC'])
        )
    else:
        df_cached = st.session_state.df_cached
        coins_cached = df_cached.columns.get_level_values(level=0).unique()
        coins_uncached = set(asset_list) - set(coins_cached)
        if coins_uncached:
            df_uncached = reduce(
                lambda left, right: pd.merge(
                    left,
                    right,
                    left_index=True,
                    right_index=True,
                    how='outer'),
                map(get_historical_data, tuple(coins_uncached))
            )
            df_cached = st.session_state.df_cached = pd.merge(
                df_cached,
                df_uncached,
                left_index=True,
                right_index=True,
                how='outer'
            )

    # Global dataframes
    df_ohlcv = df_cached[asset_list]
    st.session_state.df_ohlcv = df_ohlcv
    df_close = df_ohlcv[pd.MultiIndex.from_product([asset_list, ['close']])].droplevel(1, axis=1)
    st.session_state.df_close = df_close
    st.session_state.df_daily_returns = df_close.pct_change().dropna()


def get_historical_data(currency):
    klines = client.get_historical_klines(
        currency + fiat,
        Client.KLINE_INTERVAL_1DAY,
        "1 year ago UTC"
    )
    # klines columns=['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
    cols_ohlcv = ('open', 'high', 'low', 'close', 'volume')
    df = pd.DataFrame((x[:6] for x in klines), columns=['timestamp', *cols_ohlcv])
    df[[*cols_ohlcv]] = df[[*cols_ohlcv]].astype(float)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    df.columns = pd.MultiIndex.from_product([[currency], cols_ohlcv])

    return df


if __name__ == '__main__':
    app()
