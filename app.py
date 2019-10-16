import io
from flask import Flask, render_template, redirect, url_for, make_response
from flask import jsonify
from flask import request
import pymysql
from db_config import mysql
from werkzeug import generate_password_hash, check_password_hash
from flask import flash, session, render_template, request, redirect
import uuid
import datetime

# cache = Cache(config={'CACHE_TYPE': 'simple'})
app = Flask(__name__)
# cache.init_app(app)
app.secret_key = "secret key"

@app.route('/')
def login():
	return render_template('login.html')

@app.route('/index')
def index():
    return render_template('index.html', row2 = session.get('returns',None), k = session.get("k",None), row3 = session.get("rating_returns", None), m = session.get("m",None), admin = session.get("admin",None))

@app.route('/employee', methods=["POST"])
def partner():
	session['employee_id'] = request.form['employee']
	return render_template('employee2.html')

@app.route('/inputRating', methods=["POST"])
def output():
	id = session.get("employee_id",None)
	manager_id = session.get("id",None)
	company_id = session.get("company_id",None)
	template_id = "ca5de35a-201e-40f7-9642-21c595801b27"
	created_at = datetime.date.today()
	rating_id = str(uuid.uuid1())
	var1 = request.form['character']
	var2 = request.form['hability']
	var3 = request.form['attitude']
	var4 = request.form['knowledge']
	rate_metadata = "{"+var1+","+var2+","+var3+","+var4+"}"
	conn2 = mysql.connect()
	cursor2 = conn2.cursor()
	sql2 = "INSERT INTO `cp_rating`(`rating_id`, `template_id`, `employee_id`, `manager_id`, `rate_metadata`, `created_at`) VALUES (%s,%s,%s,%s,%s,%s)"
	sql_where2 = (rating_id,template_id,id,manager_id,rate_metadata,created_at)
	cursor2.execute(sql2, sql_where2)
	conn2.commit()
	if (session.get("admin",None)=="1"):
		sql3 = "SELECT * FROM cp_rating LEFT JOIN cp_users ON cp_rating.employee_id = cp_users.user_id WHERE cp_rating.manager_id = %s"
		sql_where3 = (session.get("id",None))
		cursor2.execute(sql3, sql_where3)
		row3 = cursor2.fetchall()
		session['rating_returns'] = row3
		session["m"] = len(row3)
	else:
		sql3 = "SELECT * FROM cp_rating LEFT JOIN cp_users ON cp_rating.employee_id = cp_users.user_id WHERE cp_rating.company_id = %s"
		sql_where3 = (session.get("company_id",None))
		cursor2.execute(sql3, sql_where3)
		row3 = cursor2.fetchall()
		session['rating_returns'] = row3
		session["m"] = len(row3)
	cursor2.close()
	conn2.close()
	#return render_template('testeoutput.html', manager_id = manager_id, id = id, company_id = company_id, template_id = template_id, created_at = created_at, rating_id =rating_id, rate_metadata = rate_metadata)
	#return redirect('/index')
	return render_template('index.html', row2 = session.get('returns',None), k = session.get("k",None), row3 = session.get("rating_returns", None), m = session.get("m",None), admin = session.get("admin",None))

