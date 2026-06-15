from flask import Flask
from routes.students import students_bp
from routes.staff import staff_bp
from routes.books import books_bp
from routes.departments import departments_bp

app = Flask(__name__)

app.register_blueprint(students_bp)
app.register_blueprint(staff_bp)
app.register_blueprint(books_bp)
app.register_blueprint(departments_bp)

if __name__ == "__main__":
    app.run(debug=True)