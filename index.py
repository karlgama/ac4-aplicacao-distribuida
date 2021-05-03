from flask import Flask, render_template, request, redirect, Response
from flask_sqlalchemy import SQLAlchemy
import requests
import sqlite3

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///alunos.db"
db = SQLAlchemy(app)


@app.route("/")
def index():
    students = Student.query.all()
    return render_template("index.html", students = students)

@app.route("/students", methods=['GET', 'POST'])
def students():
    if request.method == 'GET':
        return render_template("cadastrar.html")
        
    elif request.method == 'POST':
        student = Student(request.form['name'],request.form['email'] , request.form['numero'] , request.form['cep'], request.form['complemento'])
        db.session.add(student)
        db.session.commit()
        return redirect("/")    

@app.route("/students/<int:ra>", methods=['DELETE', 'PUT'])
def delete(ra):
    student = Student.query.get(ra)
    db.session.delete(student)
    db.session.commit()
    return Response(status=204)


@app.route("/edit/<int:ra>", methods=['GET', 'POST'])
def edit(ra):
    student = Student.query.get(ra)
    if request.method == 'GET':
        return render_template('cadastrar.html', student = student)
    elif request.method == 'POST':
        student.name = request.form['name']
        student.email = request.form['email']
        student.numero = request.form['numero']
        student.cep =  request.form['cep']
        student.complemento =  request.form['complemento']
        db.session.commit()
        return redirect("/")


class Student(db.Model):
    ra = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(60))
    email = db.Column(db.String(50))
    logradouro = db.Column(db.String(50))
    numero = db.Column(db.String(20))
    cep = db.Column(db.String(10))
    complemento = db.Column(db.String(60))

    def __init__(self, name, email, numero, cep, complemento=''):
        
        self.name = name
        self.email = email
        self.logradouro = consulta_cep(cep)
        self.numero = numero
        self.cep = cep
        self.complemento = complemento


def consulta_cep(cep):
    try:
        response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
        logradouro = response.json()['logradouro']
        return logradouro
    except:
        return "erro ao consultar cep:"+cep

if __name__ == "__main__":
    app.run(debug=True)
