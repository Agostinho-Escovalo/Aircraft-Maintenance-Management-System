from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Numeric

db = SQLAlchemy()

class AircraftModel(db.Model):
    __tablename__ = 'aircraft_model'
    model_id = db.Column(db.Integer, primary_key=True)
    manufacturer = db.Column(db.String(50), nullable=False)
    model_name = db.Column(db.String(50), unique=True, nullable=False)
    certificate_type = db.Column(db.String(50))

class Aircraft(db.Model):
    __tablename__ = 'aircraft'
    aircraft_id = db.Column(db.String(15), primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey('aircraft_model.model_id'), nullable=False)
    registration_number = db.Column(db.String(15), unique=True, nullable=False)
    production_date = db.Column(db.Date)
    airline = db.Column(db.String(100), nullable=False)
    total_flight_hours = db.Column(db.Numeric(10, 1), default=0.0)
    total_cycles = db.Column(db.Integer, default=0)

    model = db.relationship('AircraftModel', backref='aircrafts')

class ComponentType(db.Model):
    __tablename__ = 'component_type'
    type_id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(50), unique=True, nullable=False)
    manufacturer = db.Column(db.String(50), nullable=False)

class Component(db.Model):
    __tablename__ = 'component'
    component_id = db.Column(db.Integer, primary_key=True)
    aircraft_id = db.Column(db.String(15), db.ForeignKey('aircraft.aircraft_id'), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('component_type.type_id'), nullable=False)
    serial_number = db.Column(db.String(50), unique=True, nullable=False)
    installation_date = db.Column(db.Date)
    current_hours = db.Column(db.Numeric(10, 1), default=0.0)
    current_cycles = db.Column(db.Integer, default=0)

    aircraft = db.relationship('Aircraft', backref='components')
    component_type = db.relationship('ComponentType', backref='components')

class WorkType(db.Model):
    __tablename__ = 'work_type'
    work_type_id = db.Column(db.Integer, primary_key=True)
    work_type_name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)

class WorkOrder(db.Model):
    __tablename__ = 'work_order'
    work_order_id = db.Column(db.Integer, primary_key=True)
    work_name = db.Column(db.String(100), nullable=False)
    work_type_id = db.Column(db.Integer, db.ForeignKey('work_type.work_type_id'), nullable=False)
    expected_duration_hours = db.Column(db.Numeric(10, 1))

    work_type = db.relationship('WorkType', backref='work_orders')

class MaintenanceHistory(db.Model):
    __tablename__ = 'maintenance_history'
    maintenance_id = db.Column(db.Integer, primary_key=True)
    aircraft_id = db.Column(db.String(15), db.ForeignKey('aircraft.aircraft_id', ondelete='SET NULL'))
    component_id = db.Column(db.Integer, db.ForeignKey('component.component_id', ondelete='SET NULL'))
    work_order_id = db.Column(db.Integer, db.ForeignKey('work_order.work_order_id'), nullable=False)
    maintenance_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(30), nullable=False)

    aircraft = db.relationship('Aircraft', backref='maintenance_records')
    component = db.relationship('Component', backref='maintenance_records')
    work_order = db.relationship('WorkOrder', backref='maintenance_records')

class Specialist(db.Model):
    __tablename__ = 'specialist'
    specialist_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    specialization = db.Column(db.String(100))

class SparePart(db.Model):
    __tablename__ = 'spare_part'
    part_id = db.Column(db.Integer, primary_key=True)
    part_number = db.Column(db.String(50), unique=True, nullable=False)
    manufacturer = db.Column(db.String(100))
    type_id = db.Column(db.Integer, db.ForeignKey('component_type.type_id', ondelete='SET NULL'))

    component_type = db.relationship('ComponentType', backref='spare_parts')

class WorkExecution(db.Model):
    __tablename__ = 'work_execution'
    execution_id = db.Column(db.Integer, primary_key=True)
    maintenance_id = db.Column(db.Integer, db.ForeignKey('maintenance_history.maintenance_id', ondelete='CASCADE'), nullable=False)
    specialist_id = db.Column(db.Integer, db.ForeignKey('specialist.specialist_id', ondelete='SET NULL'))
    part_id = db.Column(db.Integer, db.ForeignKey('spare_part.part_id', ondelete='SET NULL'))

    maintenance = db.relationship('MaintenanceHistory', backref='executions')
    specialist = db.relationship('Specialist', backref='executions')
    spare_part = db.relationship('SparePart', backref='executions')