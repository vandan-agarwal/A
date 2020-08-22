import os
import datetime

# date_1 = datetime.datetime.strptime(start_date, "%m/%d/%y")

# end_date = date_1 + datetime.timedelta(days=10)
# date_2=datetime.strftime(end_date)
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
db = SQLAlchemy(app)

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

    
def getdateplus(start_date):
  date_1 = datetime.datetime.strptime(start_date, "%m/%d/%Y")
  end_date = date_1 + datetime.timedelta(days=1)
  date_2=end_date.strftime("%m/%d/%Y")
  return date_2


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///.data/db.sqlite3'


@app.route("/email")
def send_mail():
  sendmailLivePass('vandanrkt@gmail.com')
  return "<h1>Message has been sent!</h1>"




class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(50))
    email=db.Column(db.String(50))

class Busy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    Date=db.Column(db.String(10))
    start=db.Column(db.String(5))
    end=db.Column(db.String(5))

class Interview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student1 = db.Column(db.String(50))
    student2 = db.Column(db.String(50))
    date = db.Column(db.String(50))
    start=db.Column(db.String(5))
    end=db.Column(db.String(5))
    

@app.route('/', methods=["POST","GET"])
def home():
  if request.method == "POST":
    student1 = request.form["student1"]
    student2 = request.form["student2"]
    date = request.form["date"]
    start=request.form["start"]
    end=request.form["end"]
    if start<end:
      f1=Busy.query.filter_by(name=student1)
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
    users=User.query.all()
    if len(users)<2:
      flash('Users are less than 2')
      return render_template("index.html", values=users)
    else:  
      return render_template("index.html", values=users)
      

@app.route("/show_all")
def show():
  return render_template("show_all.html", values=User.query.all())

@app.route("/test")
def test():
  Te= User.query.all()
  if len(Te)==2:
    return "<h1> found</h1>"
  else:
    return "<h1> Not found</h1>"
  
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