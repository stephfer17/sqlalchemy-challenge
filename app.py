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
        f"Please put a date in start and end yyyy-mm-dd<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"

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
 
#AskBSC Helped me out 
@app.route("/api/v1.0/<start>")
def Start_date(start):
    calc = [Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    results_calc = (session.query(*calc)).\
    filter(func.strftime("%Y-%m-%d",Measurement.date)>=start).group_by(Measurement.date).all()
     # to catch all the data 
    start_date = []                       
    for climate_starter in results_calc:
        start_dates = {}
        start_dates["Date"] = climate_starter[0]
        start_dates["Low Temp"] = climate_starter[1]
        start_dates["Avg Temp"] = climate_starter[2]
        start_dates["High Temp"] = climate_starter[3]
        start_date.append(results_calc)
    return jsonify(start_dates)
    
@app.route("/api/v1.0/<start>/<end>")
def end_date(start,end):
    calc_end = [Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    results_end = (session.query(*calc_end)).\
        filter(func.strftime("%Y-%m-%d"(Measurement.date)>=start)).\
        filter(func.strftime("%Y-%m-%d"(Measurement.date)<=end)).group_by(Measurement.date).all()
    #same thing but for end 
    start_date = []                       
    for climate_starter in results_calc:
        start_dates = {}
        start_dates["Date"] = climate_starter[0]
        start_dates["Low Temp"] = climate_starter[1]
        start_dates["Avg Temp"] = climate_starter[2]
        start_dates["High Temp"] = climate_starter[3]
        start_date.append(start_dates)
    return jsonify(results_end)
 # for debugging   
if __name__ == '__main__':
    app.run(debug=True) 