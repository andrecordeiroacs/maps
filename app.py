import io
from flask import Flask, render_template, redirect, url_for, make_response
from flask import jsonify
from flask import request
import pymysql
from db_config import mysql
from flask import flash, session, render_template, request, redirect
import uuid
import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

# cache = Cache(config={'CACHE_TYPE': 'simple'})
app = Flask(__name__)
# cache.init_app(app)
app.secret_key = "secret key"

@app.route('/')
def form_open():
	return render_template('index.html')

@app.route('/redirect1')
def form_redirect1():
        return render_template('voluntary.html')

@app.route('/redirect2')
def form_redirect2():
        return render_template('server.html')


@app.route('/submit_voluntary', methods=['POST'])
def form_submit():
	_name = request.form['inputName']
	_email = request.form['inputEmail']
	_phone = request.form['inputPhone']
	_city = request.form['inputCity']
    _services = str(request.form.getlist('checkbox'))
	_comments = request.form['inputComments']
    flash('Obrigado! Em breve entraremos em contato com voce!')
    print("Olha leeee2")
	print(_services)
	lead_id = str(uuid.uuid1())


	#escrevendo no banco
	conn = mysql.connect()
        cursor = conn.cursor()
        user_sql = "INSERT INTO `ajudelocal_voluntary`(`id`, `name`, `email`, `phone`, `city`, `services`, `comments`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        sql_where = (lead_id, _name, _email, _phone, _city, _services, _comments)
        cursor.execute(user_sql, sql_where)
        row = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
	return redirect('/')

@app.route('/submit_server', methods=['POST'])
def form_submit_server():
	_name = request.form['inputName']
	_email = request.form['inputEmail']
	_phone = request.form['inputPhone']
	_city = request.form['inputCity']
        _services = str(request.form.getlist('checkbox'))
	_comments = request.form['inputComments']
        flash('Obrigado! Em breve entraremos em contato com voce!')
        print("Olha leeee2")
	print(_services)
	lead_id = str(uuid.uuid1())


	#escrevendo no banco
	conn = mysql.connect()
        cursor = conn.cursor()
        user_sql = "INSERT INTO `ajudelocal_server`(`id`, `name`, `email`, `phone`, `city`, `services`, `comments`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        sql_where = (lead_id, _name, _email, _phone, _city, _services, _comments)
        cursor.execute(user_sql, sql_where)
        row = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
	return redirect('/')


if __name__ == "__main__":
    app.secret_key = 'secret key'
    app.run()



# @app.route('/submit', methods=['POST'])
# def login_submit():
# 	_email = request.form['inputEmail']
# 	_password = request.form['inputPassword']
# 	# validate the received values
# 	if _email and _password and request.method == 'POST':
# 		#check user exists
# 		conn = mysql.connect()
# 		cursor = conn.cursor()
# 		sql = "SELECT * FROM cp_users WHERE email=%s"
# 		sql_where = (_email,)
# 		cursor.execute(sql, sql_where)
# 		row = cursor.fetchone()
# 		if row:
# 			if (row[2] == _password):
# 				session['email'] = row[1]
# 				cursor.close()
# 				conn.close()
# 				session["id"]=row[0]
# 				session["manager_id"]=row[5]
# 				session["company_id"]=row[4]
# 	if _email and _password and request.method == 'POST':
# 		#check user exists
# 		conn = mysql.connect()
# 		cursor = conn.cursor()
# 		sql = "SELECT * FROM cp_users WHERE email=%s"
# 		sql_where = (_email,)
# 		cursor.execute(sql, sql_where)
# 		row = cursor.fetchone()
# 		if row:
# 			if (row[2] == _password):
# 				session['email'] = row[1]
# 				cursor.close()
# 				conn.close()
# 				session["id"]=row[0]
# 				session["manager_id"]=row[5]
# 				session["company_id"]=row[4]
# 	if _email and _password and request.method == 'POST':
# 		#check user exists
# 		conn = mysql.connect()
# 		cursor = conn.cursor()
# 		sql = "SELECT * FROM cp_users WHERE email=%s"
# 		sql_where = (_email,)
# 		cursor.execute(sql, sql_where)
# 		row = cursor.fetchone()
# 		if row:
# 			if (row[2] == _password):
# 				session['email'] = row[1]
# 				cursor.close()
# 				conn.close()
# 				session["id"]=row[0]
# 				session["manager_id"]=row[5]
# 				session["company_id"]=row[4]
# 				id=session.get("id",None)
# 				session["admin"]=row[11]
# 				if (row[11] == "1"):
# 					conn2 = mysql.connect()
# 					cursor2 = conn2.cursor()
# 					sql2 = "SELECT user_id,name FROM `cp_users` WHERE manager_id = %s"
# 					sql_where2 = (id)
# 					cursor2.execute(sql2, sql_where2)
# 					row2 = cursor2.fetchall()
# 					session['returns'] = row2
#
# 					#sql3 = "SELECT * FROM `cp_rating` WHERE manager_id = %s"
# 					sql3 = "SELECT * FROM cp_rating LEFT JOIN cp_users ON cp_rating.employee_id = cp_users.user_id WHERE cp_rating.manager_id = %s"
# 					sql_where2 = (id)
# 					cursor2.execute(sql3, sql_where2)
# 					row3 = cursor2.fetchall()
# 					session['rating_returns'] = row3
# 					cursor2.close()
# 					conn2.close()
# 					session["m"] = len(row3)
# 					session["k"] = len(row2)
# 					return render_template('index.html', row2 = session.get('returns',None), k = session.get("k",None), row3 = session.get("rating_returns", None), m = session.get("m",None), admin = session.get("admin",None))
# 				else:
# 					conn2 = mysql.connect()
# 					cursor2 = conn2.cursor()
# 					sql2 = "SELECT user_id,name FROM `cp_users` WHERE company_id = %s"
# 					sql_where2 = session.get("company_id",None)
# 					cursor2.execute(sql2, sql_where2)
# 					row2 = cursor2.fetchall()
# 					session['returns'] = row2
#
# 					#sql3 = "SELECT * FROM `cp_rating` WHERE manager_id = %s"
# 					sql3 = "SELECT * FROM cp_rating LEFT JOIN cp_users ON cp_rating.employee_id = cp_users.user_id WHERE cp_users.company_id = %s"
# 					sql_where2 = session.get("company_id",None)
# 					cursor2.execute(sql3, sql_where2)
# 					row3 = cursor2.fetchall()
# 					session['rating_returns'] = row3
# 					cursor2.close()
# 					conn2.close()
# 					session["m"] = len(row3)
# 					session["k"] = len(row2)
# 					return render_template('index.html', row2 = session.get('returns',None), k = session.get("k",None), row3 = session.get("rating_returns", None), m = session.get("m",None), admin = session.get("admin",None))
# 			else:
# 				flash('Invalid password!')
# 				return redirect('/')
# 		else:
# 			flash('Invalid email/password!')
# 			return redirect('/')
