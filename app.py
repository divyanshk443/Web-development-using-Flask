
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import json
from datetime import datetime


with open('config.json', 'r') as c:
    params = json.load(c)["params"]

local_server = True
app = Flask(__name__)

'''
MAIL_SERVER : Name/IP address of the email server.
MAIL_PORT : Port number of server used.
MAIL_USE_SSL : Enable/disable Secure Sockets Layer encryption
Mail server didn't allow to send unencrypted email so ssl used
MAIL_USERNAME : Username of the sender
MAIL_PASSWORD : The password of the corresponding Username of the sender
'''
app.config.update(
	MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD=  params['gmail-password']
)
mail = Mail(app)

'''sqlalchemy for database connection'''

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3307/iit_bhilai'

'''
pymsql-database connector
iit_bhilai-database name
we can put server IP in place of localhost if our server is something different
'''


db = SQLAlchemy(app)


class Contacts(db.Model):
    Sno = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(80), nullable=False)
    Phone = db.Column(db.String(12), nullable=False)
    Email = db.Column(db.String(20), nullable=False)
    Message = db.Column(db.String(120), nullable=False)
    Date = db.Column(db.String(12), nullable=False)
    
@app.route("/")
def home():

    return render_template('Home.html',params=params)


@app.route("/about")
def about():
    return render_template('About.html')


@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    if(request.method=='POST'):
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        message = request.form.get('message')
        entry = Contacts(Name=name, Phone = phone,Email = email, Message = message, Date= datetime.now() )
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from ' + name,
                          sender='kdivyansh658@gmail.com',
                          recipients = [params['gmail-user']],
                          body = message + "\n" + phone
                          )
             
    return render_template('Contact.html')


'''Gmail blocked the login attempt'''

app.run(debug=True)

