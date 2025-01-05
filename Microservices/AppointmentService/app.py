import pymongo

#test commit Anuradha 1

from flask import Flask
from flask import request,jsonify
from flask_cors import CORS

mongoclient = pymongo.MongoClient("mongodb://mongodb:27017")
database = mongoclient['appointments']
collection = database['appointments']

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


#Get Appointment
@app.route('/GetAppointnment/<int:appointment_id>',methods=["GET"])
def GetAppointment(appointment_id):
    sendData = []
    try:
        appointment = collection.find_one({"AppointmentID":appointment_id})

        if not appointment:
            return jsonify({"error":"no records found"})

        appointment["_id"] = str(appointment["_id"])
        sendData.append(appointment)

        return jsonify(sendData)
    
    except Exception as e:
         return jsonify({"error": str(e)})
    
#Get Appointments by patient
@app.route('/GetAppointnmentByPatient/<int:patient_id>',methods=["GET"])
def GetAppointmentPatient(patient_id):
    sendData = []
    try:
        appointments = collection.find({"PatientID":patient_id})

        if not appointments:
            return jsonify({"error":"no records found"})

        for appointment in appointments:
            appointment["_id"] = str(appointment["_id"])
            sendData.append(appointment)

        return jsonify(sendData)
    
    except Exception as e:
         return jsonify({"error": str(e)})

#Get All Appointments
@app.route('/GetAllAppointnments',methods=["GET"])
def GetAllAppointments():
    sendData = []
    try:
        appointments = collection.find({})

        if not appointments:
            return jsonify({"error":"no records found"})

        for appointment in appointments:
            appointment["_id"] = str(appointment["_id"])
            sendData.append(appointment)

        return jsonify(sendData)
    
    except Exception as e:
         return jsonify({"error": str(e)})

#Insert Appointment
@app.route("/AddAppointment", methods=["POST"])
def AddAppointment():
    appointment = request.get_json()

    if not appointment['PatientID'] or appointment['PatientID']=='':
        return jsonify({"error":"PatientID is not valid"})
    try:
        collection.insert_one(appointment)
        return jsonify({"success":"Successfully Inserted"})
    except Exception as e:
        return jsonify({"error":str(e)})

#Update Appointment
@app.route("/UpdateAppointnment/<int:appointment_id>",methods=["PUT"])
def UpdateAppointment(appointment_id):
    appointment = request.get_json()

    if not appointment['AppointmentID'] or appointment['AppointmentID']=='':
        return jsonify({"error":"PatientID is not valid"})

    try:
        res = collection.update_one({"AppointmentID": appointment_id},
        {"$set": 
            {
                "AppointmentID": appointment["AppointmentID"],
                "PatientID": appointment["PatientID"],
                "AppointmentDate":appointment["AppointmentDate"],
                "DoctorID": appointment["DoctorID"],
                "Status": appointment["Status"]
            }
        })

        return jsonify({"success":"Record Updated Successfully", "rows_affected":res.matched_count})

    except Exception as e:
        return jsonify({"error":str(e)})


#Delete Appointment
@app.route("/DeleteAppointnment/<int:appointment_id>", methods=["DELETE"])
def DeleteAppointment(appointment_id):
    try:
        res = collection.delete_one({"AppointmentID":appointment_id})
        return jsonify({"success":"Record Deleted Successfuly", "rows_affected":res.deleted_count})
    except Exception as e:
        return jsonify({"error":str(e)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000)
    # app.run()
