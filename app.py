from flask import Flask
from flask.helpers import send_from_directory
from flask_restful import Api
from itsdangerous import base64_decode
#from resources import RecursoAgregarAdmins,RecursoListarLocutores,RecursoLogin,RecursoListarConcursos,RecursoUnConcurso,RecursoUnAdmin
from .resources import RecursoAgregarAdmins,RecursoListarLocutores,RecursoLogin,RecursoListarConcursos,RecursoUnConcurso,RecursoUnAdmin,RecursoConsultaConcurso
from . import  db,ma,bcrypt,mail
from flask_mail import Message
from pathlib import Path
import os
import json
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager


#directorio relativo
BASE_DIR = Path(__file__).resolve().parent.parent

#código para determinar los settings
path_settings = os.path.join(BASE_DIR,"settings/settings.json")
with open(path_settings) as json_file:
    data = json.load(json_file)

#instancia app
#app = Flask(__name__)
#instancia app con react deploy
app = Flask(__name__,static_folder="build",static_url_path='')

#configuraciones app
app.config['SECRET_KEY'] = data['SECRET_KEY']
app.config["JWT_SECRET_KEY"] = data["JWT_SECRET_KEY"]
app.config['SQLALCHEMY_DATABASE_URI'] = data['SQLALCHEMY_DATABASE_URI']

##configuraciones email
app.config['MAIL_SERVER']= data['MAIL_SERVER']

app.config['MAIL_PORT'] = data['MAIL_PORT']
app.config['MAIL_USERNAME'] = data['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = data['MAIL_PASSWORD']
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = data['MAIL_USE_SSL']

db.init_app(app)
ma.init_app(app)
bcrypt.init_app(app)
mail.init_app(app)
jwt = JWTManager(app)

CORS(app)

@app.route('/')
@cross_origin()
def index():
    # return "hola mundo"
    print("base dir {0}".format(BASE_DIR))
    print("raiz del proyecto")
    return send_from_directory(app.static_folder,"index.html")

# @app.route('/')
# def index():
#         return app.send_static_file('index.html')



##TESTEO DE ENVIO DE CORREO PRUEBA
@app.route("/enviocorreo")
def enviocorreo():
    email = "lamedinaa@gmail.com"
    msg = Message("asunto", sender = 'lamedinaa@gmail.com', recipients = [f'{email}'])
    msg.body = "body supervoices"
    mail.send(msg)
    return "envio de correo correcto"

api=Api(app)

api.add_resource(RecursoLogin,'/api/login')
api.add_resource(RecursoAgregarAdmins,'/api/registrarAdmin')
api.add_resource(RecursoUnAdmin,'/api/admin')
api.add_resource(RecursoListarConcursos,'/api/registrarConcursos')
api.add_resource(RecursoUnConcurso,'/api/registrarconcursos/<int:id_tblConcursos>')
api.add_resource(RecursoListarLocutores,'/api/locutores')
api.add_resource(RecursoConsultaConcurso,'/api/consultaconcurso')



if __name__ == '__main__':

    app.run(debug=True)