from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import pandas as pd
import numpy as np
from flask import Flask, jsonify
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False #flask automatically organizes output into alphabetical order - this line stops that. 

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
base = automap_base()
base.prepare(engine)
measurement = base.classes.measurement
station = base.classes.station

last_year = dt.date(2017,8,23)-dt.timedelta(days=365)

@app.route("/")
def home():
    return ("Hawaii Vacation!<br><br>"
            f"Available Routes:<br>"
            f"<br>"
            f"/api/v1.0/precipitation<br>"
            f" Last 12 months of rain<br>"
            f"<br>"
            f"/api/v1.0/stations<br>"
            f" Stations<br>"
            f"<br>"
            f"/api/v1.0/tobs"
            f"<br>"
            f" Temperature and Dates from most active station<br>"
            f"<br>"
            f"/api/v1.0/&lt;start&gt;<br>"
            f" Minimum, maximum, and average of specific date<br>"
            f" Please enter as YYYY-MM-DD<br>"
            f"<br>"
            f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br>"
            f" Minimum, maximum, and average for specified start and end date<br>"
            f" Please enter range as YYYY-MM-DD/YYY-MM-DD for example: 2016-04-19/1017-04-19<br>")

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    question_two = session.query(measurement.date, measurement.prcp).filter(measurement.date > last_year).all()
    date_pcp = pd.DataFrame(question_two)
    date_sort = date_pcp.sort_values("date")
    session.close()
    return date_sort.to_json(orient= "records") #records to get list of dictionaries


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    total_stations = session.query(station.station).all()
    tot_stations = list(np.ravel(total_stations))
    session.close()
    return jsonify(tot_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    most_active_data = session.query(measurement.tobs).\
    filter(measurement.station == "USC00519281").\
    filter(measurement.date > last_year).all()
    year_active = list(np.ravel(most_active_data))
    session.close()
    return jsonify(year_active)


@app.route("/api/v1.0/<start>")
def start_function(start):
    session = Session(engine)
    most_active_stat = session.query(func.min(measurement.tobs),func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date > start).first()
    session.close()
    return jsonify(min = most_active_stat[0], max = most_active_stat[1], avg = most_active_stat[2])

@app.route("/api/v1.0/<start>/<end>")
def end_function(start,end):
    session = Session(engine)
    most_active_stat = session.query(func.min(measurement.tobs),func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date > start, measurement.date < end).first()
    session.close()
    return jsonify(start = start, end = end, min = most_active_stat[0], max = most_active_stat[1], avg = most_active_stat[2])
    #flask autmatically puts it in alphabetical order - changed this in line 9 

if __name__  == "__main__": 
    app.run(debug = True)
