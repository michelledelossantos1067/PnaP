from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'di_nani_secreta_dls_dls'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///productos.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    from app.routes import main
    app.register_blueprint(main)
    
    from app.commands import init_db
    app.cli.add_command(init_db)
    
    return app