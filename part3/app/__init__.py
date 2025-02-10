from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt  # ✅ Import Bcrypt for password hashing
from config import DevelopmentConfig

# ✅ Initialize extensions (but don't tie them to the app yet)
jwt = JWTManager()
db = SQLAlchemy()
bcrypt = Bcrypt()  # ✅ Add bcrypt instance

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)

    # ✅ Load configuration from the provided config class
    app.config.from_object(config_class)

    # ✅ Initialize extensions with the app
    jwt.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)  # ✅ Initialize bcrypt

    # ✅ Ensure tables are created within the app context
    with app.app_context():
        db.create_all()  # ✅ Creates tables only if they don't exist

    # ✅ Import API namespaces **AFTER** initializing db to avoid circular imports
    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.auth import api as auth_ns
    from app.api.v1.protected import api as protected_ns

    # ✅ Create API instance and register namespaces
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(protected_ns, path='/api/v1/protected')

    return app