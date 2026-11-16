from flask import Blueprint, render_template, request, redirect, url_for
from models import db, MaintenanceHistory, Aircraft, Component, WorkOrder, WorkType

maintenance_bp = Blueprint('maintenance', __name__)

@maintenance_bp.route('/')
def list_maintenance():
    query = db.session.query(
        MaintenanceHistory,
        Aircraft,
        Component,
        WorkOrder,
        WorkType
    ).join(Aircraft, MaintenanceHistory.aircraft_id == Aircraft.aircraft_id)\
     .join(WorkOrder, MaintenanceHistory.work_order_id == WorkOrder.work_order_id)\
     .join(WorkType, WorkOrder.work_type_id == WorkType.work_type_id)\
     .outerjoin(Component, MaintenanceHistory.component_id == Component.component_id)

    # Фильтрация
    status = request.args.get('status', '').strip()
    airline = request.args.get('airline', '').strip()
    work_type_name = request.args.get('work_type', '').strip()

    if status:
        query = query.filter(MaintenanceHistory.status == status)
    if airline:
        query = query.filter(Aircraft.airline.ilike(f'%{airline}%'))
    if work_type_name:
        query = query.filter(WorkType.work_type_name.ilike(f'%{work_type_name}%'))

    # Сортировка
    sort_by = request.args.get('sort', 'date')
    order = request.args.get('order', 'desc')
    sortable = {
        'date': MaintenanceHistory.maintenance_date,
        'aircraft': Aircraft.registration_number,
        'work': WorkOrder.work_name,
        'component': Component.serial_number,
        'status': MaintenanceHistory.status
    }
    col = sortable.get(sort_by, MaintenanceHistory.maintenance_date)
    if order == 'desc':
        col = col.desc()
    query = query.order_by(col)

    records = query.all()
    return render_template('maintenance/list.html', records=records, request_args=request.args)

@maintenance_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_maintenance(id):
    # Оставляем как есть
    from models import MaintenanceHistory
    record = MaintenanceHistory.query.get_or_404(id)
    if request.method == 'POST':
        record.status = request.form['status']
        db.session.commit()
        return redirect(url_for('maintenance.list_maintenance'))
    return render_template('maintenance/edit.html', record=record)

@maintenance_bp.route('/delete/<int:id>', methods=['POST'])
def delete_maintenance(id):
    from models import MaintenanceHistory
    record = MaintenanceHistory.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    return redirect(url_for('maintenance.list_maintenance'))