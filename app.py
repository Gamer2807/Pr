from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from models import db, User, Equipment
from sqlalchemy import func

app = Flask(__name__)
app.config['SECRET_KEY'] = 'replace-this-with-a-secure-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Login successful.', 'success')
            return redirect(url_for('dashboard'))

        flash('Invalid username or password.', 'danger')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/')
@app.route('/dashboard')
@login_required
def dashboard():
    total_devices = Equipment.query.count()
    computers = Equipment.query.filter_by(device_type='Computer').count()
    laptops = Equipment.query.filter_by(device_type='Laptop').count()
    printers = Equipment.query.filter_by(device_type='Printer').count()
    under_repair = Equipment.query.filter_by(status='Repair').count()
    working_count = Equipment.query.filter_by(status='Working').count()

    type_counts = db.session.query(Equipment.device_type, func.count(Equipment.id)).group_by(Equipment.device_type).all()
    status_counts = db.session.query(Equipment.status, func.count(Equipment.id)).group_by(Equipment.status).all()

    return render_template(
        'dashboard.html',
        total_devices=total_devices,
        computers=computers,
        laptops=laptops,
        printers=printers,
        under_repair=under_repair,
        working_count=working_count,
        type_counts=type_counts,
        status_counts=status_counts,
    )


@app.route('/equipment')
@login_required
def equipment_list():
    inventory_number = request.args.get('inventory_number', '').strip()
    serial_number = request.args.get('serial_number', '').strip()
    employee = request.args.get('employee', '').strip()
    device_type = request.args.get('device_type', '')
    status = request.args.get('status', '')

    query = Equipment.query

    if inventory_number:
        query = query.filter(Equipment.inventory_number.ilike(f'%{inventory_number}%'))
    if serial_number:
        query = query.filter(Equipment.serial_number.ilike(f'%{serial_number}%'))
    if employee:
        query = query.filter(Equipment.responsible_employee.ilike(f'%{employee}%'))
    if device_type:
        query = query.filter(Equipment.device_type == device_type)
    if status:
        query = query.filter(Equipment.status == status)

    equipments = query.order_by(Equipment.id.desc()).all()
    return render_template(
        'equipment_list.html',
        equipments=equipments,
        inventory_number=inventory_number,
        serial_number=serial_number,
        employee=employee,
        device_type=device_type,
        status=status,
    )


@app.route('/equipment/add', methods=['GET', 'POST'])
@login_required
def add_equipment():
    if request.method == 'POST':
        inventory_number = request.form.get('inventory_number', '').strip()
        device_name = request.form.get('device_name', '').strip()
        device_type = request.form.get('device_type')
        brand = request.form.get('brand', '').strip()
        model = request.form.get('model', '').strip()
        cpu = request.form.get('cpu', '').strip()
        ram = request.form.get('ram', '').strip()
        storage = request.form.get('storage', '').strip()
        serial_number = request.form.get('serial_number', '').strip()
        purchase_date = request.form.get('purchase_date')
        location = request.form.get('location', '').strip()
        responsible_employee = request.form.get('responsible_employee', '').strip()
        status = request.form.get('status')

        if not inventory_number or not device_name or not serial_number:
            flash('Inventory number, device name, and serial number are required.', 'danger')
            return redirect(url_for('add_equipment'))

        if Equipment.query.filter((Equipment.inventory_number == inventory_number) | (Equipment.serial_number == serial_number)).first():
            flash('Inventory number or serial number already exists.', 'danger')
            return redirect(url_for('add_equipment'))

        try:
            purchase_date_obj = datetime.strptime(purchase_date, '%Y-%m-%d').date() if purchase_date else None
        except ValueError:
            flash('Please use a valid purchase date.', 'danger')
            return redirect(url_for('add_equipment'))

        equipment = Equipment(
            inventory_number=inventory_number,
            device_name=device_name,
            device_type=device_type,
            brand=brand,
            model=model,
            cpu=cpu,
            ram=ram,
            storage=storage,
            serial_number=serial_number,
            purchase_date=purchase_date_obj,
            location=location,
            responsible_employee=responsible_employee,
            status=status,
        )
        db.session.add(equipment)
        db.session.commit()
        flash('Equipment added successfully.', 'success')
        return redirect(url_for('equipment_list'))

    return render_template('equipment_form.html', equipment=None)


@app.route('/equipment/<int:equipment_id>')
@login_required
def equipment_detail(equipment_id):
    equipment = Equipment.query.get_or_404(equipment_id)
    return render_template('equipment_detail.html', equipment=equipment)


@app.route('/equipment/<int:equipment_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_equipment(equipment_id):
    equipment = Equipment.query.get_or_404(equipment_id)

    if request.method == 'POST':
        equipment.inventory_number = request.form.get('inventory_number', '').strip()
        equipment.device_name = request.form.get('device_name', '').strip()
        equipment.device_type = request.form.get('device_type')
        equipment.brand = request.form.get('brand', '').strip()
        equipment.model = request.form.get('model', '').strip()
        equipment.cpu = request.form.get('cpu', '').strip()
        equipment.ram = request.form.get('ram', '').strip()
        equipment.storage = request.form.get('storage', '').strip()
        equipment.serial_number = request.form.get('serial_number', '').strip()
        equipment.location = request.form.get('location', '').strip()
        equipment.responsible_employee = request.form.get('responsible_employee', '').strip()
        equipment.status = request.form.get('status')

        purchase_date = request.form.get('purchase_date')
        try:
            equipment.purchase_date = datetime.strptime(purchase_date, '%Y-%m-%d').date() if purchase_date else None
        except ValueError:
            flash('Please use a valid purchase date.', 'danger')
            return redirect(url_for('edit_equipment', equipment_id=equipment.id))

        db.session.commit()
        flash('Equipment updated successfully.', 'success')
        return redirect(url_for('equipment_detail', equipment_id=equipment.id))

    return render_template('equipment_form.html', equipment=equipment)


@app.route('/equipment/<int:equipment_id>/delete', methods=['POST'])
@login_required
def delete_equipment(equipment_id):
    equipment = Equipment.query.get_or_404(equipment_id)
    db.session.delete(equipment)
    db.session.commit()
    flash('Equipment deleted successfully.', 'success')
    return redirect(url_for('equipment_list'))


@app.route('/reports')
@login_required
def reports():
    type_counts = db.session.query(Equipment.device_type, func.count(Equipment.id)).group_by(Equipment.device_type).all()
    status_counts = db.session.query(Equipment.status, func.count(Equipment.id)).group_by(Equipment.status).all()

    type_labels = [item[0] for item in type_counts]
    type_data = [item[1] for item in type_counts]
    status_labels = [item[0] for item in status_counts]
    status_data = [item[1] for item in status_counts]

    return render_template(
        'reports.html',
        type_labels=type_labels,
        type_data=type_data,
        status_labels=status_labels,
        status_data=status_data,
    )


with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            password_hash=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)
