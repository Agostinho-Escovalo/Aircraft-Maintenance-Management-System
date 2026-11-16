from flask import Blueprint, render_template, request, make_response
import csv
from io import StringIO
from sqlalchemy import func
from models import db, MaintenanceHistory, Aircraft, WorkOrder, Component, Specialist, WorkExecution, ComponentType

reports_bp = Blueprint('reports', __name__)


# === Существующий отчёт по обслуживанию ===
@reports_bp.route('/maintenance_history')
def maintenance_history():
    aircraft_id = request.args.get('aircraft_id')
    records = MaintenanceHistory.query
    if aircraft_id:
        records = records.filter_by(aircraft_id=aircraft_id)
    records = records.order_by(MaintenanceHistory.maintenance_date.desc()).all()
    aircrafts = Aircraft.query.all()
    return render_template('reports/maintenance_history.html', records=records, aircrafts=aircrafts,
                           selected=aircraft_id)


@reports_bp.route('/maintenance_history/export')
def export_maintenance_csv():
    aircraft_id = request.args.get('aircraft_id')
    records = MaintenanceHistory.query
    if aircraft_id:
        records = records.filter_by(aircraft_id=aircraft_id)
    records = records.order_by(MaintenanceHistory.maintenance_date.desc()).all()

    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['Дата', 'Самолёт', 'Работа', 'Компонент', 'Статус', 'Исполнители', 'Запчасти'])

    for r in records:
        execs = WorkExecution.query.filter_by(maintenance_id=r.maintenance_id).all()
        specialists = '; '.join([f"{e.specialist.first_name} {e.specialist.last_name}" for e in execs if e.specialist])
        parts = '; '.join([e.spare_part.part_number for e in execs if e.spare_part])

        cw.writerow([
            r.maintenance_date,
            r.aircraft.registration_number if r.aircraft else '',
            r.work_order.work_name if r.work_order else '',
            r.component.serial_number if r.component else '',
            r.status,
            specialists,
            parts
        ])

    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=maintenance_report.csv"
    output.headers["Content-type"] = "text/csv"
    return output


# === НОВОЕ: Статистика ===
@reports_bp.route('/stats')
def stats():
    # Агрегаты
    total_aircraft = db.session.query(func.count(Aircraft.aircraft_id)).scalar()
    total_components = db.session.query(func.count(Component.component_id)).scalar()
    total_maintenance = db.session.query(func.count(MaintenanceHistory.maintenance_id)).scalar()

    # Самый налёченный самолёт
    max_hours_aircraft = db.session.query(
        Aircraft.registration_number,
        Aircraft.total_flight_hours
    ).order_by(Aircraft.total_flight_hours.desc()).first()

    # Самый используемый тип компонента
    top_component_type = db.session.query(
        ComponentType.type_name,
        func.count(Component.component_id).label('cnt')
    ).join(Component, Component.type_id == ComponentType.type_id) \
        .group_by(ComponentType.type_id, ComponentType.type_name) \
        .order_by(func.count(Component.component_id).desc()) \
        .first()

    # Количество работ по статусам
    status_counts = db.session.query(
        MaintenanceHistory.status,
        func.count(MaintenanceHistory.maintenance_id)
    ).group_by(MaintenanceHistory.status).all()

    return render_template('stats.html',
                           total_aircraft=total_aircraft,
                           total_components=total_components,
                           total_maintenance=total_maintenance,
                           max_hours_aircraft=max_hours_aircraft,
                           top_component_type=top_component_type,
                           status_counts=status_counts
                           )