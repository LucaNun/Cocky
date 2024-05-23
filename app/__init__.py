from flask import Flask

from config import Config
from app.extensions import mysql

def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)
    
    # Extentions
    mysql.init_app(app)
    
    # Blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp, url_prefix="/")

    @app.route('/r')
    def test_page():
        return ['%s' % rule for rule in app.url_map.iter_rules()]

    return app
