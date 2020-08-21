import os
from datetime import date

from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///.data/db.sqlite3'


db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(50))
    email=db.Column(db.String(50))
    interviewer = db.Column(db.String(50))
    date_created = db.Column(db.String(50))		
    slot=db.Column(db.String(50))

@app.route('/', methods=["POST","GET"])
def home():
	if request.method == "POST":
		student_name= request.form["student_name"]
		email= request.form["email"]
		interviewer= request.form["interviewer"]
		date_created= request.form["date"]
		slot=request.form["slot"]
		user= User(student_name=student_name,email=email, interviewer=interviewer, date_created=date_created, slot=slot)
		db.session.add(user)
		db.session.commit()



		return '<h1> Added</h1>'
	else: 
		return render_template("index.html")

# @app.route("/<usr>/<email>")
# def pri(usr,email):
#     return f'<html><h1>{usr}</h1></html>'




# class Interviewer(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     Interviewer = db.Column(db.String(50))
#     Date = db.Column(db.Date)		
#     slot=db.Column(db.String(50))



@app.route('/<name>/<location>')
def index(name, location):
    user = User(name=name, location=location)
    db.session.add(user)
    db.session.commit()

    return '<h1>Added New User!</h1>'

@app.route('/<name>')
def get_user(name):
    user = User.query.filter_by(name=name).first()

    return  '<h1>Added New Use3!</h1>'
  
  
if __name__ == '__main__':
    app.run(debug=True, port=int(os.getenv('PORT', 5000)))