import re
from shiny import render, reactive, Inputs, Outputs, Session, ui
from model.data_loader import get_bikes, get_subscription, get_usernames, insert_user, get_usernames_filtered


def server(input , output, session):
    # # Preload data to stop the reload of the webpage when changing tab
	# # https://shiny.posit.co/py/api/core/reactive.value.html
	# # used to find out how to set a reactive value
	# usernames = reactive.value(get_usernames())
	# bikes = reactive.value(get_bikes())
	# subscriptions = reactive.value(get_subscription())
	
    # Rendering DataFrames
	# https://shiny.posit.co/py/api/core/ui.output_data_frame.html#examples
	# used to find an example of how if was used/called
	@output 
	@render.data_frame
	def usernames_df():
		query = input.user_search_input().strip()
		if query:
			df = get_usernames_filtered(query)
		else:
			df = get_usernames()
		return render.DataGrid(df)
	@output
	@render.data_frame
	def bikes_df():
		return render.DataGrid(bikes.get())
	@output
	@render.data_frame
	def subs_df():
		return render.DataGrid(subscriptions.get())
	
	# Validity checks        
	# Used this link the make the checks: https://www.w3schools.com/python/python_regex.asp 
	def is_valid_name(name):
		return (re.fullmatch(r"[A-Åa-å]+(?: [A-Åa-å]+)*", name) is not None)
	
	def is_valid_phone(phone):
		return (re.fullmatch(r"\d{8}", phone) is not None)
	
	def is_valid_email(email):
		return "@" in email

	# Submit user form button handling
	@reactive.event(input.submit_user_form)
	def submit_user():
		name = input.full_name().strip()   # Getting rid of trailing white spaces
		phone = input.phone_nr().strip()
		email = input.email().strip()
		
        # Validity checks
		validity = []
		if not is_valid_name(name):
			validity.append(f"{name} - Not Valid")
		else:
			validity.append(f"{name} - Valid")

		if not is_valid_phone(phone):
			validity.append(f"{phone} - Not Valid")
		else:
			validity.append(f"{phone} - Valid")

		if not is_valid_email(email):
			validity.append(f"{email} - Not Valid")
		else:
			validity.append(f"{email} - Valid")


		if is_valid_name(name) and is_valid_phone(phone) and is_valid_email(email):
			insert_user(name, phone, email)

		return validity
	
	@output
	@render.text
	def user_info_ui():
		return ui.markdown("<br>".join(submit_user()))  # <br> break in HTML, because \n didn't work 
