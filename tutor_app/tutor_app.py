import reflex as rx

from backend.api import fastapi_app
from tutor_app.constants import APP_TITLE
from tutor_app.ui import index


app = rx.App(api_transformer=fastapi_app)
app.add_page(index, title=APP_TITLE)
