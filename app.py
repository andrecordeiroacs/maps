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
# cache.init_app(app)u
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

@app.route('/thankyou')
def form_thankyou():
        voluntary_id = manager_id = session.get("voluntary_id",None)
        #Pegando as informacoes

        conn = mysql.connect()
        cursor = conn.cursor()
        user_sql = "SELECT `city`, `services`, `bairro` FROM `ajudelocal_voluntary` WHERE `id` = %s"
        cursor.execute(user_sql, voluntary_id)
        row = cursor.fetchall()
        conn.commit()

        user_sql2 = "SELECT * FROM `ajudelocal_server` WHERE `city` = %s ORDER BY `created_at` DESC"
        cursor.execute(user_sql2, row[0][0])
        row2 = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        #print(row)
        #print(row2)
        
        rows =  len(row2)
        #match perfeito
        i=0
        match = 0
        other_service_same_neighbor = 0
        same_city_and_service = 0
        same_city_other_service = 0
        match_list = []
        other_service_same_neighbor_list = []
        same_city_and_service_list = []
        same_city_other_service_list = []
        same_city = 0

        if(len(row2)>0):
            same_city = 1
            for i in range(rows):
                #checa mesmo bairro
                if(row2[i][9] == row[0][2]):
                    #checa mesmo bairro e  servico
                    if(row[0][1] in row2[i][6]):
                        match_list.append(row2[i])
                        match += 1
                    #mesmo bairro, prem outro servico
                    else:
                        other_service_same_neighbor_list.append(row2[i])
                        other_service_same_neighbor += 1
                else:
                    #checa mesma cidade e mesmo servico
                    if(row[0][1] in row2[i][6]):
                        same_city_and_service_list.append(row2[i])
                        same_city_and_service += 1
                    #mesma cidade e outro servico
                    else:
                        same_city_other_service_list.append(row2[i])
                        same_city_other_service += 1
        else:
            same_city = 0
        #print("Match Perfeito")
        #print(match_list)

        #print("Na sua Cidade")
        #print(same_city_and_service_list)

        #print("No seu bairro")
        #print(other_service_same_neighbor)

        #print("Na sua cidade outro servico")
        #print(same_city_other_service_list)
        return render_template('thankyou.html', same_city = same_city, match = match, match_list = match_list, same_city_and_service = same_city_and_service, same_city_and_service_list = same_city_and_service_list, other_service_same_neighbor = other_service_same_neighbor, other_service_same_neighbor_list = other_service_same_neighbor_list, same_city_other_service = same_city_other_service, same_city_other_service_list = same_city_other_service_list)

@app.route('/submit_voluntary', methods=['POST'])
def form_submit():
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _phone = request.form['inputPhone']
        _city = request.form['cidade']
	_cep = request.form['cep']
        _bairro = request.form['bairro']
        _estado = request.form['estado']
        _services = str(request.form.getlist('checkbox'))
        _comments = request.form['inputComments']
        #flash('Obrigado! Em breve entraremos em contato com voce!')
        #print("Olha leeee3")
        #print(_services)
        lead_id = str(uuid.uuid1())

        #escrevendo no banco
        conn = mysql.connect()
        cursor = conn.cursor()
        user_sql = "INSERT INTO `ajudelocal_voluntary`(`id`, `name`, `email`, `phone`, `city`, `services`, `comments`, `cep`, `bairro`, `estado`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        sql_where = (lead_id, _name, _email, _phone, _city, _services, _comments, _cep, _bairro, _estado)
        cursor.execute(user_sql, sql_where)
        row = cursor.fetchall()
        conn.commit()
        user_sql2 = "SELECT * FROM `ajudelocal_server` WHERE `city` = %s ORDER BY `created_at` DESC LIMIT 1"
        cursor.execute(user_sql2, _city)
        row2 = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        if (len(row2) > 0):
            message = Mail(
            from_email='ajudelocal@gmail.com',
            to_emails=_email
            )

            message.template_id = 'd-641a0020a8174bb5ad817e67dc7b9dac'
            message.dynamic_template_data = {'Sender_Name': row2[0][2], 'Sender_City': row2[0][5], 'Sender_Email': row2[0][3] , 'Sender_Zip': row2[0][4] }
            try:
                sg = SendGridAPIClient("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")
                response = sg.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                print(e)
                print("Deu Ruim")
        else:
            message = Mail(
            from_email='ajudelocal@gmail.com',
            to_emails=_email
            )

            message.template_id = 'd-9b18a6dffbc948e3bd83622a7f2eb5f1'
            try:
                sg = SendGridAPIClient("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")
                response = sg.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                print(e)
                print("Deu Ruim sem custom")
        session['voluntary_id'] = lead_id
        return redirect('/thankyou')

@app.route('/submit_server', methods=['POST'])
def form_submit_server():
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _phone = request.form['inputPhone']
        _city = request.form['cidade']
	_cep = request.form['cep']
        _bairro = request.form['bairro']
        _estado = request.form['estado']
        _services = str(request.form.getlist('checkbox'))
        _comments = request.form['inputComments']
        flash('Obrigado! Em breve entraremos em contato com voce!')
        print("Olha leeee2")
        print(_services)
        lead_id = str(uuid.uuid1())

        #escrevendo no banco
        conn = mysql.connect()
        cursor = conn.cursor()
        user_sql = "INSERT INTO `ajudelocal_server`(`id`, `name`, `email`, `phone`, `city`, `services`, `comments`, `cep`, `bairro`, `estado`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        sql_where = (lead_id, _name, _email, _phone, _city, _services, _comments, _cep, _bairro, _estado)
        cursor.execute(user_sql, sql_where)
        row = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()

        message = Mail(
              from_email='ajudelocal@gmail.com',
              to_emails=_email
              )

        message.template_id = 'd-b97119cd37ea4490b5b2a7870cbb81f3'
        try:
              sg = SendGridAPIClient("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")
              response = sg.send(message)
              print(response.status_code)
              print(response.body)
              print(response.headers)
        except Exception as e:
              print(e)
              print("Deu Ruim")
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
