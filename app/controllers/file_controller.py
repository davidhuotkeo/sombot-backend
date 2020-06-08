import pandas as pd
from app.models import (
    db,
    File,
    Audience,
    Event
)
from app import app
import os

def csv_control(csv_data: str, add_to_database=True, event_id=""):
    """
    Getting file data in csv file and split out each rows and also put into database

    Args:
    - CSV_DATA [string]: filename of the opened file (request file object)
    - ADD_TO_DATABASE [bool]: Add all audiences to database
    - EVENT_ID [string]: an event id
    """

    # Read file and map array to lowercase
    data = pd.read_csv(csv_data)
    data.columns = list(map(str.lower, data.columns))

    # select only 3 columns [name email phonenumber] and turn into array 
    selected_data = data[["name", "email", "phonenumber"]]
    rows = selected_data.values

    # if add to database
    # query the eventid
    # loop every array and add to audience table in db
    if add_to_database:
        event = Event.query.filter(Event.id == event_id).first()

        if not event:
            return None

        for row in rows:
            print(row)
            db.session.add(Audience(event, row))
        file = File(event)
        file_name = file.id + ".csv"
        file_full_path = os.path.join(app.config.get("CSV_FOLDER"), file_name)
        data.to_csv(file_full_path)
        db.session.commit()
        print(file_full_path)
    return rows
