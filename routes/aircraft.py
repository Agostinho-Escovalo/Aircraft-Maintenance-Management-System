from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Aircraft, AircraftModel

aircraft_bp = Blueprint('aircraft', __name__)

@aircraft_bp.route('/')
def list_aircraft():
    # Базовый запрос с JOIN
    query = db.session.query(Aircraft, AircraftModel)\
        .join(AircraftModel, Aircraft.model_id == AircraftModel.model_id)

    # Фильтрация
    airline = request.args.get('airline', '').strip()
    manufacturer = request.args.get('manufacturer', '').strip()
    model_name = request.args.get('model_name', '').strip()
    min_hours = request.args.get('min_hours', type=float)
    max_hours = request.args.get('max_hours', type=float)

    if airline:
        query = query.filter(Aircraft.airline.ilike(f'%{airline}%'))
    if manufacturer:
        query = query.filter(AircraftModel.manufacturer.ilike(f'%{manufacturer}%'))
    if model_name:
        query = query.filter(AircraftModel.model_name.ilike(f'%{model_name}%'))
    if min_hours is not None:
        query = query.filter(Aircraft.total_flight_hours >= min_hours)
    if max_hours is not None:
        query = query.filter(Aircraft.total_flight_hours <= max_hours)

    # Сортировка
    sort_by = request.args.get('sort', 'aircraft_id')
    order = request.args.get('order', 'asc')
    sortable_fields = {
        'aircraft_id': Aircraft.aircraft_id,
        'registration': Aircraft.registration_number,
        'airline': Aircraft.airline,
        'hours': Aircraft.total_flight_hours,
        'cycles': Aircraft.total_cycles,
        'manufacturer': AircraftModel.manufacturer,
        'model': AircraftModel.model_name
    }

    if sort_by in sortable_fields:
        col = sortable_fields[sort_by]
        if order == 'desc':
            col = col.desc()
        query = query.order_by(col)
    else:
        query = query.order_by(Aircraft.aircraft_id)

    aircrafts_with_models = query.all()
    all_models = AircraftModel.query.all()

    return render_template(
        'aircraft/list.html',
        aircrafts_with_models=aircrafts_with_models,
        models=all_models,
        request_args=request.args
    )

@aircraft_bp.route('/create', methods=['GET', 'POST'])
def create_aircraft():
    # Оставляем как есть (уже реализовано)
    from models import AircraftModel
    if request.method == 'POST':
        aircraft = Aircraft(
            aircraft_id=request.form['aircraft_id'],
            model_id=int(request.form['model_id']),
            registration_number=request.form['registration_number'],
            production_date=request.form.get('production_date') or None,
            airline=request.form['airline'],
            total_flight_hours=float(request.form.get('total_flight_hours', 0)),
            total_cycles=int(request.form.get('total_cycles', 0))
        )
        db.session.add(aircraft)
        db.session.commit()
        return redirect(url_for('aircraft.list_aircraft'))

    models = AircraftModel.query.all()
    return render_template('aircraft/create.html', models=models)