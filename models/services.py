from db_config import db

class Services(db.Model):
    __tablename__ = "ajudelocal_services"
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.String(255), nullable=False)
    servicename = db.Column(db.String(50), nullable=False)

    def __init__(self, id_user, id_service):
        self.id_user = id_user
        self.servicename = get_service(id_service)

def get_service(i):
    switcher={                
                '1':'Cabelereiro',
                '2':'Manicure e Pedicure',
                '3':'Procedimentos Estéticos',
                '4':'Diarista',
                '5':'Dentista',
                '6':'Doações',
                '7': 'Outros Servicos'
            }
    return switcher.get(i,"Outros Servicos")

# class Services:
#     def __init__(self, id_user, servicename):        
#         self.id_user = id_user
#         self.servicename = servicename

#     def post_services(self, service, id):
#         conn = mysql.connect()
#         cursor = conn.cursor()
#         services_sql = "INSERT INTO `ajudelocal_services`(`id_user`, `servicename`) VALUES (%s,%s)"
#         for i in service:                                     
#             service_name = get_service(i)              
#             sql_services = (id, service_name)
#             cursor.execute(services_sql, sql_services)
#             conn.commit()
#         conn.close()