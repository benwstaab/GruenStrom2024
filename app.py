import json
from flask import Flask, render_template, request
import requests
from flask_cors import CORS  # Import Flask-CORS
from api.data.endPoints import BackendServerException
from api.tools.converter import InputParameterException
from api.usecase import (
    stromRechnerUsecase,
    stromRechnerSolarUsecase,
    stromRechnerCombinedUsecase,
)

app = Flask(__name__)
CORS(app)  # Aktiviert CORS für alle Routen

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("home.html")

@app.route("/strom", methods=["GET", "POST"])
def stromPrediction():
    zip_code = request.form.get("zip")

    resp = requests.get("https://gruenstromindex.de/v2.0/gsi/prediction", params={"zip": zip_code})
    response = resp.json()

    data = [{"time": entry["epochtime"], "data": entry["eevalue"]} for entry in response.get("forecast", [])]

    return render_template("index.html", data=json.dumps(data))

@app.route("/stromRechner", methods=["GET", "POST"])
def stromRechner():
    zip_code = request.args.get("zip")
    dur = request.args.get("dur")
    take_off = request.args.get("takeOff")
    split = request.args.get("split")

    return executeUsecase(stromRechnerUsecase, zip_code, dur, take_off, split)

@app.route("/stromRechnerSolar", methods=["GET", "POST"])
def stromRechnerSolar():
    zip_code = request.args.get("zip")
    dur = request.args.get("dur")
    take_off = request.args.get("takeOff")
    split = request.args.get("split")

    return executeUsecase(stromRechnerSolarUsecase, zip_code, dur, take_off, split)

@app.route("/stromRechnerCombined", methods=["GET", "POST"])
def stromRechnerCombined():
    zip_code = request.args.get("zip")
    dur = request.args.get("dur")
    take_off = request.args.get("takeOff")
    split = request.args.get("split")

    return executeUsecase(stromRechnerCombinedUsecase, zip_code, dur, take_off, split)

@app.route("/stromTest")
def stromTest():
    resp = requests.get("https://gruenstromindex.de/v2.0/gsi/prediction", params={"zip": "60594"})
    response = resp.json()

    return json.dumps(response)

@app.route("/test")
def test():
    return "system online"

def executeUsecase(usecase, *args, **kwargs):
    try:
        result = usecase.execute(*args, **kwargs)
        return json.dumps({"code": 200, "data": result})
    except BackendServerException as e:
        return json.dumps({"code": 501, "data": str(e)})
    except InputParameterException as e:
        return json.dumps({"code": 502, "data": str(e)})
    except Exception as e:
        return json.dumps({"code": 500, "data": str(e)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=False)
