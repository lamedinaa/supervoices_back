from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_mail import Mail


bcrypt = Bcrypt()
db = SQLAlchemy()
ma=Marshmallow()
bcrypt = Bcrypt()
mail= Mail()
