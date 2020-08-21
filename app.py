import os
from datetime import date

from flask import Flask, render_template, redirect, url_for, request, flash
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
    temp=User.query.filter_by(interviewer=interviewer,date_created=date_created,slot=slot).first()
    if temp:
      # flash("Interviewer not availble!!")
      #return render_template("index.html")
      return "<h1>Busy</h1>"
    else: 
      user= User(student_name=student_name,email=email, interviewer=interviewer, date_created=date_created, slot=slot)
      db.session.add(user)
      db.session.commit()
      # flash("Added")
      # return render_template("index.html")
      return "<h1>yes</h1>"
      
  else: 
    return render_template("index.html")

@app.route("/show_all")
def show():
  return render_template("show_all.html", values=User.query.all())

@app.route("/edit/<id>",methods=["POST","GET"])
def index(id):
  user = User.query.filter_by(id=id).first()
  if request.method == "POST":
    interviewer= request.form["interviewer"]
    date_created= request.form["date"]
    slot=request.form["slot"]
    temp=User.query.filter_by(interviewer=interviewer,date_created=date_created,slot=slot).first()
    if temp:
      return "<h1>Busy</h1>"
    else:
      user.interviewer=interviewer
      user.date_created=date_created
      user.slot=slot
      db.session.commit()
      return render_template("show_all.html", values=User.query.all())
  else:
    return render_template("edit.html", values=user)


if __name__ == '__main__':
    db.create_all()
    app.secret_key = os.urandom(24)
    app.run(debug=True, port=int(os.getenv('PORT', 5000)))