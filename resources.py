from dbm import dumb
from flask import jsonify,request,json,Response
from flask_restful import Resource
#from models import *
from .models import *
#from __init__ import db, bcrypt,mail
from . import db, bcrypt,mail
from flask_jwt_extended import create_access_token,jwt_required
from flask_mail import Message

from datetime import datetime

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
            print("debug1")
            nombre=request.json['nombre']
            apellido=request.json['apellido']
            email=request.json['email']
            clave=request.json['clave']
            print("debug 2")
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
        print("#################")

        email=request.json['email']
        clave=request.json['clave']
        print("DEBUG 1")

        if not email or not clave:
                return jsonify({'message':'Email or password mismatch'})
        print("DEBUG 2")
        user = Administradores.query.filter_by(email=email).first()
        print("DEBUG 3")
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
             "fechafin":concurso.fechafin
             }
             for concurso in admin.concursos ]
            admin = admin_schema.dump(admin)
            print("debug 4")
            message =  json.dumps({"administrador": admin,"concursos": concursos })
            print("debug 5")
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
        print("s debug 1")
        concursos= Concursos.query.all()
        print("debug 2")
        message = concs_schema.dump(concursos)
        print("debug 3")
        return jsonify({"concursos":message})

    def post(self):
        print(request.json)
        print("#############DEBUG VALORES: ")
        print(request.json['nombreConcurso'])
        print(request.json['url'])
        print(request.json['urlBanner'])
        print(request.json['precio'])
        print(request.json['guion'])
        print(request.json['recomendaciones'])
        print(request.json['fechaInicio'])
        print(request.json['fechaFinal'])
        print(request.json['admin_id'])
        print("###############fin valores")

        administrador_id = request.json['admin_id']

        nuevo_concurso=Concursos(
            nombre=request.json['nombreConcurso'],
            administrador_id = int(administrador_id),
            url=request.json['url'],
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
        print("DEBUG 2")
        administrador = Administradores.query.filter_by( id= int(administrador_id) ).first()
        print("DEBUG 3")
        administrador.concursos.append(nuevo_concurso)
        print("DEBUG 4")
        db.session.add(administrador)
        db.session.add(administrador)
        print("DEBUG 5")
        db.session.add(nuevo_concurso)
        print("DEBUG 6")
        db.session.commit()
        print("DEBUG 7")
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
            "fechacreacion": locutor.fechacreacion
        }
        for locutor in concurso.locutores
        ]

        message = json.dumps({"concurso": conc_schema.dump(concurso) ,"locutores": locutores})

        return Response(message,status=201,mimetype="application/json")

    def put(self, id_tblConcursos):
        
        concurso=Concursos.query.get_or_404(id_tblConcursos)

        for _,key in request.json:
            concurso[key] = request.json[key]

        db.session.add(concurso)
        db.session.commit()
        message =  json.dumps({"message": "Concurso Actualizado Exitosamente"})
        return Response(message, status=201, mimetype='application/json')




class RecursoListarLocutores(Resource):

    def get(self):

            locutores=Locutores.query.all()
            return locs_schema.dump(locutores)

    def post(self):

            concurso = Concursos.query.filter_by( id = int(request.json['id_concurso']) ).first()
            print("debug 1")
            locutor=Locutores(
                nombre=request.json['nombre'],
                apellido=request.json['apellido'],
                email=request.json['email'],
                observaciones=request.json['observaciones'],
                nombreArchivo=request.json['nombreArchivo'],
                extensionArchivo=request.json['extensionArchivo'],
                pathArchivo=request.json['pathArchivo'],
                tipoArchivo=request.json['tipoArchivo'],
            )
            print("debug 2")
            locutor.concursos.append(concurso)
            concurso.locutores.append(locutor)
            print("debug 3")
            db.session.add(locutor)
            db.session.add(concurso)
            db.session.commit()
            print("debug 4")

            return loc_schema.dump(locutor), 201
