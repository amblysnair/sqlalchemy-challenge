# Import the dependencies.
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine,func
from flask import  Flask,jsonify



#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine,reflect=True)


# Save references to each table

Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB

session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################
last_twelve_months = '2016-08-23'
@app.route("/")
def welcome():
    return (
        f"<p>Hawaii weather API. </p>"   
    )
@app.route("/app/v1.0/percipitation") 
def percipitation():
    p_results = session.query(Measurement.date,Measurement.prcp).\
    filter(Measurement.date >= last_twelve_months).all()
    return jsonify(p_results)
@app.route("/app/v1.0/station") 
def station():
    s_results = session.query(Station.station).all()
    return jsonify(s_results)
@app.route("/app/v1.0/tobs")
def tobs():
    t_results = session.query(Measurement.tobs).\
    filter(Measurement.station ==station).\
    filter(Measurement.date >= last_twelve_months).all()
    return jsonify(t_results)

if __name__ == '__main__':
    app.run(debug=True)