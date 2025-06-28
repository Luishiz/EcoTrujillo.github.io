import os
import logging
from flask import Flask
from flask_login import LoginManager
from werkzeug.middleware.proxy_fix import ProxyFix

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "eco-trujillo-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'

# In-memory storage
users_db = {}
activities_db = []
challenges_db = [
    {
        'id': 1,
        'name': 'Reto Reciclaje Semanal',
        'description': 'Recicla al menos 5 kg de materiales esta semana',
        'points': 100,
        'type': 'weekly',
        'target': 5,
        'unit': 'kg'
    },
    {
        'id': 2,
        'name': 'Transporte Eco',
        'description': 'Usa transporte sostenible por 7 días consecutivos',
        'points': 150,
        'type': 'weekly',
        'target': 7,
        'unit': 'días'
    },
    {
        'id': 3,
        'name': 'Limpieza Comunitaria',
        'description': 'Participa en una jornada de limpieza',
        'points': 200,
        'type': 'weekly',
        'target': 1,
        'unit': 'evento'
    }
]

rewards_db = [
    {
        'id': 1,
        'name': 'Descuento 20% - Café Ecológico',
        'description': 'Descuento en café orgánico local',
        'points_required': 500,
        'partner': 'Café Verde Trujillo',
        'category': 'alimentación'
    },
    {
        'id': 2,
        'name': 'Entrada gratis - Museo Arqueológico',
        'description': 'Entrada gratuita al museo',
        'points_required': 300,
        'partner': 'Museo de Arqueología',
        'category': 'cultura'
    },
    {
        'id': 3,
        'name': 'Kit de Plantas Nativas',
        'description': 'Kit con 3 plantas nativas de la región',
        'points_required': 800,
        'partner': 'Vivero EcoTrujillo',
        'category': 'jardinería'
    }
]

# Trujillo ecological points
ecological_points = [
    {
        'id': 1,
        'name': 'Parque El Recreo',
        'lat': -8.1116,
        'lng': -79.0287,
        'type': 'parque',
        'description': 'Parque ecológico con áreas verdes'
    },
    {
        'id': 2,
        'name': 'Malecón de Huanchaco',
        'lat': -8.0833,
        'lng': -79.1167,
        'type': 'playa',
        'description': 'Área costera con biodiversidad marina'
    },
    {
        'id': 3,
        'name': 'Centro de Reciclaje Municipal',
        'lat': -8.1085,
        'lng': -79.0215,
        'type': 'reciclaje',
        'description': 'Centro de acopio de materiales reciclables'
    },
    {
        'id': 4,
        'name': 'Jardín Botánico UNT',
        'lat': -8.1015,
        'lng': -79.0445,
        'type': 'jardin',
        'description': 'Jardín botánico de la Universidad Nacional'
    },
    {
        'id': 5,
        'name': 'Humedales de Villa María',
        'lat': -8.0950,
        'lng': -79.0150,
        'type': 'humedal',
        'description': 'Ecosistema de humedales urbanos'
    }
]

from models import User

@login_manager.user_loader
def load_user(user_id):
    return users_db.get(int(user_id))

# Import routes after app creation
from routes import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
