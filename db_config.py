from main import app
from flaskext.mysql import MySQL

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'u488708247_riscc'
app.config['MYSQL_DATABASE_PASSWORD'] = 'xVTDch9X3Ugd'
app.config['MYSQL_DATABASE_DB'] = 'u488708247_riscc'
app.config['MYSQL_DATABASE_HOST'] = 'sql156.main-hosting.eu'
mysql.init_app(app)
