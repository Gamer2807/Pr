from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime


db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='admin')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Equipment(db.Model):
    __tablename__ = 'equipment'

    id = db.Column(db.Integer, primary_key=True)
    inventory_number = db.Column(db.String(80), unique=True, nullable=False)
    device_name = db.Column(db.String(200), nullable=False)
    device_type = db.Column(db.String(50), nullable=False)
    brand = db.Column(db.String(100), nullable=True)
    model = db.Column(db.String(120), nullable=True)
    cpu = db.Column(db.String(120), nullable=True)
    ram = db.Column(db.String(50), nullable=True)
    storage = db.Column(db.String(50), nullable=True)
    serial_number = db.Column(db.String(120), unique=True, nullable=False)
    purchase_date = db.Column(db.Date, nullable=True)
    location = db.Column(db.String(120), nullable=True)
    responsible_employee = db.Column(db.String(120), nullable=True)
    status = db.Column(db.String(30), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Equipment {self.inventory_number}>'
