# Store this code in 'app.py' file
import pandas as pd
from operator import ge
import webbrowser
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import math,random
import csv
import sqlite3
from csv import writer
import time
app = Flask(__name__)


app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mysql1234'
app.config['MYSQL_DB'] = 'mini_project'
mysql = MySQL(app)
system_no = 1 
l=[]
@app.route('/')
@app.route('/login', methods =['GET', 'POST'])

def login():
	msg = ''
	
	if request.method == 'POST' and 'system_no' in request.form and 'otp' in request.form:
		otp = request.form['otp']
		print(otp)
		with open("../server/cred.csv",newline="") as cred:
			data = [i for i in csv.DictReader(cred)]
			print(data)
			for i in range(0,len(data)):
				if data[i]['system_no'] == str(system_no) and data[i]['otp']==str(otp) :
					username1=data[i]['username']
					l.append(username1)
					msg="YOU ARE GRANTED TO ACCESS THE BROWSER"
					return render_template('index.html', msg = msg)
				else:
					msg="Incorrect OTP !"


	return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
	history_1()
	update()
	l.pop()
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('login'))
def update():
	with open("../server/cred.csv",newline="") as cred:
			data = [i for i in csv.DictReader(cred)]
			# print(data)
			for i in range(0,len(data)):
				
				if str(system_no)==data[i]['system_no']:
					data[i]['otp']=""
					data[i]['status']='no'
					data[i]['username']=""
					print(data)
					with open("../server/cred.csv","w",newline="") as csvfile:
						readheader = data[0].keys()
						writer = csv.DictWriter(csvfile,fieldnames= readheader)
						writer.writeheader()
						writer.writerows(data)
						break

def history_1():
        path="C:\\Users\\Hai\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1\\History"
        con=sqlite3.connect(path)
        c=con.cursor()
        c.execute("SELECT urls.url, urls.title, urls.visit_count, urls.typed_count, datetime(urls.last_visit_time / 1000000 +  (strftime('%s', '1601-01-01' )), 'unixepoch','localtime') as last_visit_time, urls.hidden, datetime(visits.visit_time / 1000000 +  (strftime('%s', '1601-01-01' )), 'unixepoch','localtime') as visit_time, visits.from_visit, datetime(visits.transition/ 1000000 +  (strftime('%s', '1601-01-01' )), 'unixepoch','localtime') as transition FROM urls, visits WHERE urls.id = visits.url")
        results=c.fetchall()
        df = pd.DataFrame(results)
        # for i in results[0:100]:
        # 	print(i)
            
        print(df)
        df.to_csv('data.csv')
        c.close()
        df1=pd.read_csv('data.csv')
        print(len(df1))
        k=[]
        m=[]
        for i in range(0,len(df1)):
            k.append(system_no)
            m.append(l[0])
        df1['system_no']=k
        df1['username']=m
        df1['4']=pd.to_datetime(df1['4'])
        df1['6']=pd.to_datetime(df1['6'])
        df1.to_csv('data.csv')

        with open('data.csv',encoding="utf8") as csv1, open('new.csv','r')as csv2:
            import1 =csv1.readlines()
            import2 =csv2.readlines()
        count=0
        with open('diff.csv','a') as diff:
            
            for row in import1:
              if count==0:
                    count+=1
              else:
                 if row not in import2:
                    writ = writer(diff)
                    print(row)

                    row=str(system_no)+","+str(l[0])+","+row
			
                    diff.write(row)
		          

        with open('new.csv','w')as con:
         for row in import1:           
            con.write(row)




# system_no = 1 
# 		otp = request.form['otp']
# 		with open("../server/cred.csv",newline="") as cred:
# 			data = [i for i in csv.DictReader(cred)]
# 			print(data)
# 			for i in range(0,len(data)):
# 				if data[i]['system_no'] == system_no and data[i]['otp']==otp :
# 					msg="YOU ARE GRANTED TO ACCESS THE BROWSER"