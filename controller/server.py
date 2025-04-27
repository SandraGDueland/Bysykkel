import re
from shiny import render, reactive, ui
from model.data_loader import get_bikes, get_subscription, get_usernames, insert_user, get_usernames_filtered, get_username, get_station
from model.data_loader import get_trips_endstation, get_station_bikes, get_stations, get_users, find_available_bikeID, get_availability
from model.data_loader import insert_checkout, get_stationID, get_userID, get_bike_name, find_active_bike, insert_dropoff, get_bike_status
from model.data_loader import get_repair_choices, send_repair_request, get_parking_availability, get_bike_availability, get_position


def server(input , output, session):
    # Preload data to stop the reload of the webpage when changing tab
	# https://shiny.posit.co/py/api/core/reactive.value.html
	# used to find out how to set a reactive value
	usernames = reactive.value(get_usernames())
	bikes = reactive.value(get_bikes())
	subscriptions = reactive.value(get_subscription())
	trips_end = reactive.value(get_trips_endstation())
	search_query_usernames = reactive.value("")
	station_bikes = reactive.value(get_station_bikes(""))
	repairchoices = reactive.value(get_repair_choices())
	repair_bikeID = reactive.value(-1)
	availability = reactive.value("")
	selected_station = reactive.value("")
			
    # Rendering DataFrames
	# https://shiny.posit.co/py/api/core/ui.output_data_frame.html#examples
	# used to find an example of how it was used/called
	@output
	@render.data_frame
	def usernames_df():
		query = search_query_usernames.get() # Collect the search value from the reactive.value that is changed when the search button is clicked
		if query:                            # This prevents the usernames table from changing as one writes the search value, and only updates when the button is pressed
			df = get_usernames_filtered(query)
		else:
			df = usernames.get()
		return render.DataGrid(df)

	@reactive.effect
	@reactive.event(input.user_search_button)      # Called only when the usernames searach button is pressed
	def usernames_search_handling():  			   # sets the reactive.value search_query_usernames force an update in the 
		search_query_usernames.set(input.user_search_input().strip())  # usernames ui to reflect the filtered list from the search
	
	@output
	@render.data_frame
	def trips_end_df():
		return render.DataGrid(trips_end.get())

	@output
	@render.data_frame
	def station_bikes_df():
		query = input.station_search().strip()
		station_bikes.set(get_station_bikes(query))
		df = station_bikes.get()
		return df

	@output
	@render.data_frame
	def bikes_df():
		return render.DataGrid(bikes.get())

	@output
	@render.data_frame
	def subs_df():
		return render.DataGrid(subscriptions.get())
	
	@output
	@render.data_frame
	def trip_df():
		selected_station.set(input.select_station_trip())
		station = selected_station.get()
		in_progress = input.in_progress()
		if station is None:
			return
		else:
			if in_progress:
				availability.set(get_parking_availability(station))
				df = availability.get()
			else:
				availability.set(get_bike_availability(station))
				df = availability.get()
		position = get_position(station)
		lat = position[0]
		long = position[1]
		link = [ui.HTML(f'<a href="https://www.openstreetmap.org/#map=17/{lat}/{long}">Map link</a>')]   # https://stackoverflow.com/questions/78835912/how-to-add-a-hyperlink-to-a-rendered-dataframe-in-shiny-for-python
		df["Map"]= link
		df["Availability"] = (df["Availability"]).astype(int).astype(str) + '%'
		return df
 
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

	def is_available_station(stationID):
		return get_availability(stationID) > 0

	def is_valid_bikeID(bikeID):
		return bikeID is not None

	def is_active_bike(bikeID):
		return get_bike_status(bikeID) == 'Active'

	def is_valid_checkout(userID, stationID, bikeID):
		return userID is not None and stationID is not None and bikeID is not None

	def is_valid_dropoff(userID, stationID, bikeID):
		validity = False
		if is_valid_bikeID(bikeID) and is_valid_userID(userID) and is_valid_stationID(stationID):
			if is_active_bike(bikeID) and is_available_station(stationID):
				validity = True
		return validity
     
	# -----------------------Button handling-------------------------------
	# Submit-user-form button handling
	@reactive.event(input.submit_user_form)
	def submit_user():
		# sets the reactive.values to the text field input
		name = input.full_name().strip()        # Getting rid of trailing white spaces with strip
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
			insert_user(name, phone, email)         # Inserts user into db if all checks are valid
			
			# Resets the reactive.value search_query_usernames to force an utdate in the
			# usernames table ui when a new user is added to the database
			query = search_query_usernames.get()
			search_query_usernames.set("")
			search_query_usernames.set(query)
			usernames.set(get_usernames())
			ui.update_text("full_name", value="")
			ui.update_text("phone_nr", value="")
			ui.update_text("email", value="")

			validity.append("User was added to the database.")
		else: validity.append("User was not added to the database.")

		return validity   # returns a list of which validity checks failed and which passed

	# Checkout button handling
	@reactive.event(input.checkout_button)
	def checkout_bike():
		userID = get_userID(input.select_user_check())
		stationID = get_stationID(input.select_station_check())
		bikeID = find_available_bikeID(stationID)
  
		# Validity check
		if is_valid_checkout(userID, stationID, bikeID):
			insert_checkout(userID, stationID, bikeID)
			station_bikes.set(get_station_bikes(input.station_search().strip()))    # Force a new call to db to update station_bikes ui
			bikes.set(get_bikes())
			station = selected_station.get()
			if station is not None:
				if input.in_progress():
					availability.set(get_parking_availability(station))
				else:
					availability.set(get_bike_availability(station))
			message = f"{get_username(userID)} checked out {get_bike_name(bikeID)} at {get_station(stationID)}"

		else:
			if not is_valid_bikeID(bikeID):   
				message = f"There were no available bikes at this station."   # This is useful 
			elif not is_valid_stationID(stationID):                           # These are redundant at this point because there is a default value selected
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
		# Validity check dropoff
		if is_valid_dropoff(userID, stationID, bikeID):
			insert_dropoff(userID, stationID, bikeID)    # Adds dropoff to db if valid
			message = f"{get_username(userID)}  dropped off {get_bike_name(bikeID)} at {get_station(stationID)}"
			rchoices = repairchoices.get()
			repair_bikeID.set(bikeID)
			modal = ui.modal(                             # https://shiny.posit.co/py/api/core/ui.modal.html used as example
            "Send in a repair request.",
			ui.input_selectize("select_repairs", "Please select one of the options below:", choices=rchoices, multiple=True),
            title="Was there anything wrong with the bike?",
            easy_close=False,
            footer=ui.row(
                ui.markdown("If you close the modal without selecting an option, the option of no problems will be selected for you."),
                ui.input_action_button("modal_close", "Close")),
            )
			ui.modal_show(modal)
		else:
			if not is_valid_bikeID(bikeID):   
				message = f"There was no trip found for this user."
			elif not is_available_station(stationID):
				message = f"This station is full, select another station."
			else:
				message = f"Something went wrong."
		return message
 
	@reactive.effect
	@reactive.event(input.modal_close)
	def handle_modal_close():
		selected_repair_codes = input.select_repairs()
		ui.modal_remove()
		if not selected_repair_codes:
			pass
		else:
			for item in selected_repair_codes:
				send_repair_request(item, repair_bikeID.get())
		# Resets / recalls the reactive.values that have been affected
		repair_bikeID.set(-1)
		trips_end.set(get_trips_endstation())                                  # Force a reload of the trips table in ui
		station_bikes.set(get_station_bikes(input.station_search().strip()))   # Force a new call to db to update station_bikes ui
		bikes.set(get_bikes())												   # Force a reload of bikes and status table
		station = selected_station.get()
		if input.in_progress():
			availability.set(get_parking_availability(station))
		else:
			availability.set(get_bike_availability(station))
  
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
  
  
	@output	
	@render.ui
	def trip_select_ui():
		stations = station_choices()
		return ui.input_selectize("select_station_trip", "Select a station below:", choices=stations, selected=stations[0], multiple=False),
 
	# Hidden text until action buttons are pressed	
	@output
	@render.text
	def user_info_ui():                                 # Shows only after Submit button is clicked
		return ui.markdown("<br>".join(submit_user()))  # <br> break in HTML, because '\n' and '\r' didn't work 

	@output
	@render.text
	def checkout_selected():
		return ui.markdown(checkout_bike())

	@output
	@render.text
	def dropoff_selected():
		return ui.markdown(dropoff_bike())

	@output
	@render.ui
	def trip_df_ui():
		return ui.output_data_frame("trip_df")

	@output	
	@render.text	
	def switch_value():
		val = input.in_progress()
		if val:
			return "Active trip: Availability shows percentage of available parking spots."
		else:
			return "Inactive trip: Availability shows percentage of available bikes."
			
