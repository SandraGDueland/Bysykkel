# Bysykkel

# How to run: 
In terminal inside the repo folder:
    
    python3 -m shiny run app.py

Dependencise:
- shiny
- pandas

# Overview of web-application:
The web app is a single page application. The page consists of a card with different tabs that correspond to the different exercises. 
# Tabs:
- Users:
    Users is filled with a table of users that display userId, usernames and phone numbers, ordered by usernames in alphabetical order. There is also a search field that will filter the table according to the search term, only searching by name. The search only filters the table when the search button is pressed.
- Trips Ended:
    This tab is filled with a table of stations with a counter of how many trips have ended at each station.
- Available Bikes:
    Available Bikes shows a table of the bikes that are parked and are therefore available to checkout and which stations they are parked at. One can search by station name or bike name to filter the table. 
- Bike Status:
    This tab contains a table of all bikes accompanied by their status. This can be: "Active, Parked, Missing or Inactive" so far. 'Inactive' is the status I have chosen to set when a bike is marked for repairs.
- Subscriptions:
    The subscription tab simply contains a table of subscription types and the amount of times they have been purchased. This table has no chnages from the first iteration of this project. 
- Add User:
    The Add User tab contains a card with a form to add a new user. To add a new user one must input a valid name, phone number and email after the specifications in the exercise. When the Submit button is pressed, the input is checked and added to the database if the input is valid. Whether or not the input is valid will be displayed under the form in a list together with a success or failure message.
- Interactions:
    This tab holds two cards with different interactions from task 3 in the exercise. Both card dispaly two selecters with username and station names and their individual buttons. 
        The checkout card will check out a parked bike from the selected station if a bike is available there and set it to active. This will also start a trip with the selected user and chosen bike. 
        The dropoff card will drop off and park a bike at the selected station if the selected user is tied to an active trip. This will also end the trip and update the trip information in the database. 
        After the dropoff a modal will pop up that asks the user if there was anything wrong with the bike and suggest a list of repair codes. If the user choses a code, a repair request will be sent to the database and the status of the bike in question will be set to 'Inactive', meaning that the bike will no longer be available to ride until it is repaired. I considered letting the bikes that need repairs continue to stay in circulation, but figured that some faults are dangerous and the bikes should therefore be repaired before they can be used again. 
- Active Trip:
    Within this tab there is a selecter and a switch with some associated output. The switch represent a trip being in progress or not. A station is selected and depending on the switch being turned on or off the information text and the table will change. If the switch is turned off, the table will display the availability of bikes as a percentage of the maximum number of parking spots at that station. However, if the switch is turned on, the table will display the availability of parking spots as a percentage of the maximum number of parking spots at that station. In the last column in the table, a link to a map is displayed and can be pressed to open the map at the coordinated of the station selected. 

# General: 
 As of now there is no ui that can set the bike status back to 'Parked'/'Active' after it has been set to 'Inactive'. This would probably be the next interaction I would implement, however it should only be available for administrators or employees depending on what roles will be implemented. 
 The application is heavily reliant on frequent queries to the database, but for a small db and application like this, that is not a problem. 