from shiny import ui

app_ui = ui.page_fluid(
    	ui.head_content(        # https://shiny.posit.co/py/api/express/express.ui.include_css.html#note
							    # CSS styling to make the tables look nicer, and adding some color ;)
		ui.tags.style("""
		.shiny-data-grid {
			width: 100% !important;   /* Adjusting width of the table to take up the entire width of the card*/
			max_width: 1400px;
			margin: auto;
			height: auto !important;   /* Adjusting height to make all usernames visible, avoid scrolling inside component*/
			max-height: none !important;
			overflow: visible !important;
		}
		.nav-tabs .nav-link {           /* web inspector used to find name of the ui.element and the active html class*/
			color: green !important;
		}
		.nav-tabs .active {
			color: black !important;

		}#switch_value{
			max-width: fit-content;
		}.row{
			justify-content: space-around;
			align-items: top;

		}.form-switch{
			justify-content: center;
			align-items: center;
		}
  
		""")
	),
	ui.h1('Bysykkel', style = 'color: green;'),
	ui.page_fillable(                       # https://shiny.posit.co/py/layouts/tabs/#card-with-a-tabbed-tabset
		ui.navset_card_tab(                 # Used this link to find the tab component
			ui.nav_panel("Users", 
				ui.h2('Usernames', style='color: green;'),
                ui.row(
                	ui.input_text("user_search_input", label=None, placeholder="Search by name..", width="67%"),
                	ui.input_action_button("user_search_button", "Search", style="color: green; max-height: 4.5dvh; justify-content: center; align-items: center; display: flex;", width='30%'),
				),
				ui.output_data_frame("usernames_df"),
			),
			ui.nav_panel("Trips Ended", 
				ui.h2('Number of trips ending at each station', style='color: green;'),
				ui.output_data_frame('trips_end_df')
			),
			ui.nav_panel("Available Bikes",
				ui.h2('Available bikes at each staiton', style='color: green;'),
				ui.input_text("station_search", "Search by station or bike:", placeholder="Search by station or bike...", value=""),
				ui.output_data_frame("station_bikes_df")
			),
			ui.nav_panel("Bike Status", 
				ui.h2('Bike names and status', style='color: green;'),
				ui.output_data_frame('bikes_df')
			),
			ui.nav_panel("Subscriptions", 
				ui.h2('Purchasing statistics for subscriptions', style='color: green;'),
				ui.output_data_frame('subs_df')
			),
            ui.nav_panel("Add User",
                ui.h2('Add new user', style= 'color: green;'),
					ui.layout_columns(                             # https://shiny.posit.co/py/layouts/panels-cards/#content-divided-by-cards
						ui.card(                                   # used for layout example
							ui.input_text("full_name", "Full name ", placeholder="Enter name..."),
							ui.input_text("phone_nr", "Phone number", placeholder="Enter phone number..."),
							ui.input_text("email", "Email", placeholder="Enter email..."),
							ui.input_action_button("submit_user_form", "Submit", style="color: green;", width='30%'),
							ui.output_ui("user_info_ui"),           # Placeholder until 'submit_user_form' action button is clicked.
						)	
    				),
                         
			),
            ui.nav_panel("Interactions",
				ui.h2('Interactions', style='color: green;'),
                ui.layout_columns(
					ui.card(
						ui.card_header('CHECKOUT', style="color: green;"),
							ui.output_ui("select_user_ui_check"),
							ui.output_ui("select_station_ui_check"),
							ui.input_action_button("checkout_button", "Checkout", width='40%', style="color: green;"),
						ui.output_ui("checkout_selected")       #Placeholder until 'checkout_button' has been clicked.
					),
    				ui.card(
						ui.card_header('DROPOFF', style="color: green;"),
							ui.output_ui("select_user_ui_drop"),
							ui.output_ui("select_station_ui_drop"),
							ui.input_action_button("dropoff_button", "Dropoff", width='40%', style="color: green;"),
						ui.output_ui("dropoff_selected")       #Placeholder until 'droppff_button' has been clicked.
					),
				),
			), 
            ui.nav_panel("Active Trip",
				ui.h2('Active trip', style='color: green;'),
				ui.row(
                ui.output_ui("trip_select_ui"),
                ui.row(
                	ui.input_switch("in_progress", "Trip in progress", False),
            		ui.output_text("switch_value"),
					)
    			),
				ui.output_ui("trip_df_ui")
			),   
        )
    )
)