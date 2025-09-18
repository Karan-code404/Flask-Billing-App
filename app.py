from flask import Flask, render_template, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from fpdf import FPDF
import qrcode
import json
import os # To handle file paths and deletion

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Database model for a single bill item
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Item {self.name}>'

# Create the database and add some initial items
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

# Main route to display the web page
@app.route('/')
def index():
    return render_template('index.html')

# API endpoint to get and add items
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

# Route to generate and send the PDF with QR code
@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    bill_data = request.json
    
    # 1. Generate QR Code
    qr_data = json.dumps(bill_data)
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

    # 2. Initialize PDF object and add bill content
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=16)

    pdf.cell(200, 10, text="Bill", ln=True, align="C")
    pdf.cell(200, 10, text="", ln=True)

    pdf.set_font("Arial", size=12, style='B')
    pdf.cell(70, 10, "Item", border=1)
    pdf.cell(40, 10, "Price", border=1)
    pdf.cell(30, 10, "Qty", border=1)
    pdf.cell(50, 10, "Total", border=1, ln=True)

    pdf.set_font("Arial", size=12)
    grand_total = 0
    for item in bill_data:
        name = item['name']
        price = item['price']
        quantity = item['quantity']
        total = item['total']
        grand_total += total
        
        pdf.cell(70, 10, str(name), border=1)
        pdf.cell(40, 10, str(price), border=1)
        pdf.cell(30, 10, str(quantity), border=1)
        pdf.cell(50, 10, str(total), border=1, ln=True)

    pdf.cell(140, 10, "Grand Total:", border=1, align="R")
    pdf.cell(50, 10, str(grand_total), border=1, ln=True)

    # 3. Add QR code to PDF
    pdf.cell(200, 10, text="", ln=True) # Add space
    pdf.image(temp_qr_path, x=80, y=pdf.get_y(), w=40)

    # Create and send the response with PDF data
    response = make_response(bytes(pdf.output(dest='S')))
    response.headers.set('Content-Type', 'application/pdf')
    response.headers.set('Content-Disposition', 'attachment', filename='bill.pdf')

    # Delete the temporary QR code file
    os.remove(temp_qr_path)
    
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)