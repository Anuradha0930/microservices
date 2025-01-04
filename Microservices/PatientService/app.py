import pymongo

from flask import Flask
from flask import request,jsonify
from flask_cors import CORS

mongoclient = pymongo.MongoClient("mongodb://mongodb:27017")
database = mongoclient['customers']
collection = database['customers']

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


#Get API
@app.route('/GetPatient/<int:patient_id>',methods=["GET"])
def GetPatient(patient_id):
    sendData = []
    try:
        patient = collection.find_one({"PatientID":patient_id})

        if not patient:
            return jsonify({"error":"no records found"})

        patient["_id"] = str(patient["_id"])
        sendData.append(patient)

        return jsonify(sendData)
    
    except Exception as e:
         return jsonify({"error": str(e)})

#Get API All
@app.route('/GetAllPatients',methods=["GET"])
def GetAllPatiens():
    sendData = []
    try:
        patients = collection.find({})

        if not patients:
            return jsonify({"error":"no records found"})

        for patient in patients:
            patient["_id"] = str(patient["_id"])
            sendData.append(patient)

        return jsonify(sendData)
    
    except Exception as e:
         return jsonify({"error": str(e)})

#Insert API
@app.route("/AddPatient", methods=["POST"])
def AddPatient():
    patient = request.get_json()

    if not patient['PatientID'] or patient['PatientID']=='':
        return jsonify({"error":"PatientID is not valid"})
    try:
        collection.insert_one(patient)
        return jsonify({"success":"Successfully Inserted"})
    except Exception as e:
        return jsonify({"error":str(e)})

#Update API
@app.route("/UpdatePatient/<int:patient_id>",methods=["PUT"])
def UpdatePatient(patient_id):
    patient = request.get_json()

    if not patient['PatientID'] or patient['PatientID']=='':
        return jsonify({"error":"PatientID is not valid"})

    try:
        res = collection.update_one({"PatientID": patient_id},
        {"$set": 
            {
                "FullName": patient["FullName"],
                "DOB":patient["DOB"],
                "Email": patient["Email"],
                "EmergencyNumber": patient["EmergencyNumber"],
                "Gender": patient["Gender"],
                "PatientID": patient["PatientID"],
                "Phone": patient["Phone"]
            }
        })

        return jsonify({"success":"Record Updated Successfully", "rows_affected":res.matched_count})

    except Exception as e:
        return jsonify({"error":str(e)})


#Delete API
@app.route("/DeletePatient/<int:patient_id>", methods=["DELETE"])
def DeletePatient(patient_id):
    print(patient_id)
    try:
        res = collection.delete_one({"PatientID":patient_id})
        return jsonify({"success":"Record Deleted Successfuly", "rows_affected":res.deleted_count})
    except Exception as e:
        return jsonify({"error":str(e)})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000)
    # app.run()
