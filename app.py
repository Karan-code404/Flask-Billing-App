from flask import Flask, render_template, request, jsonify, make_response, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from fpdf import FPDF
import qrcode
import json
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = 'your_super_secret_key'  # Change this to a strong, random string
db = SQLAlchemy(app)

# Database model for a user
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Database model for a single bill item
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Item {self.name}>'

# Database model for bill history
class BillHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    bill_data = db.Column(db.Text, nullable=False) # Stores JSON string of items
    total_amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<BillHistory {self.client_name} - {self.timestamp}>'

# Create the database and add initial items
with app.app_context():
    db.create_all()
    if not Item.query.first():
        sample_items = [
            Item(name='Aloo Paratha', price=50.0),
            Item(name='Chole Bhature', price=70.0),
            Item(name='Samosa', price=20.0)
        ]
        db.session.bulk_save_objects(sample_items)
        db.session.commit()
    # Create a default user for testing
    if not User.query.first():
        admin_user = User(username='admin')
        admin_user.set_password('password')
        db.session.add(admin_user)
        db.session.commit()

# Default route for the login page
@app.route('/')
def default_redirect():
    return redirect(url_for('login'))

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user is None:
            flash('This user does not exist. Please register first.', 'error')
        elif not user.check_password(password):
            flash('Wrong password. Please try again.', 'error')
        else:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('bill_generator'))
    
    return render_template('login.html')

# User registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash('A user with this username already exists.', 'error')
        else:
            new_user = User(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
            
    return render_template('register.html')

# Bill generator page (protected route)
@app.route('/bill_generator')
def bill_generator():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('bill_generator.html')

# History page (protected route)
@app.route('/history')
def history():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    history_list = BillHistory.query.order_by(BillHistory.timestamp.desc()).all()
    
    parsed_history = []
    for bill in history_list:
        parsed_history.append({
            'id': bill.id,
            'client_name': bill.client_name,
            'total_amount': bill.total_amount,
            'timestamp': bill.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'bill_data': json.loads(bill.bill_data)
        })

    return render_template('history.html', history=parsed_history)

# Admin panel route
@app.route('/admin_panel')
def admin_panel():
    if not session.get('logged_in') or session.get('username') != 'admin':
        flash('You do not have permission to view this page.', 'error')
        return redirect(url_for('login'))
    
    items_list = Item.query.all()
    
    return render_template('admin_panel.html', items=items_list)

# Logout route
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

# API endpoint to get and add items (used by both front-end and admin panel)
@app.route('/items', methods=['GET', 'POST'])
def items():
    if request.method == 'POST':
        data = request.json
        if not data or 'name' not in data or 'price' not in data:
            return jsonify({'error': 'Invalid data provided'}), 400
        
        new_item = Item(name=data['name'], price=data['price'])
        try:
            db.session.add(new_item)
            db.session.commit()
            return jsonify({'message': 'Item added successfully!', 'id': new_item.id}), 201
        except Exception:
            return jsonify({'error': 'Item with this name already exists!'}), 409
    
    all_items = Item.query.all()
    items_list = [{'id': item.id, 'name': item.name, 'price': item.price} for item in all_items]
    return jsonify(items_list)

# API endpoint to delete an item
@app.route('/delete_item/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    if not session.get('logged_in') or session.get('username') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401
    
    item_to_delete = Item.query.get_or_404(item_id)
    db.session.delete(item_to_delete)
    db.session.commit()
    return jsonify({'message': 'Item deleted successfully!'})

# Route to generate and send the PDF with QR code
@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    request_data = request.json
    client_name = request_data.get('client_name', 'Client')
    bill_data = request_data.get('bill_items', [])

    # 1. Store Bill History
    grand_total = sum(item['total'] for item in bill_data)
    
    new_bill = BillHistory(
        client_name=client_name,
        bill_data=json.dumps(bill_data),
        total_amount=grand_total
    )
    db.session.add(new_bill)
    db.session.commit()

    # 2. Generate QR Code
    qr_data = json.dumps(request_data)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    temp_qr_path = "temp_qr.png"
    img.save(temp_qr_path)

    # 3. Initialize PDF object and add bill content
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=16)

    pdf.cell(200, 10, text="Bill", ln=True, align="C")
    pdf.cell(200, 10, text=f"Client Name: {client_name}", ln=True, align="L")
    pdf.cell(200, 10, text=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align="L")
    pdf.cell(200, 10, text="", ln=True)

    pdf.set_font("Arial", size=12, style='B')
    pdf.cell(70, 10, "Item", border=1)
    pdf.cell(40, 10, "Price", border=1)
    pdf.cell(30, 10, "Qty", border=1)
    pdf.cell(50, 10, "Total", border=1, ln=True)

    pdf.set_font("Arial", size=12)
    for item in bill_data:
        name = item['name']
        price = item['price']
        quantity = item['quantity']
        total = item['total']
        
        pdf.cell(70, 10, str(name), border=1)
        pdf.cell(40, 10, str(price), border=1)
        pdf.cell(30, 10, str(quantity), border=1)
        pdf.cell(50, 10, str(total), border=1, ln=True)

    pdf.cell(140, 10, "Grand Total:", border=1, align="R")
    pdf.cell(50, 10, str(grand_total), border=1, ln=True)

    # 4. Add QR code to PDF
    pdf.cell(200, 10, text="", ln=True)
    pdf.image(temp_qr_path, x=80, y=pdf.get_y(), w=40)

    response = make_response(bytes(pdf.output(dest='S')))
    response.headers.set('Content-Type', 'application/pdf')
    response.headers.set('Content-Disposition', 'attachment', filename='bill.pdf')

    os.remove(temp_qr_path)
    
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)