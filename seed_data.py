from app import app, db
from models import Equipment
from datetime import date


def seed_data():
    with app.app_context():
        # Clear existing data if you want a fresh sample set
        # db.session.query(Equipment).delete()
        # db.session.commit()

        sample_devices = [
            {
                'inventory_number': 'INV-1001',
                'device_name': 'Workstation Alpha',
                'device_type': 'Computer',
                'brand': 'Dell',
                'model': 'OptiPlex 7090',
                'cpu': 'Intel i7-11700',
                'ram': '16 GB',
                'storage': '512 GB SSD',
                'serial_number': 'SN-1001',
                'purchase_date': date(2024, 1, 15),
                'location': 'Office 101',
                'responsible_employee': 'Alice Johnson',
                'status': 'Working'
            },
            {
                'inventory_number': 'INV-1002',
                'device_name': 'Laptop Pro',
                'device_type': 'Laptop',
                'brand': 'Lenovo',
                'model': 'ThinkPad X1',
                'cpu': 'Intel i5-1240P',
                'ram': '16 GB',
                'storage': '1 TB SSD',
                'serial_number': 'SN-1002',
                'purchase_date': date(2023, 7, 20),
                'location': 'Office 205',
                'responsible_employee': 'Mark Lee',
                'status': 'Maintenance'
            },
            {
                'inventory_number': 'INV-1003',
                'device_name': 'Office Laser Printer',
                'device_type': 'Printer',
                'brand': 'HP',
                'model': 'LaserJet Pro MFP',
                'cpu': '',
                'ram': '',
                'storage': '',
                'serial_number': 'SN-1003',
                'purchase_date': date(2022, 11, 10),
                'location': 'Reception',
                'responsible_employee': 'Sarah Kim',
                'status': 'Repair'
            },
            {
                'inventory_number': 'INV-1004',
                'device_name': 'Network Gateway',
                'device_type': 'Network Device',
                'brand': 'Cisco',
                'model': 'RV340',
                'cpu': 'Quad-core',
                'ram': '2 GB',
                'storage': '128 MB',
                'serial_number': 'SN-1004',
                'purchase_date': date(2024, 3, 1),
                'location': 'Server Room',
                'responsible_employee': 'James Chen',
                'status': 'Working'
            }
        ]

        for item in sample_devices:
            if not Equipment.query.filter_by(serial_number=item['serial_number']).first():
                db.session.add(Equipment(**item))

        db.session.commit()
        print('Sample data inserted successfully.')


if __name__ == '__main__':
    seed_data()
