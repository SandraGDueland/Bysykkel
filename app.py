from shiny import App
from controller.server import server
from view.ui import app_ui


app = App(ui = app_ui, server = server)

# app.py

# from shiny import App, ui, render, reactive

# app_ui = ui.page_fluid(
#     ui.input_text("full_name", "Full name"),
#     ui.input_action_button("submit_user_form", "Submit"),
#     ui.output_ui("user_info_ui")
# )

# def server(input, output, session):
#     @reactive.event(input.submit_user_form)
#     def handle_submit():
#         name = input.full_name()
#         print("✅ Submit clicked with name:", name)
#         output.user_info_ui = render.ui(
#             ui.markdown(f"### Hello, {name}!")
#         )

# app = App(app_ui, server)