README.txt




FreeLunch is an app to merge students and users who are looking to find free food on campus or have extra food to give away in order to help manage food waste. The app will consist of 5 html template files with static code designing like our medium-fi Figma prototype. In addition, it consists of a Flask server in a python app.py file. 


* MapView.html- An easily switchable screen for users to bounce between views. Using the MapBox API, the page shows the user's current location in comparison to a map view over Columbia University. The top toolbar allows users to click between pages and select dietary preferences. The pins on the map are color coded to easily identify the difference between active, upcoming, and archived events. 


* ListView.html- An easily switchable screen for user to bounce between view in a list format. Consists of a toolbar to separate Active, Upcoming, and Archived events into tabs. The screen will start on click with active events and allow users to click on individual ones to view them in more detail. This page will transfer any event that was marked as finished to the archived tab where users will no longer be able to click a detailed view on it and will see the event as grayed out.


* DetailedView.html- A more detailed page of individual events. Any notes that are added by the author will he posted here along with the option to save or end an event. If a users clicks the save icon it will turn yellow and allow the user to find that event later in their saved page. The end event is used for anyone to note rhe event is over or has no food left and will automatically move the event into the archived tab on the list view screen. The back button will resort to the MapView page.


* AddFood.html- A starter page for when users go to add an event to the app. This will allow users to click the camera to upload a photo and use the add button to post on the map and list pages. A drop down menu of campus locations has been implemented to choose from along with a time and date feature. The tags allow the authors to select multiple dietary selections to advertise to users. The back button will resort to the MapView page. Upon selecting add food, the user will be prompted with a terms and conditions statement to agree they are responsible for event cleanliness. 


* Saved.html- A personalized page for a user depending on which events they choose to save. The events on the page will be in the same format as the ListView html and will be clickable to direct the user to that detailed view of an event dynamically. If the user clicks the save icon again from the detailed page, it will resort from yellow to white and remove that event from the users individual saved list. 


* app.py- Our main file, we have implemented a Flask server to run and connect the links between our html files. This consists of multiple helpful functions to track time of posted events and shit events from active, upcoming, and archived lists.