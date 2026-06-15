from flask import Blueprint, request, jsonify
from config import db
from bson import ObjectId

staff_bp = Blueprint('staff', __name__)

def staff_serializer(staff):
    return {
        "id": str(staff["_id"]),
        "name": staff.get("name"),
        "email": staff.get("email"),
        "department_id": staff.get("department_id")
    }

@staff_bp.route('/staff', methods=['POST'])
def create_staff():
    data = request.json
    result = db.staff.insert_one(data)
    return jsonify({"message": "Staff created", "id": str(result.inserted_id)}), 201

@staff_bp.route('/staff', methods=['GET'])
def get_staff():
    staff = list(db.staff.find())
    return jsonify([staff_serializer(s) for s in staff]), 200

@staff_bp.route('/staff/<id>', methods=['GET'])
def get_one_staff(id):
    staff = db.staff.find_one({"_id": ObjectId(id)})
    if not staff:
        return jsonify({"error": "Staff not found"}), 404
    return jsonify(staff_serializer(staff)), 200

@staff_bp.route('/staff/<id>', methods=['PUT'])
def update_staff(id):
    data = request.json
    db.staff.update_one({"_id": ObjectId(id)}, {"$set": data})
    return jsonify({"message": "Staff updated"}), 200

@staff_bp.route('/staff/<id>', methods=['DELETE'])
def delete_staff(id):
    db.staff.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Staff deleted"}), 200
