import reflex as rx

from tutor_app.constants import APP_TITLE
from tutor_app.ui import index


app = rx.App()
app.add_page(index, title=APP_TITLE)