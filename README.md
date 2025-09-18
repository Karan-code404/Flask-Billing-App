# [Bill Generator](https://render.com/docs/web-services#port-binding)
Flask Billing App
This is a simple, modern web application for small businesses and shopkeepers to generate and print digital bills. Built with the Flask framework, this app provides an intuitive interface for managing a product inventory and creating transaction receipts on the fly.

Features
Dynamic Item Management: Shopkeepers can select pre-existing items from a dropdown list.

Custom Item Addition: If an item is not in the database, users can easily add a new item with its name and price. This new item is saved and becomes available for future bills.

Real-time Billing: The application calculates the total price of the bill as items are added, including a grand total.

Server-Side PDF Generation: Upon clicking the "Print Bill" button, the app sends the billing data to the server, which uses the fpdf2 library to generate a clean, professional PDF receipt.

QR Code Integration: Each bill includes a QR code containing the transaction details in JSON format. This allows for quick verification or data transfer by scanning the code.

Modern UI/UX: The website features a clean, responsive design with a subtle, animated RGB border to provide a polished user experience.

Technologies Used
Backend: Python with Flask

Database: Flask-SQLAlchemy with SQLite for simple, local data storage.

PDF Generation: fpdf2

QR Codes: qrcode

Frontend: HTML5, CSS3, and JavaScript

Styling: Custom CSS with animations and gradients.

UI/Logic: Vanilla JavaScript for dynamic interactions and API communication.

How to Run Locally
To run this project on your local machine, follow these steps:

Clone the Repository:

Bash

git clone https://github.com/Karan-code404/Flask-Billing-App.git
cd Flask-Billing-App
Create a Virtual Environment:

Bash

python -m venv venv
Activate the Virtual Environment:

Windows: venv\Scripts\activate

macOS/Linux: source venv/bin/activate

Install Dependencies:

Bash

pip install -r requirements.txt
Run the Application:

Bash

python app.py
The application will be available at https://render.com/docs/web-services#port-binding.

Deployment
This application is deployed on Render.com. It uses the provided start.sh file to run the server.

Project Status
The project is complete and fully functional. Further improvements could include user authentication, a more advanced database (like PostgreSQL), and the ability to view a history of all generated bills.
