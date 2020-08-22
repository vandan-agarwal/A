import os
from datetime import date

from flask import Flask, render_template, redirect, url_for, request, flash
from flask_mail import Mail
from flask_mail import Message
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)



app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///.data/db.sqlite3'




app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'amanavearma@gmail.com'
app.config['MAIL_PASSWORD '] = 'Amanverma!2020'
app.config['MAIL_DEFAULT_SENDER'] = 'amanavearma@gmail.com'
app.config['MAIL_MAX_EMAILS'] = None
# app.config['MAIL_SUPPRESS_SEND'] = ''
app.config['MAIL_ASCII_ATTACHMENTS'] = False


mail = Mail(app)


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
      flash('Interviewer Unavailable!!')
      return render_template("index.html")
    else: 
      user= User(student_name=student_name,email=email, interviewer=interviewer, date_created=date_created, slot=slot)
      db.session.add(user)
      db.session.commit()
      flash("Interview Scheduled!!")
      return render_template("index.html")
      
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
      flash('Interviewer Unavailable!!')
      return render_template("edit.html", values=user)
    else:
      user.interviewer=interviewer
      user.date_created=date_created
      user.slot=slot
      db.session.commit()
      flash("Interview Modified!!")
      return render_template("show_all.html", values=User.query.all())
  else:
    return render_template("edit.html", values=user)

@app.route("/email")
def send_mail():
  msg = Message("Hello",sender="amanavearma@gmail.com", recipients=["vandanrkt@gmail.com"])
  mail.send(msg)
  return "<h1>Message has been sent!</h1>"




if __name__ == '__main__':
    db.create_all()
    app.secret_key = os.urandom(24)
    app.run(debug=True, port=int(os.getenv('PORT', 5000)))