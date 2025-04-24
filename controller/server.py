import re
from shiny import render, reactive, ui
from model.data_loader import get_bikes, get_subscription, get_usernames, insert_user, get_usernames_filtered, get_trips_endstation, get_station_bikes


def server(input , output, session):
    # Preload data to stop the reload of the webpage when changing tab
	# https://shiny.posit.co/py/api/core/reactive.value.html
	# used to find out how to set a reactive value
	usernames = reactive.value(get_usernames())
	bikes = reactive.value(get_bikes())
	subscriptions = reactive.value(get_subscription())
	trips_end = reactive.value(get_trips_endstation())
	station_bikes = reactive.value()
	
    
    # Rendering DataFrames
	# https://shiny.posit.co/py/api/core/ui.output_data_frame.html#examples
	# used to find an example of how it was used/called
	@output 
	@render.data_frame
	@reactive.event(input.user_search_button, ignore_none=False)     # Ignore_none to collect the df initially, and then update on botton click
	def usernames_df():
		query = input.user_search_input().strip()
		if query:
			df = get_usernames_filtered(query)
		else:
			df = usernames.get()
		return render.DataGrid(df)
	
	@output
	@render.data_frame
	def trips_end_df():
		return render.DataGrid(trips_end.get())

	@output
	@render.data_frame
	@reactive.event(input.station_search)
	def station_bikes_df():
		query = input.station_search().strip()
		df = get_station_bikes(query)
		return df

	@output
	@render.data_frame
	def bikes_df():
		return render.DataGrid(bikes.get())

	@output
	@render.data_frame
	def subs_df():
		return render.DataGrid(subscriptions.get())
	
 
 
	# Validity check rules        
	# Used this link the make the checks: https://www.w3schools.com/python/python_regex.asp 
	def is_valid_name(name):
		return (re.fullmatch(r"[A-Åa-å]+(?: [A-Åa-å]+)*", name) is not None)
	
	def is_valid_phone(phone):
		return (re.fullmatch(r"\d{8}", phone) is not None)
	
	def is_valid_email(email):
		return "@" in email

	# Submit-user-form button handling
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
			insert_user(name, phone, email)                      # Inserts user into db if all checks are valid
			validity.append("User was added to the database.")
		else: validity.append("User was not added to the database.")

		return validity
	
	@output
	@render.text
	def user_info_ui():          # Shows only after Submit button is clicked
		return ui.markdown("<br>".join(submit_user()))  # <br> break in HTML, because '\n' and '\r' didn't work 
