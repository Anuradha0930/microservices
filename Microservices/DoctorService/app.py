import pymongo

from flask import Flask
from flask import request,jsonify
from flask_cors import CORS

mongoclient = pymongo.MongoClient("mongodb://mongodb:27017")
database = mongoclient['doctors']
collection = database['doctors']

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


#Get API
@app.route('/GetDoctor/<int:doctor_id>',methods=["GET"])
def GetDoctor(doctor_id):
    sendData = []
    try:
        doctor = collection.find_one({"DoctorID":doctor_id})

        if not doctor:
            return jsonify({"error":"no records found"})

        doctor["_id"] = str(doctor["_id"])
        sendData.append(doctor)

        return jsonify(sendData)
    
    except Exception as e:
         return jsonify({"error": str(e)})

#Get API All
@app.route('/GetAllDoctors',methods=["GET"])
def GetAllDoctors():
    sendData = []
    try:
        doctors = collection.find({})

        if not doctors:
            return jsonify({"error":"no records found"})

        for doctor in doctors:
            doctor["_id"] = str(doctor["_id"])
            sendData.append(doctor)

        return jsonify(sendData)
    
    except Exception as e:
         return jsonify({"error": str(e)})

#Insert API
@app.route("/AddDoctor", methods=["POST"])
def AddDoctor():
    doctor = request.get_json()

    if not doctor['DoctorID'] or doctor['DoctorID']=='':
        return jsonify({"error":"DoctorID is not valid"})
    try:
        collection.insert_one(doctor)
        return jsonify({"success":"Successfully Inserted"})
    except Exception as e:
        return jsonify({"error":str(e)})

#Update API
@app.route("/UpdateDoctor/<int:doctor_id>",methods=["PUT"])
def UpdateDoctor(doctor_id):
    doctor = request.get_json()

    if not doctor['DoctorID'] or doctor['DoctorID']=='':
        return jsonify({"error":"DoctorID is not valid"})

    try:
        res = collection.update_one({"DoctorID": doctor_id},
        {"$set": 
            {
                "DoctorID": doctor["DoctorID"],
                "FullName": doctor["FullName"],
                "Specialization": doctor["Specialization"],
                "DOB":doctor["DOB"],
                "Email": doctor["Email"],
                "Gender": doctor["Gender"],
                "Phone": doctor["Phone"],
            }
        })

        return jsonify({"success":"Record Updated Successfully", "rows_affected":res.matched_count})

    except Exception as e:
        return jsonify({"error":str(e)})


#Delete API
@app.route("/DeleteDoctor/<int:doctor_id>", methods=["DELETE"])
def DeleteDoctor(doctor_id):
    try:
        res = collection.delete_one({"DoctorID":doctor_id})
        return jsonify({"success":"Record Deleted Successfuly", "rows_affected":res.deleted_count})
    except Exception as e:
        return jsonify({"error":str(e)})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000)
    # app.run()
