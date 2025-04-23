import re
from shiny import render, reactive, Inputs, Outputs, Session, ui
from model.data_loader import get_bikes, get_subscription, get_usernames, insert_user


def server(input: Inputs, output: Outputs, session: Session):
    # Preload data to stop the reload of the webpage when changing tab
	# https://shiny.posit.co/py/api/core/reactive.value.html
	# used to find out how to set a reactive value
	usernames = reactive.value(get_usernames())
	bikes = reactive.value(get_bikes())
	subscriptions = reactive.value(get_subscription())
	
    # Rendering DataFrames
	# https://shiny.posit.co/py/api/core/ui.output_data_frame.html#examples
	# used to find an example of how if was used/called
	@output 
	@render.data_frame
	def usernames_df():
		return render.DataGrid(usernames.get())
	@output
	@render.data_frame
	def bikes_df():
		return render.DataGrid(bikes.get())
	@output
	@render.data_frame
	def subs_df():
		return render.DataGrid(subscriptions.get())
	
	def is_valid_name(name):
		return (re.fullmatch(r"[A-Åa-å]+(?: [A-Åa-å]+)*", name) is not None)
	
	def is_valid_phone(phone):
		return (re.fullmatch(r"\d{8}", phone) is not None)
	
	def is_valid_email(email):
		return "@" in email

	@reactive.event(input.submit_user_form)
	def submit_user_button_clicked():
		print("submit button clicked!")
		name = input.full_name().strip()
		phone = input.phone_nr().strip()
		email = input.email().strip()
		
        # Validity checks
		errors = []
		if not is_valid_name(name):
			errors.append(f"Name: {name} is Invalid")

		if not is_valid_phone(phone):
			errors.append(f"Phone: {phone} is Invalid")

		if not is_valid_email(email):
			errors.append(f"Email: {email} is Invalid")


		if errors:
			output.user_info_ui = render.ui(
				ui.markdown("\n".join(errors))
			)
			return		
			
		insert_user(name, phone, email)

		output.user_info_ui = render.ui(
			ui.markdown(f"Successfully added user to database")
		)