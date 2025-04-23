from shiny import App
from controller.server import server
from view.ui import app_ui


app = App(ui = app_ui, server = server)