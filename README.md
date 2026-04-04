👑 A1 Bakery Management System
"Eat a taste of happiness"

The A1 Bakery Management System is a professional web-based platform designed to bring a local bakery business online. It allows customers to browse a variety of cakes and bakery products while providing the owner (Admin) with a robust dashboard to manage orders and track revenue.


🚀 Key Features
💻 For Customers

Glassmorphism UI: A premium design featuring a translucent blur effect over a high-quality bakery background to enhance user experience.

Mobile-First Design: A highly responsive, Flipkart-inspired navigation bar that works perfectly on all Android and iOS devices.

Smart UPI Payment: Generates dynamic QR codes where the order amount is automatically pre-filled to ensure a seamless checkout.

UTR Verification: Users can enter their 12-digit Transaction (UTR) ID for payment confirmation.

Order Tracking: Customers can check the real-time status of their orders (e.g., Scheduled, In Progress, Delivered).

Secure Authentication: A professional logout confirmation modal to prevent accidental sign-outs.


🛠️ For Admin (Owner)

Jazzmin Dashboard: A modern and clean administrative interface for efficient management.

One-Click Verification: A dedicated column in the dashboard to verify online payments with a single click.

Order Management: Full control to update order statuses and manage delivery schedules.

Product Management: Ability to add, edit, or delete bakery items through the admin panel.

Revenue Tracking: Real-time analytics on total orders and total revenue generated.


🛠️ Technologies Used

Backend: Python & Django Web Framework (MVT Architecture).

Frontend: HTML5, CSS3, and JavaScript.

UI Framework: Materialize CSS (for a professional and responsive layout).

Database: SQLite (Django's secure default database).

Hosting: Deployed and live on PythonAnywhere


📐 Architecture: MVT Pattern
This project follows the Model-View-Template (MVT) architecture:

Model: Defines the database structure for Products and Orders.

View: Contains the business logic that connects the database to the user interface.

Template: The frontend HTML files that the user interacts with.


📦 Local Installation
To run this project on your local machine:

Clone the Repository:

Bash
git clone https://github.com/yourusername/A1-Bakery.git
Apply Migrations:

Bash
python manage.py makemigrations
python manage.py migrate
Create a Superuser (Admin):

Bash
python manage.py createsuperuser
Run the Server:

Bash
python manage.py runserver


🛡️ Security Features
CSRF Protection: Uses Cross-Site Request Forgery tokens to secure form submissions.

Secret Key Encryption: Ensures that sessions and password hashing remain secure.


Developed with ❤️ by A1 Bakery Team