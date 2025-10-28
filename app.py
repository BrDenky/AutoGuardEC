from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345@localhost/UniversityDB'
db = SQLAlchemy(app)

# ---------- MODEL ----------
class Student(db.Model):
    id_student = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(80))

    def __init__(self, name, email):
        self.name = name
        self.email = email

with app.app_context():
    db.create_all()

# ---------- ROUTES ----------
@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([{'id': s.id_student, 'name': s.name, 'email': s.email} for s in students])

@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    new_student = Student(name=data['name'], email=data['email'])
    db.session.add(new_student)
    db.session.commit()
    return jsonify({'message': 'Student created successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)



# Obtener todos
curl -v http://127.0.0.1:5000/students

# Crear nuevo
curl --header "Content-Type: application/json" \
     --request POST \
     --data "{\"name\":\"Kevin Erazo\", \"email\":\"kevin@yachaytech.edu.ec\"}" \
     http://127.0.0.1:5000/students
