from main import app
from flask_sqlalchemy import SQLAlchemy

# MySQL configurations
# app.config['MYSQL_DATABASE_USER'] = 'u488708247_riscc'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'xVTDch9X3Ugd'
# app.config['MYSQL_DATABASE_DB'] = 'u488708247_riscc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://u488708247_riscc:xVTDch9X3Ugd@sql156.main-hosting.eu/u488708247_riscc'
db = SQLAlchemy(app)    
    