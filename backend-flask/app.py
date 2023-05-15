from flask import Flask, jsonify, request, json
from flask_sqlalchemy import SQLAlchemy
import numpy as np

#from FinalController import FinalController
from NewFinalController import NewFinalController

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

#
#   definition of DB tables
#

class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    data = db.Column(db.JSON)

with app.app_context(): 
    db.create_all()


#
#   definition of routes/adresses for ajax communication
#


@app.route('/')
def index():
    print("Working")
    return 'OK', 200


#   updates values for driver
@app.route('/sendYValuesToBackend', methods=['POST'])
def sendYValuesToBackend():
    print('Called from Settings')
    received_data = request.get_json()
    yValues = np.array(received_data['yValues'])
    yValues2 = np.array(received_data['yValues2'])

    values = np.concatenate((yValues, yValues2), axis=1)

    NewFinalController.setValues(values)
    
    return 'OK', 200

#   sets starttime for driver to synchronize GUI with driver
@app.route('/sendStartTimeToBackend', methods=['POST'])
def sendStartTimeToBackend():
    print("Called")
    received_data = request.get_json()
    startTime = received_data['startTime']/1000

    NewFinalController.startStreaming(startTime)

    return 'OK', 200

#   adds new state to database
@app.route('/addSpectrumToDB', methods=['POST'])
def addSpectrumToDB():
    print("Call successful")
    received_data = request.get_json()
    name = received_data['name']
    data = received_data['channelSliderValues']

    states = State.query.filter(State.name == name).all()
    if (states != []):
        return "A state with this name already exists."

    NewState = State(name=name, data=data)

    try:
        db.session.add(NewState)
        db.session.commit()
    except Exception as e:
        print(e)
        return "There was an issue adding this Spectrum"

    return 'OK', 200

#   loads all states from database
@app.route('/getSpectrumsFromDB', methods=['GET'])
def getSpectrumsFromDB():
    print("Call successful")

    # get spectrums and cast them to json-format
    states = State.query.all()
    statesDict = {}
    for state in states:
        statesDict[state.name] = state.__dict__
        statesDict[state.name].pop('_sa_instance_state')

    response = app.response_class(
        response=json.dumps(statesDict),
        status=200,
        mimetype='application/json'
    )
    return response

#   loads single state from database from given name
@app.route('/getSpectrumFromDB/<spectrumName>', methods=['GET'])
def getSpectrumFromDB(spectrumName):
    print("Call successful")

    spectrum = State.query.filter(State.name == spectrumName).all()
    spectrumDict = spectrum[0].__dict__
    spectrumDict.pop('_sa_instance_state')

    response = app.response_class(
        response=json.dumps(spectrumDict),
        status=200,
        mimetype='application/json'
    )
    return response

#   deletes single state from database
@app.route('/deleteSpectrumFromDB/<spectrumName>', methods=['GET'])
def deleteSpectrumFromDB(spectrumName):
    print('Call successful')

    spectrum = State.query.filter(State.name == spectrumName).all()[0]

    try: 
        db.session.delete(spectrum)
        db.session.commit()
        print("Spectrum " + spectrumName + " has been deleted successfully.")
    except Exception as e:
        print(e)
        return 'There was an issue deleting this spectrum.'


    return 'OK', 200



app.run(debug=True, use_reloader=False)