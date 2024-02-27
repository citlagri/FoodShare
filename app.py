from flask import Flask, render_template, request, redirect, url_for, json, jsonify
from datetime import datetime, timedelta


app = Flask(__name__)

event_counter = 1
active_items = []
upcoming_items = []
archived_items = []

# Function to switch active event to archived 
@app.route('/mark_finished/<item_id>')
def mark_finished(item_id):
    global active_items, upcoming_items, archived_items

    # Find the event in active_items
    event = get_event_by_id(int(item_id), active_items, upcoming_items)

    if event:
        # Move the event to archived_items
        archived_items.append(event)
        active_items = [e for e in active_items if e['itemId'] != event['itemId']]
        upcoming_items = [e for e in upcoming_items if e['itemId'] != event['itemId']]

        # Redirect to the ListView or MapView depending on the request referrer
        if request.referrer and 'mapView' in request.referrer:
            return redirect(url_for('mapView'))
        else:
            return redirect(url_for('listView'))

    return "Event not found"

# Function to dynamically post event on detailed view
# Events organized by id number: 1,2,3,....etc
def get_event_by_id(item_id, active_items, upcoming_items):
    for event in active_items + upcoming_items:
        if event.get('itemId') == item_id:
            # Handle uploaded image
            if 'itemImage' in request.files:
                item_image = save_uploaded_image(request.files['itemImage'])
            else:
                item_image = '/static/images/camera.png'  # Use a default image path

            return event
    return None  # Event not found

app.static_url_path = '/static'
app.static_folder = 'static'


# Map view function
@app.route('/')
def mapView():
    return render_template('MapView.html')

# Function to get coordinates based on location name
def get_coordinates_by_location(location_name):
    # Hardcoded coordinates based on location name
    location_coordinates = {
        'Alfred J. Lerner Hall': [-73.96399894507822, 40.80704042941291],
        'Avery Hall': [-73.96101370460352, 40.808400722415],
        'Buell Hall': [-73.96146028925891, 40.807871264977365],
        'Butler Library': [-73.96325557576746, 40.80651686812654],
        'Dodge Hall': [-73.96333837762043, 40.80826891580302],
        'Dodge Physical Fitness Center': [-73.96181446042277, 40.80958481995126],
        'Earl Hall': [-73.96289342180118, 40.80877554536566],
        'East Campus': [-73.95900220275047, 40.807364049338766],
        'Engineering Terrace': [-73.95996092973355, 40.80954798160509],
        'Faculty House': [-73.95917021438913, 40.806896529800206],
        'Fairchild Center': [-73.96015957020816, 40.809325699939535],
        'Fayerweather Hall': [-73.96036916042274, 40.80833009854027],
        'Hamilton Hall': [-73.96173127576745, 40.80695302542684],
        'Havemeyer Hall': [-73.96220431624204, 40.809458602362604],
        'International Affairs Building': [-73.95986841809506, 40.808031047461235],
        'Jerome Greene Hall': [-73.96044377391435, 40.807018771150716],
        'Kent Hall': [-73.96142716042286, 40.807369566143805],
        'Knox Hall': [-73.96177757391416, 40.812072955206936],
        'Lewisohn Hall': [-73.96324344693126, 40.8085512840448],
        'Low Library': [-73.96176650089744, 40.80834304658288],
        'Mathematics': [-73.96267680275045, 40.80929262334914],
        'Mudd Building': [-73.95994624693122, 40.80955606369817],
        'North West Corner Building': [-73.96205586227572, 40.81011367794296],
        'Philosophy Hall': [-73.96091524507821, 40.807676089980774],
        'Pulitzer Hall': [-73.96373909111205, 40.80785815164517],
        'Pupin Hall': [-73.96134155856969, 40.81013231881216],
        'Schapiro': [-73.96078944507816, 40.80987140623742],
        'Schermerhorn Hall': [-73.96018209348517, 40.808579426903066],
    }
    return location_coordinates.get(location_name, None)

