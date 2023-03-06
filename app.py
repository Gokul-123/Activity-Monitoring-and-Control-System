# Store this code in 'app.py' file

from operator import ge
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import mysql.connector
import re
import math,random
import csv
app = Flask(__name__)


app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mysql1234'
app.config['MYSQL_DB'] = 'mini_project'

mysql = MySQL(app)

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM student_login WHERE reg_no = % s AND pass = % s', (username, password, ))
		account = cursor.fetchone()
		if account:
			# session['loggedin'] = True
			# session['id'] = account['id']
			# session['username'] = account['username']
			msg = 'Logged in successfully !'
			otp =generateOTP()
			sys = systemavail(otp,username)
			if sys=='0':
				return render_template('login.html', msg = "No system available")
			msg = "System :{} \n OTP :{}".format(sys,otp)
			return render_template('index.html', msg = msg)
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)

def generateOTP():
      digits = "0123456789"
      otp=""
      for i in range(4):
        otp+= digits[math.floor(random.random()*10)]
      return str(otp)
def systemavail(otp,username):
	with open("cred.csv",newline="") as cred:
		data = [i for i in csv.DictReader(cred)]
		print(data)
		for i in range(0,len(data)):
			if data[i]['status']=="no":
				print(data[i]['system_no'])
				system_no=data[i]['system_no']
				data[i]['otp']=otp
				data[i]['status']='yes'
				data[i]['username']=username
				print(data)
				with open("cred.csv","w",newline="") as csvfile:
					readheader = data[0].keys()
					writer = csv.DictWriter(csvfile,fieldnames= readheader)
					writer.writeheader()
					writer.writerows(data)
					return system_no
		return "0"
           
						
@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('login'))

@app.route('/admin', methods =['GET', 'POST'])
def admin():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM admin_login WHERE username = % s AND pass = % s', (username, password, ))
		account = cursor.fetchone()
		if account:
			# session['loggedin'] = True
			# session['id'] = account['id']
			# session['username'] = account['username']
			msg = 'Logged in successfully !'
			return render_template('index.html', msg = msg)
		else:
			msg = 'Incorrect username / password !'
	return render_template('admin.html', msg = msg)
