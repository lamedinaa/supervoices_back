from dbm import dumb
import numbers
from flask import jsonify,request,json,Response
from flask_restful import Resource
#from models import *
from .models import *
#from __init__ import db, bcrypt,mail
from . import db, bcrypt,mail
from flask_jwt_extended import create_access_token,jwt_required
from flask_mail import Message
from datetime import datetime
import os
from pathlib import Path

#directorio relativo
BASE_DIR = Path(__file__).resolve().parent.parent

#código para determinar los settings
path_settings = os.path.join(BASE_DIR,"settings/settings.json")
with open(path_settings) as json_file:
    data = json.load(json_file)


#RegistrarAdmins
class RecursoAgregarAdmins(Resource):

    def get(self):
        #def get_all_users(current_user):
         #   if not current_user.id:
          #      return jsonify({"error":"User not authenticated"}), 401
            administradores=Administradores.query.all()
            return admins_schema.dump(administradores)

    def post(self):
            print(request.json)
            
            nombre=request.json['nombre']
            apellido=request.json['apellido']
            email=request.json['email']
            clave=request.json['clave']
            
            admin_exists = Administradores.query.filter_by(email=email).first()
            
            if admin_exists:
                return jsonify({"error": "Usuario ya esta registrado"}, 409)

            hashed_clave=bcrypt.generate_password_hash(clave).decode('utf-8')

            #ENVIO DE CORREO
            # msg = Message("asunto", sender = 'lamedinaa@gmail.com', recipients = [f'{email}'])
            # msg.body = "body supervoices"
            # mail.send(msg)

            #ADIRIENDO ADMINISTRADOR
            nuevo_admin=Administradores(nombre=nombre, apellido=apellido, email=email,clave=hashed_clave)
            db.session.add(nuevo_admin)

            db.session.commit()
            message = json.dumps({"message": "usuario creado", "usuario": admin_schema.dump(nuevo_admin)})



            return Response(message, status=201, mimetype='application/json')

class RecursoLogin(Resource):
    def post(self):

        print(request.json)
    
        email=request.json['email']
        clave=request.json['clave']
        
        if not email or not clave:
                return jsonify({'message':'Email or password mismatch'})
        
        user = Administradores.query.filter_by(email=email).first()
        
        if user is None:
            print("debug 3.1")
            message = json.dumps({"message": "No Autorizado, el email no está registrado o es incorrecto", 'auth':'False'})
            return Response(message, status=401, mimetype='application/json')

        elif not bcrypt.check_password_hash(user.clave, clave):
            print("debug 3.2")
            message = json.dumps({"message": "No Autorizado, la contraseña es incorrecta", 'auth':'False'})
            return Response(message, status=401, mimetype='application/json')
        else:
            print("DEBUG 4 ")
            access_token=create_access_token(identity=email)
            print("DEBUG 5")
            return jsonify({'auth':'True', "access_token":access_token,"usuario_id":user.id})
            #return jsonify({'message': 'Autenticado exitosamente', 'auth':'True', "access_token":access_token,"usuario_id":user.id})



class RecursoUnAdmin(Resource):

    # @jwt_required()
    def post(self):   ##cambiar acá por una variable para obtener los concursos
            print("debug 1 ")
            id_Administradores = request.json["usuario_id"]
            print("debug 2")
            admin= Administradores.query.filter_by(id=id_Administradores).first()
            print("debug 3")
            concursos = [ {
             "id": concurso.id ,
             "nombre": concurso.nombre,
             "url": concurso.url,
             "valor":concurso.precio,
             "guion":concurso.guion,
             "recomendaciones":concurso.recomendaciones,
             "fechainicio":concurso.fechainicio,
             "fechafin":concurso.fechafin,
             "urlbanner": concurso.urlbanner
             }
             for concurso in admin.concursos ]
            admin = admin_schema.dump(admin)
            
            message =  json.dumps({"administrador": admin,"concursos": concursos })
            
            return Response(message, status=201, mimetype='application/json')


    def put(self, id_Administradores):

            admin=Administradores.query.get_or_404(id_Administradores)
            if 'nombre' in request.json:
                admin.nombre=request.json['nombre']
            if 'apellido' in request.json:
                admin.url=request.json['apellido']
            if 'email' in request.json:
                admin.valor=request.json['email']
            if 'clave' in request.json:
                admin.guion=request.json['clave']
            db.session.add(admin)
            db.session.commit()
            message =  json.dumps({"message": "Administrador Actualizado Exitosamente"})
            return Response(message, status=201, mimetype='application/json')