@app.route('/submit', methods=['POST'])
def login_submit():
	_email = request.form['inputEmail']
	_password = request.form['inputPassword']
	# validate the received values
	if _email and _password and request.method == 'POST':
		#check user exists
		conn = mysql.connect()
		cursor = conn.cursor()
		sql = "SELECT * FROM cp_users WHERE email=%s"
		sql_where = (_email,)
		cursor.execute(sql, sql_where)
		row = cursor.fetchone()
		if row:
			if (row[2] == _password):
				session['email'] = row[1]
				cursor.close()
				conn.close()
				session["id"]=row[0]
				session["manager_id"]=row[5]
				session["company_id"]=row[4]
				id=session.get("id",None)
				session["admin"]=row[11]
				if (row[11] == "1"):
					conn2 = mysql.connect()
					cursor2 = conn2.cursor()
					sql2 = "SELECT user_id,name FROM `cp_users` WHERE manager_id = %s"
					sql_where2 = (id)
					cursor2.execute(sql2, sql_where2)
					row2 = cursor2.fetchall()
					session['returns'] = row2

					#sql3 = "SELECT * FROM `cp_rating` WHERE manager_id = %s"
					sql3 = "SELECT * FROM cp_rating LEFT JOIN cp_users ON cp_rating.employee_id = cp_users.user_id WHERE cp_rating.manager_id = %s"
					sql_where2 = (id)
					cursor2.execute(sql3, sql_where2)
					row3 = cursor2.fetchall()
					session['rating_returns'] = row3
					cursor2.close()
					conn2.close()
					session["m"] = len(row3)
					session["k"] = len(row2)
					return render_template('index.html', row2 = session.get('returns',None), k = session.get("k",None), row3 = session.get("rating_returns", None), m = session.get("m",None), admin = session.get("admin",None))
				else:
					conn2 = mysql.connect()
					cursor2 = conn2.cursor()
					sql2 = "SELECT user_id,name FROM `cp_users` WHERE company_id = %s"
					sql_where2 = session.get("company_id",None)
					cursor2.execute(sql2, sql_where2)
					row2 = cursor2.fetchall()
					session['returns'] = row2

					#sql3 = "SELECT * FROM `cp_rating` WHERE manager_id = %s"
					sql3 = "SELECT * FROM cp_rating LEFT JOIN cp_users ON cp_rating.employee_id = cp_users.user_id WHERE cp_rating.company_id = %s"
					sql_where2 = session.get("company_id",None)
					cursor2.execute(sql3, sql_where2)
					row3 = cursor2.fetchall()
					session['rating_returns'] = row3
					cursor2.close()
					conn2.close()
					session["m"] = len(row3)
					session["k"] = len(row2)
					return render_template('index.html', row2 = session.get('returns',None), k = session.get("k",None), row3 = session.get("rating_returns", None), m = session.get("m",None), admin = session.get("admin",None))
			else:
				flash('Invalid password!')
				return redirect('/')
		else:
			flash('Invalid email/password!')
			return redirect('/')

#creating right now

@app.route('/createuser')
def createuser():
	return render_template('createuser.html')

@app.route('/inputUser', methods=["POST"])
def newuser():
	_useremail = request.form['employee_email']
	_userpassword = request.form['employee_password']
	_username = request.form['employee_name']
	_usermangerid = request.form['manager_employee_id']
	#manager_id = session.get("id",None)
	company_id = session.get("company_id",None)
	created_at = datetime.date.today()
	user_id = str(uuid.uuid1())
	conn2 = mysql.connect()
	cursor2 = conn2.cursor()
	sql2 = "INSERT INTO `cp_users`(`user_id`, `email`, `password`, `name`, `company_id`, `manager_id`, `created_at`, `last_login_at`, `hierarchy_enum`, `photo_id`, `status`, `admin`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,'7','10','1','1')"
	sql_where2 = (user_id,_useremail,_userpassword,_username,company_id,_usermangerid,created_at,created_at)
	cursor2.execute(sql2, sql_where2)
	conn2.commit()
	conn2 = mysql.connect()
	cursor2 = conn2.cursor()
	sql2 = "SELECT user_id,name FROM `cp_users` WHERE company_id = %s"
	sql_where2 = session.get("company_id",None)
	cursor2.execute(sql2, sql_where2)
	row2 = cursor2.fetchall()
	session['returns'] = row2

	#sql3 = "SELECT * FROM `cp_rating` WHERE manager_id = %s"
	sql3 = "SELECT * FROM cp_rating LEFT JOIN cp_users ON cp_rating.employee_id = cp_users.user_id WHERE cp_rating.company_id = %s"
	cursor2.execute(sql3, sql_where2)
	row3 = cursor2.fetchall()
	session['rating_returns'] = row3
	session["m"] = len(row3)
	session["k"] = len(row2)
	cursor2.close()
	conn2.close()
	return render_template('index.html', row2 = session.get('returns',None), k = session.get("k",None), row3 = session.get("rating_returns", None), m = session.get("m",None))


@app.route('/logout')
def logout():
	session.pop('email', None)
	return redirect('/')

if __name__ == "__main__":
    app.secret_key = 'secret key'
    app.run()
