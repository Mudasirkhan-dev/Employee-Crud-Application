from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/employee_database"
mongo = PyMongo(app)

@app.route("/employees", methods=["POST"])
def insert_employee():
    data = request.json

    if not data:
        return jsonify({"error": "Invalid data"}), 400

    mongo.db.employees.insert_one(data)
    return jsonify({"message": "Data inserted successfully"}), 201

@app.route("/employees/<string:employee_id>", methods=["PUT"])
def update_employee(employee_id):
    data = request.json

    if not data:
        return jsonify({"error": "Invalid data"}), 400

    result = mongo.db.employees.update_one({"_id": ObjectId(employee_id)}, {"$set": data})

    if result.modified_count > 0:
        return jsonify({"message": "Data updated successfully"})
    else:
        return jsonify({"error": "Failed to update data"}), 404

@app.route("/employees/<string:employee_id>", methods=["DELETE"])
def delete_employee(employee_id):
    result = mongo.db.employees.delete_one({"_id": ObjectId(employee_id)})

    if result.deleted_count > 0:
        return jsonify({"message": "Data deleted successfully"})
    else:
        return jsonify({"error": "Failed to delete data"}), 404

@app.route("/employees/<string:employee_id>", methods=["GET"])
def retrieve_employee(employee_id):
    data = mongo.db.employees.find_one({"_id": ObjectId(employee_id)})

    if data:
        # Convert ObjectId to string for JSON serialization
        data['_id'] = str(data['_id'])
        return jsonify({"data": data})
    else:
        return jsonify({"error": "Employee not found"}), 404

# Add a new route for GET requests to /employees
@app.route("/employees", methods=["GET"])
def get_all_employees():
    # Retrieve all employees from the database
    employees = list(mongo.db.employees.find())

    # Convert ObjectId to string for JSON serialization
    for employee in employees:
        employee['_id'] = str(employee['_id'])

    return jsonify({"data": employees})

if __name__ == "__main__":
    app.run(debug=True)



