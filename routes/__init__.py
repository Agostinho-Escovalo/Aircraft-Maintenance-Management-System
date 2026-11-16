from .aircraft import aircraft_bp
from .component import component_bp
from .maintenance import maintenance_bp
from .reports import reports_bp

def register_routes(app):
    app.register_blueprint(aircraft_bp, url_prefix='/aircraft')
    app.register_blueprint(component_bp, url_prefix='/component')
    app.register_blueprint(maintenance_bp, url_prefix='/maintenance')
    app.register_blueprint(reports_bp, url_prefix='/reports')