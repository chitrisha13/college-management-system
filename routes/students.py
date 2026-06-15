from flask import Blueprint, request, jsonify
from config import db
from bson import ObjectId

students_bp = Blueprint('students', __name__)

def student_serializer(student):
    return {
        "id": str(student["_id"]),
        "name": student.get("name"),
        "email": student.get("email"),
        "department_id": student.get("department_id"),
        "staff_id": student.get("staff_id")
    }

@students_bp.route('/students', methods=['POST'])
def create_student():
    data = request.json
    result = db.students.insert_one(data)
    return jsonify({"message": "Student created", "id": str(result.inserted_id)}), 201

@students_bp.route('/students', methods=['GET'])
def get_students():
    students = list(db.students.find())
    return jsonify([student_serializer(s) for s in students]), 200

@students_bp.route('/students/<id>', methods=['GET'])
def get_student(id):
    student = db.students.find_one({"_id": ObjectId(id)})
    if not student:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(student_serializer(student)), 200

@students_bp.route('/students/<id>', methods=['PUT'])
def update_student(id):
    data = request.json
    db.students.update_one({"_id": ObjectId(id)}, {"$set": data})
    return jsonify({"message": "Student updated"}), 200

@students_bp.route('/students/<id>', methods=['DELETE'])
def delete_student(id):
    db.students.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Student deleted"}), 200
