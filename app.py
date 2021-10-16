import logging
import webview
from contextlib import redirect_stdout
from io import StringIO
from server import server
logger = logging.getLogger(__name__)
if __name__ == '__main__':
    stream = StringIO()
    with redirect_stdout(stream):
        window = webview.create_window("App", server, width=1200, height=900, resizable=False)
        webview.start(debug=True)