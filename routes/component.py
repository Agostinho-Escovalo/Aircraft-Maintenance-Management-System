from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Component, Aircraft, ComponentType

component_bp = Blueprint('component', __name__)


@component_bp.route('/create', methods=['GET', 'POST'])
def create_component():
    if request.method == 'POST':
        comp = Component(
            aircraft_id=request.form['aircraft_id'],
            type_id=int(request.form['type_id']),
            serial_number=request.form['serial_number'],
            installation_date=request.form.get('installation_date') or None,
            current_hours=float(request.form.get('current_hours', 0)),
            current_cycles=int(request.form.get('current_cycles', 0))
        )
        db.session.add(comp)
        db.session.commit()
        return redirect(url_for('maintenance.list_maintenance'))

    aircrafts = Aircraft.query.all()
    types = ComponentType.query.all()
    return render_template('component/create.html', aircrafts=aircrafts, types=types)