class RecursoListarConcursos(Resource):

    def get(self):
        #servicio para todos los concursos

        concursos= Concursos.query.all()
        message = concs_schema.dump(concursos)

        return jsonify({"concursos":message})

    def post(self):

        print(request.json)
        administrador_id = request.json['admin_id']

        nuevo_concurso=Concursos(
            nombre=request.json['nombreConcurso'],
            administrador_id = int(administrador_id),
            urlbanner = request.json['urlBanner'],
            precio=request.json['precio'],
            guion=request.json['guion'],
            recomendaciones=request.json['recomendaciones'],
            #fechainicio= datetime.strptime(request.json['fechaInicio'],"%Y-%m-%dT%H:%M:%S.%fZ"),
            fechainicio= datetime.strptime(request.json['fechaInicio'],"%Y-%m-%dT%H:%M"),
            #fechafin= datetime.strptime(request.json['fechaFinal'],"%Y-%m-%dT%H:%M:%S.%fZ"),
            fechafin= datetime.strptime(request.json['fechaFinal'],"%Y-%m-%dT%H:%M"),
            fechacreacion=datetime.utcnow()
        )
        
        print("debug 1 ")


        administrador = Administradores.query.filter_by( id= int(administrador_id) ).first()
        administrador.concursos.append(nuevo_concurso)
        db.session.add(administrador)
        db.session.add(administrador)
        db.session.add(nuevo_concurso)
        db.session.commit()
        print("debug 1.2 ")

        url_concurso = data["URL_SUPERVOICES"] + request.json['nombreConcurso'].replace(" ","") + "/" + str(nuevo_concurso.id)
        url_concursobanner = request.json['nombreConcurso'].replace(" ","") + "/" + str(nuevo_concurso.id)
        print("url_concurso: {0}" + url_concurso)
        print("url_banner: {0}".format(url_concursobanner))
        nuevo_concurso.url = url_concurso
        nuevo_concurso.urlbanner = url_concursobanner 
        db.session.commit()
        print("debug 1.3 ")

        message = json.dumps({"message": "concurso creado"})

        return Response(message, status=201, mimetype='application/json')





class RecursoUnConcurso(Resource):

    def get(self,id_tblConcursos):

        concurso=Concursos.query.get_or_404(id_tblConcursos)

        locutores = [{
            "nombre": locutor.nombre,
            "apellido": locutor.apellido,
            "email": locutor.email,
            "observaciones": locutor.observaciones,
            "nombreArchivo": locutor.nombreArchivo,
            "extensionArchivo": locutor.extensionArchivo,
            "pathArchivo": locutor.pathArchivo,
            "tipoArchivo": locutor.tipoArchivo,
            "fechacreacion": locutor.fechacreacion,
            "convertido": locutor.convertido
        }
        for locutor in concurso.locutores
        ]

        message = json.dumps({"concurso": conc_schema.dump(concurso) ,"locutores": locutores})

        return Response(message,status=201,mimetype="application/json")


    def put(self, id_tblConcursos):
        
        concurso=Concursos.query.get_or_404(id_tblConcursos)
        print(request.json)
        for key in request.json.keys():
            concurso.key = request.json[key] if request.json[key] else ""

        concurso.nombre = request.json["nombre"] if request.json["nombre"] else ""
        db.session.commit()

        message =  json.dumps({"message": "Concurso Actualizado Exitosamente"})

        return Response(message, status=201, mimetype='application/json')


    def delete(self,id_tblConcursos):

        concurso=Concursos.query.get_or_404(id_tblConcursos)
        message =  json.dumps({"message": "Concurso Actualizado Exitosamente"})


        return Response(message, status=201, mimetype='application/json')



class RecursoListarLocutores(Resource):

    def get(self):

            locutores=Locutores.query.all()
            return locs_schema.dump(locutores)

    def post(self):
            print(request.files)
            print(request.form)
            form = request.form
            file = request.files
            ALLOWED_EXTENSIONS = {'wav','mp3','mp4','ogg'}
            if 'file' not in request.files:
                return {"message":"no existe archivo"}
            filename = file['file'].filename

            if file['file'] and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS:

                concurso = Concursos.query.filter_by( id = int(request.form['id_concurso']) ).first()

                locutor=Locutores(
                    nombre=request.form['nombre'],
                    apellido=request.form['apellido'],
                    email=request.form['email'],
                    observaciones=request.form['observaciones']
                )

                locutor.concursos.append(concurso)
                concurso.locutores.append(locutor)
                db.session.commit()

                print("id_locutor: {0} ".format(locutor.id))
                filename = "{0}{1}_{2}".format(request.form['id_concurso'],locutor.id,filename)
                print("filename: {0}".format(filename))
                locutor.nombreArchivo = filename

                db.session.commit()
                
                print("commit 1 ")
                
                guardar_archivo = os.path.join(data["UPLOAD_FOLDER"], filename)
                print("guardando archivo: {0}".format(guardar_archivo))
                file['file'].save(guardar_archivo)
                print("archivo guardado")

                message =  json.dumps({"message": "Audio subido Exitosamente"})
                return Response(message, status=201, mimetype='application/json')

            message =  json.dumps({"message": "Fallo al subir el archivo"})
            return Response(message, status=500, mimetype='application/json')



class RecursoConsultaConcurso(Resource):

    def post(self):
        
        print(request.json)

        concurso = Concursos.query.filter_by( id = int(request.json['id_concurso']) ).first()
        print(concurso)
        print("debug 1.0")
        if concurso is None:
            message =  json.dumps({"message": "No existe concurso","concurso":"false"})
            return Response(message, status=201, mimetype='application/json')            

        print("debug 1")
        if request.json["nombre"] != concurso.nombre.replace(" ",""):
            print("No existe concurso con es nombre")
            message =  json.dumps({"message": "No existe el nombre concurso","concurso":"false"})
            return Response(message, status=201, mimetype='application/json')


        message =  json.dumps({"message": "Existe concurso","concurso":"true"})
        return Response(message, status=201, mimetype='application/json')
