from flask import Blueprint, request, jsonify
from config import db
from bson import ObjectId

books_bp = Blueprint('books', __name__)

def book_serializer(book):
    return {
        "id": str(book["_id"]),
        "title": book.get("title"),
        "author": book.get("author"),
        "department_id": book.get("department_id")
    }

@books_bp.route('/books', methods=['POST'])
def create_book():
    data = request.json
    result = db.books.insert_one(data)
    return jsonify({"message": "Book created", "id": str(result.inserted_id)}), 201

@books_bp.route('/books', methods=['GET'])
def get_books():
    books = list(db.books.find())
    return jsonify([book_serializer(b) for b in books]), 200

@books_bp.route('/books/<id>', methods=['GET'])
def get_book(id):
    book = db.books.find_one({"_id": ObjectId(id)})
    if not book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book_serializer(book)), 200

@books_bp.route('/books/<id>', methods=['PUT'])
def update_book(id):
    data = request.json
    db.books.update_one({"_id": ObjectId(id)}, {"$set": data})
    return jsonify({"message": "Book updated"}), 200

@books_bp.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    db.books.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Book deleted"}), 200