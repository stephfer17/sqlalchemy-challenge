# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)


# Save references to each table
Station = Base.classes.station
Measurement  = Base.classes.measurement 

# Create our session (link) from Python to the DB
session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/end<br/>"

    )
@app.route("/api/v1.0/precipitation")
def preciptation():

    """Return a list of precipitation data including the date, prcp of each station"""
    # Query all precipitation
    last_year_rain= dt.date(2017,8,23)-dt.timedelta(days=365)
    last_year_rain
    results_precp = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= last_year_rain).all()


    # Create a dictionary from the row data and append to a list of all_precp
    all_precp = []
    for date, prcp in results_precp:
        precp_dict = {}
        precp_dict["date"] = date
        precp_dict["prcp"] = prcp
        all_precp.append(precp_dict)

    return jsonify(all_precp)

@app.route("/api/v1.0/stations")
def stations():

    """Return a list of all station names"""
    # Query all passengers
    results_station = session.query(Measurement.station).all()

    # Convert list of tuples into normal list
    all_names_station = list(np.ravel(results_station))

    return jsonify(all_names_station)


@app.route("/api/v1.0/tobs")
def tobs():
 #fitler for last year 
 last_year_rain= dt.date(2017,8,23)-dt.timedelta(days=365)
 last_year_rain
 recent_station=session.query(Measurement.date, Measurement.tobs).\
filter(Measurement.station == 'USC00519281').\
filter(Measurement.date >= last_year_rain).all()
 # Convert list of tuples into normal list
 recent_stations=list(np.ravel(recent_station))
 return jsonify(recent_stations)
 
 
 
 # for debugging   
if __name__ == '__main__':
    app.run(debug=True) 