# Function to get the status of an event (upcoming, active, or archived)
def get_event_status(event):
    current_date = datetime.now().date()
    event_date = datetime.strptime(event['itemDate'], '%Y-%m-%d').date()

    if event_date < current_date:
        return 'archived'
    elif event_date == current_date:
        return 'active'
    else:
        return 'upcoming'
    
# Fetch locations data from Flask backend
@app.route('/get_locations')
def get_locations():
    global active_items, upcoming_items, archived_items

    # Combine active, upcoming, and archived items into a single list
    all_items = active_items + upcoming_items + archived_items

    # Create a list of dictionaries containing 'name', 'coordinates', and 'status'
    locations = [
        {
            'name': item['itemName'],
            'coordinates': get_coordinates_by_location(item['itemLocation']),
            'status': get_event_status(item),
            'itemTags': item['itemTags']
        }
        for item in all_items
    ]

    print("Locations:", locations)
    return jsonify(locations)


# List view function, dynamically posts events
@app.route('/listView', methods=['GET', 'POST'])
def listView():
    global active_items, upcoming_items, archived_items
    global event_counter 
    if request.method == 'POST':
        # Retrieve form data from AddFood.html
        item_name = request.form.get('itemName')
        item_location = request.form.get('itemLocation')
        item_date_str = request.form.get('itemDate')
        item_time = request.form.get('itemTime')     
        item_author = request.form.get('itemAuthor')  
        item_tags = request.form.getlist('itemTags[]')
        item_notes = request.form.get('itemNotes')

        # Convert the date string to a datetime object
        item_date = datetime.strptime(item_date_str, '%Y-%m-%d').date()
        item_datetime = datetime.combine(item_date, datetime.strptime(item_time, '%H:%M').time())
        time_difference = datetime.now() - item_datetime
        item_time = datetime.strptime(item_time, '%H:%M').strftime('%-I:%M %p')
        # Save the uploaded image 
        item_image = save_uploaded_image(request.files['itemImage'])
        item_time = time_determine(time_difference, item_time)

        new_item = {
        'itemId': event_counter,
        'itemName': item_name,
        'itemLocation': item_location,
        'itemDate': item_date_str,
        'itemImage': item_image,
        'itemTime': item_time,
        'itemAuthor': item_author,
        'itemTags': item_tags,
        'itemNotes': item_notes
        }
        event_counter += 1

        today = datetime.now().date()
        if item_date == today:
            active_items.append(new_item)
        elif item_date > today:
            upcoming_items.append(new_item)
        
    # Render ListView.html with existing data (for GET requests)
    return render_template('ListView.html', active_items=active_items, upcoming_items=upcoming_items, archived_items=archived_items)


# Function to create time difference for time stamp
def time_determine(time_difference, item_time):
    if time_difference.total_seconds() >= 0:
        minutes_ago = int(time_difference.total_seconds() / 60)
        item_time = f"{minutes_ago} minutes ago"
        return item_time
    elif time_difference.total_seconds() < 0:
        return item_time
    

# Function to save uploaded image
def save_uploaded_image(file):
    # Handle the logic to save the uploaded image to a location
    save_path = 'static/uploads/'
    file_path = save_path + file.filename
    file.save(file_path)
    return '/' + file_path  # Return the relative path to be used in the HTML


# Detailed view function to get events dynamically
@app.route('/detailedView/<item_id>')
def detailedView(item_id):
    event = get_event_by_id(int(item_id), active_items, upcoming_items)
    if event:
        return render_template('DetailedView.html', event=event)
    else:
        return("Not found")
    

# Add view function    
@app.route('/addFood')
def addFood():
    return render_template('AddFood.html')


# Saved for later view function uses cookie function to remember user saved items
@app.route('/saved')
def saved():
    saved_items_json = request.cookies.get('saved_items')
    saved_items = json.loads(saved_items_json) if saved_items_json else []
    saved_events = [event for event in active_items + upcoming_items if str(event['itemId']) in saved_items]

    return render_template('SavedForLater.html', saved_events=saved_events, saved_items=saved_items)



if __name__ == '__main__':
    app.run(debug=True)