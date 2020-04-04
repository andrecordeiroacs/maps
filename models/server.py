from db_config import db

class Server(db.Model):
    __tablename__ = "ajudelocal_server"
    id = db.Column(db.Integer, primary_key=True)   
    id_user = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.TIMESTAMP(), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    services = db.Column(db.String(255), nullable=False)
    comments = db.Column(db.String(255), nullable=False)
    cep = db.Column(db.String(255), nullable=False)
    bairro = db.Column(db.String(255), nullable=False)
    estado = db.Column(db.String(255), nullable=False)

    def __init__(self, id_user, created_at, name, email, phone, city, services, comments, cep, bairro, estado):
        self.id_user = id_user
        self.created_at = created_at
        self.name = name
        self.email = email
        self.phone = phone
        self.city = city
        self.services = services
        self.comments = comments
        self.cep = cep
        self.bairro = bairro
        self.estado = estado   