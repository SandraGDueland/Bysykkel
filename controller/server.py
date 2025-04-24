import re
from shiny import render, reactive, ui
from model.data_loader import get_bikes, get_subscription, get_usernames, insert_user, get_usernames_filtered 
from model.data_loader import get_trips_endstation, get_station_bikes, get_stations, get_users, find_available_bikeID
from model.data_loader import insert_checkout, get_stationID, get_userID, get_bike_name, find_active_bike, insert_dropoff, get_bike_status


def server(input , output, session):
    # Preload data to stop the reload of the webpage when changing tab
	# https://shiny.posit.co/py/api/core/reactive.value.html
	# used to find out how to set a reactive value
	usernames = reactive.value(get_usernames())
	bikes = reactive.value(get_bikes())
	subscriptions = reactive.value(get_subscription())
	trips_end = reactive.value(get_trips_endstation())
	
			
    # Rendering DataFrames
	# https://shiny.posit.co/py/api/core/ui.output_data_frame.html#examples
	# used to find an example of how it was used/called
	@output 
	@render.data_frame
	@reactive.event(input.user_search_button, ignore_none=False)    	# Ignore_none to collect the df initially, and then update on botton click
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

	def is_valid_userID(userID):
		return userID is not None

	def is_valid_stationID(stationID):
		return stationID is not None

	def is_valid_bikeID(bikeID):
		return bikeID is not None

	def is_active_bike(bikeID):
		return get_bike_status(bikeID) == 'Active'

	def is_valid_checkout(userID, stationID, bikeID):
		return userID is not None and stationID is not None and bikeID is not None

	def is_valid_dropoff(userID, stationID, bikeID):
		validity = False
		if is_valid_bikeID(bikeID) and is_valid_userID(userID) and is_valid_stationID(stationID):
			if is_active_bike(bikeID):
				validity = True
       
		return validity
     
	# -----------------------Button handling-------------------------------
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
	
	# Checkout button handling
	@reactive.event(input.checkout_button)
	def checkout_bike():
		userID = get_userID(input.select_user_check())
		stationID = get_stationID(input.select_station_check())
		bikeID = find_available_bikeID(stationID)
  
		# Validity check
		if is_valid_checkout(userID, stationID, bikeID):
			insert_checkout(userID, stationID, bikeID)
			message = f"{input.select_user_check()} checked out {get_bike_name(bikeID)} at {input.select_station_check()}"
		else:
			if not is_valid_bikeID(bikeID):   
				message = f"There were no available bikes at this station."   # This is useful, the ones under are redundant at this point
			elif not is_valid_stationID(stationID):
				message = f"No station was selected."
			elif not is_valid_userID(userID):
				message = f"No user was selected."
			else:
				message = f"Something went wrong."
		return message
 
	# Dropoff button handling
	@reactive.event(input.dropoff_button)
	def dropoff_bike():
		userID = get_userID(input.select_user_drop())
		stationID = get_stationID(input.select_station_drop())
		bikeID = find_active_bike(userID)
  
		# Validity check
		if is_valid_dropoff(userID, stationID, bikeID):
			insert_dropoff(userID, stationID, bikeID)
			message = f"{input.select_user_drop()}  dropped off {get_bike_name(bikeID)} at {input.select_station_drop()}"
		else:
			if not is_valid_bikeID(bikeID):   
				message = f"There was no trip found for this user."   # This is useful, the ones under are redundant at this point
			else:
				message = f"Something went wrong."
		return message
 
	# Select choices
	# https://shiny.posit.co/py/api/core/ui.update_select.html
	@reactive.Calc
	def user_choices():
		names = get_users()
		return names      
  
	@reactive.Calc
	def station_choices():
		names = get_stations()
		return names
 
	# Select fields, must render in after choices have been collected to be able to have a preselected choice from the list
	@output
	@render.ui
	def select_user_ui_check():
		userchoices = user_choices()
		return ui.input_select("select_user_check", "Select a user below:", choices=userchoices, selected=userchoices[0], multiple=False)   # https://shiny.posit.co/py/components/inputs/select-single/

	@output
	@render.ui
	def select_station_ui_check(): 
		stationchoices = station_choices()
		return ui.input_select("select_station_check", "Select a station below:", choices=stationchoices, selected=stationchoices[0], multiple=False),
  	
	@output
	@render.ui
	def select_user_ui_drop():
		userchoices = user_choices()
		return ui.input_select("select_user_drop", "Select a user below:", choices=userchoices, selected=userchoices[0], multiple=False)   # https://shiny.posit.co/py/components/inputs/select-single/

	@output
	@render.ui
	def select_station_ui_drop(): 
		stationchoices = station_choices()
		return ui.input_select("select_station_drop", "Select a station below:", choices=stationchoices, selected=stationchoices[0], multiple=False),
  
  
	# Hidden text until action buttons are pressed	
	@output
	@render.text
	def user_info_ui():          # Shows only after Submit button is clicked
		return ui.markdown("<br>".join(submit_user()))  # <br> break in HTML, because '\n' and '\r' didn't work 

	@output
	@render.text
	def checkout_selected():
		return ui.markdown(checkout_bike())

	@output
	@render.text
	def dropoff_selected():
		return ui.markdown(dropoff_bike())
