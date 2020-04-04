import io
from flask import Flask, render_template, redirect, url_for, make_response
from flask import jsonify
from flask import request
from db_config import *
from flask import flash, session, render_template, request, redirect
import uuid
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
import ast
from models.match_users import *
from models.services import Services
from models.voluntary import Voluntary
from models.server import Server

# cache = Cache(config={'CACHE_TYPE': 'simple'})
#app = Flask(__name__)
# cache.init_app(app)u
#app.secret_key = "secret key"

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
        voluntary_id = session.get("voluntary_id",None)        
        
        voluntary = Voluntary.query.filter_by(id_user=voluntary_id).first()
        server = Server.query.filter_by(city=voluntary.city).all()
        serviceVoluntary = Services.query.with_entities(Services.servicename).filter_by(id_user = voluntary_id).all()        

        #list_servicesVoluntary = value for value in serviceVoluntary
        
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
        
        same_city = 0
        for i in server:
            #atribui servico
            serviceServer = Services.query.with_entities(Services.servicename).filter_by(id_user=i.id_user).all()
            
            if (len(serviceServer) == 0):
                continue

            user_obj = Match_Users(i.name, serviceServer, i.phone, i.email)           

            #checa mesmo bairro
            bairroServer = i.bairro
            bairroVoluntary = voluntary.bairro
            if(bairroServer == bairroVoluntary):
                #checa mesmo bairro e  servico
                if(any(check in serviceServer for check in serviceVoluntary)):
                    match_list.append(user_obj)
                    match += 1
                #mesmo bairro, prem outro servico
                else:
                    other_service_same_neighbor_list.append(user_obj)
                    other_service_same_neighbor += 1
            else:
                #checa mesma cidade e mesmo servico                    
                if(any(check in serviceServer for check in serviceVoluntary)):
                    same_city_and_service_list.append(user_obj)
                    same_city_and_service += 1
                #mesma cidade e outro servico
                else:
                    same_city_other_service_list.append(user_obj)
                    same_city_other_service += 1   
            same_city = 1
           
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
        _listServices = ast.literal_eval(_services)       
        _comments = request.form['inputComments']        
        lead_id = str(uuid.uuid1())
        voluntary = Voluntary(lead_id, datetime.now(), _name, _email, _phone, _city, _services, _comments, _cep, _bairro, _estado)
        db.session.add(voluntary)
        
        for i in _listServices:                                    
            service = Services(lead_id, i)
            db.session.add(service)                
        db.session.commit()  
        server_services = Server.query.filter_by(city=_city).first()
        
        if (server_services.name != ""):
            message = Mail(
            from_email='ajudelocal@gmail.com',
            to_emails=_email
            )

            message.template_id = 'd-641a0020a8174bb5ad817e67dc7b9dac'
            message.dynamic_template_data = {'Sender_Name': server_services.name, 'Sender_City': server_services.city,
            'Sender_Email': server_services.email , 'Sender_Zip': server_services.cep }
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
        _listServices = ast.literal_eval(_services)
        _comments = request.form['inputComments']
        lead_id = str(uuid.uuid1())      
        server = Server(lead_id, datetime.now(), _name, _email, _phone, _city, _services, _comments, _cep, _bairro, _estado)
        db.session.add(server)
        
        for i in _listServices:                                    
            service = Services(lead_id, i)
            db.session.add(service)                
        db.session.commit()  
        
        
        flash('Obrigado! Em breve entraremos em contato com voce!')
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
