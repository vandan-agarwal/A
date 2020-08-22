import os
from datetime import date

from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders


def sendmailLivePass(reciever):
    sender= 'amanavearma@gmail.com'

    msg= MIMEMultipart()    
    msg['From'] = sender
    msg['To'] = reciever
    msg['Subject'] = 'Access Granted'
    body = """Hello"""
    msg.attach(MIMEText(body,'plain'))
    s= smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    s.login(sender,'Amanverma!2020')
    text= msg.as_string()
    s.sendmail(sender,reciever,text)


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///.data/db.sqlite3'


@app.route("/email")
def send_mail():
  sendmailLivePass('vandanrkt@gmail.com')
  return "<h1>Message has been sent!</h1>"



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

@app.route("/test")
def test():
  Te= User.query.all()
  
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



if __name__ == '__main__':
    db.create_all()
    app.secret_key = os.urandom(24)
    app.run(debug=True, port=int(os.getenv('PORT', 5000)))