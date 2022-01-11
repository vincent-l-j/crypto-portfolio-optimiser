"""
This renders the webpage which allows the user to build their own portfolio
"""
import streamlit as st
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
        on_click=update_weightings_msg,
        args=(st.session_state.weightings,)
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


if __name__ == '__main__':
    app()
