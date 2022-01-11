"""
Frameworks for running multiple Streamlit applications as a single app.
For more information, check out https://github.com/dataprofessor/multi-page-app
"""
import streamlit as st

class MultiApp:
    """Framework for combining multiple streamlit applications.
    Usage:
        def foo():
            st.title("Hello Foo")
        def bar():
            st.title("Hello Bar")
        app = MultiApp()
        app.add_app("Foo", foo)
        app.add_app("Bar", bar)
        app.run()
    It is also possible keep each application in a separate file.
        import foo
        import bar
        app = MultiApp()
        app.add_app("Foo", foo.app)
        app.add_app("Bar", bar.app)
        app.run()
    """
    def __init__(self):
        self.apps = dict()

    def add_app(self, title, func):
        """Adds a new application.
        Parameters
        ----------
        func:
            the python function to render this app.
        title:
            title of the app. Appears in the dropdown in the sidebar.
        """
        self.apps[title] = func

    def run(self):
        titles = self.apps.keys()
        if 'page' not in st.session_state:
            default_radio = 0
        else:
            default_radio = titles.index(st.session_state.page)
        st.sidebar.title("Navigation")
        title = st.sidebar.radio("Go To", titles, index=default_radio, key="radio")
        self.apps[title]()
