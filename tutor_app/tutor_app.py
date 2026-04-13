import reflex as rx

from tutor_app.constants import APP_TITLE
from tutor_app.ui import index

# ─── Google Fonts import for Atifex ─────────────────────────────────
ATIFEX_FONT_IMPORT = (
    "https://fonts.googleapis.com/css2?family=Atifex:wght@300;400;500;600;700&display=swap"
)

app = rx.App(
    style={
        "font_family": "Atifex, sans-serif",
        "color_scheme": "dark",
    },
    stylesheets=[ATIFEX_FONT_IMPORT],
)
app.add_page(index, title=APP_TITLE)