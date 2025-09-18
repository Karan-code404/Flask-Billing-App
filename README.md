# [Bill Generator](https://flask-billing-app-l5ll.onrender.com)

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
Here is a proper README.md file for your GitHub project. This will give a professional overview of your Flask application, explaining its features, how to set it up, and how to use it.

You can copy and paste this text directly into a file named README.md in the root of your project folder.

Flask Bill Generator
A simple web application for generating bills, managing items, and tracking sales history. This project is built using Python's Flask framework with SQLAlchemy for database management.

Features
User Authentication: Secure login and registration for users.

Bill Generation: A user-friendly interface to select items and quantities to generate a bill.

Dynamic Item Management: Add and remove items and their prices directly from the web interface.

PDF Generation: Bills are generated as professional PDF documents, including client details, item breakdowns, and a QR code with bill data.

Bill History: View a complete history of all generated bills, including client names, totals, and timestamps.

Admin Panel: A protected section for the administrator to manage item inventory and sales history.

Responsive UI: A clean, modern, and mobile-friendly design.

Technologies Used
Backend: Python, Flask, Flask-SQLAlchemy

Database: SQLite3

PDF Generation: FPDF, qrcode

Frontend: HTML, CSS, JavaScript

Getting Started
Prerequisites
Make sure you have Python installed on your system. You can download it from python.org.

Installation
Clone the repository:


Bash

git clone https://github.com/Karan-code404/Flask-Billing-App.git
cd Flask-Billing-App

Create a Virtual Environment:

Create a virtual environment:
It's recommended to work within a virtual environment to manage dependencies.


Bash

python -m venv venv

Activate the virtual environment:

On Windows:

Bash

venv\Scripts\activate
On macOS and Linux:

Bash

source venv/bin/activate
Install the required packages:


Bash

pip install -r requirements.txt

Run the Application:

Note: If you don't have a requirements.txt file, you can generate one after installing the packages with pip freeze > requirements.txt. For this project, you'll need: Flask, Flask-SQLAlchemy, fpdf, qrcode, and Werkzeug.

Running the Application
Run the Flask application:


Bash

python app.py

The application will be available at https://render.com/docs/web-services#port-binding.

Deployment
This application is deployed on Render.com. It uses the provided start.sh file to run the server.

Project Status
The project is complete and fully functional. Further improvements could include user authentication, a more advanced database (like PostgreSQL), and the ability to view a history of all generated bills.

Access the application:
Open your web browser and go to http://127.0.0.1:5000.

Usage
Public Pages
Login (/login): The main entry point. Log in with your credentials.

Register (/register): Create a new user account.

Bill Generator (/bill_generator): Accessible after logging in. This is where you can select items to generate a PDF bill.

Bill History (/history): A dedicated page to view all past transactions.

Admin Access
The admin panel is a restricted area.

Login: Use the default admin credentials to access the admin panel.

Username: admin

Password: password

Admin Panel (/admin_panel): From here, you can manage and delete items from the database.

