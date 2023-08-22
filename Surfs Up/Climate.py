from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    print("Server received request for 'Home' page...")
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
            f"/api/v1.0/<start><br>"
            f" Minimum, maximum, and average of specific date<br>"
            f"<br>"
            f"/api/v1.0/<start>/<end><br>"
            f" Minimum, maximum, and average for specified start and end date")

# @app.route("/api/v1.0/precipitation")
# def precipitation

# @app.route("/api/v1.0/stations")
# def stations

# @app.route("/api/v1.0/tobs")
# def tobs

# @app.route("/api/v1.0/<start>")
# def start

# @app.route("/api/v1.0/<start>/<end>")
# def end


if __name__  == "__main__": 
    app.run(debug = True)
