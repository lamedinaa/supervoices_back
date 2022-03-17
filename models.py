from linecache import lazycache
#from __init__ import db , ma
from . import db , ma
from datetime import datetime
from marshmallow import fields

class Administradores(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(50),nullable=False)
    apellido=db.Column(db.String(50),nullable=False)
    email=db.Column(db.String(50), nullable=False, unique=True)
    clave=db.Column(db.String(200), nullable=False)
    concursos = db.relationship('Concursos',backref='administradores', lazy='dynamic')


concursos_locutores = db.Table('concursos_locutores',
    db.Column('concurso_id',db.Integer,db.ForeignKey('concursos.id')),
    db.Column('locutor_id',db.Integer,db.ForeignKey('locutores.id'))
)

class Concursos(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(255))
    administrador_id = db.Column(db.Integer,db.ForeignKey('administradores.id'))
    locutores = db.relationship('Locutores',secondary=concursos_locutores)
    url=db.Column(db.String(200), unique=True)
    urlbanner= db.Column(db.String(200))
    precio=db.Column(db.Numeric(10,2))
    guion=db.Column(db.Text)
    recomendaciones=db.Column(db.Text)
    fechainicio=db.Column(db.DateTime)
    fechafin=db.Column(db.DateTime)
    fechacreacion=db.Column(db.DateTime,default=datetime.now)


class Locutores(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(50))
    apellido=db.Column(db.String(50))
    email=db.Column(db.String(50))
    observaciones=db.Column(db.Text)
    nombreArchivo=db.Column(db.String(50))
    extensionArchivo=db.Column(db.String(50))
    pathArchivo=db.Column(db.String(50))
    tipoArchivo=db.Column(db.String(50))
    fechacreacion=db.Column(db.DateTime,default=datetime.now)
    concursos = db.relationship('Concursos',secondary=concursos_locutores)


class Administradores_Schema(ma.Schema):
    class Meta:
        fields=('id','nombre','apellido','email','clave')
admin_schema=Administradores_Schema()
admins_schema=Administradores_Schema(many=True)

class Concursos_Schema(ma.Schema):
    class Meta:
        fields=('id','nombre','url','urlbanner','precio','guion','recomendaciones','fechainicio','fechafin','fechacreacion')

conc_schema=Concursos_Schema()
concs_schema=Concursos_Schema(many=True)

class Locutores_Schema(ma.Schema):
    class Meta:
        fields=('id', 'id_concurso','nombre','apellido','email','observaciones','nombreArchivo','extensionArchivo','pathArchivo','tipoArchivo','fechacreacion')
loc_schema=Locutores_Schema()
locs_schema=Locutores_Schema(many=True)