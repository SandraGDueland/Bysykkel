from shiny import render, reactive, Inputs, Outputs, Session
from model.data_loader import get_bikes, get_subscription, get_usernames

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
    



 