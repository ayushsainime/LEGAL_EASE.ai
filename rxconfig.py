import reflex as rx


config = rx.Config(
    app_name="tutor_app",
    disable_plugins=["reflex.plugins.sitemap.SitemapPlugin"],
    backend_port=7860,
    frontend_port=7860,
)
