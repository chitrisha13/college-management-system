from flask import Blueprint, request, jsonify
from config import db
from bson import ObjectId

departments_bp = Blueprint('departments', __name__)

def dept_serializer(dept):
    return {
        "id": str(dept["_id"]),
        "name": dept.get("name"),
        "code": dept.get("code")
    }

@departments_bp.route('/departments', methods=['POST'])
def create_department():
    data = request.json
    result = db.departments.insert_one(data)
    return jsonify({"message": "Department created", "id": str(result.inserted_id)}), 201

@departments_bp.route('/departments', methods=['GET'])
def get_departments():
    departments = list(db.departments.find())
    return jsonify([dept_serializer(d) for d in departments]), 200

@departments_bp.route('/departments/<id>', methods=['GET'])
def get_department(id):
    dept = db.departments.find_one({"_id": ObjectId(id)})
    if not dept:
        return jsonify({"error": "Department not found"}), 404
    return jsonify(dept_serializer(dept)), 200

@departments_bp.route('/departments/<id>', methods=['PUT'])
def update_department(id):
    data = request.json
    db.departments.update_one({"_id": ObjectId(id)}, {"$set": data})
    return jsonify({"message": "Department updated"}), 200

@departments_bp.route('/departments/<id>', methods=['DELETE'])
def delete_department(id):
    db.departments.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Department deleted"}), 200