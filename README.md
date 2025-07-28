🎓 Online School API
A secure, scalable, and production-deployable e-learning backend API built with Django REST Framework, offering JWT-based authentication, role-specific access, and course monetization capabilities. This project is deployed using Vercel, integrated with Supabase (PostgreSQL) for production, and features a complete sandbox payment workflow using SSLCommerz.

🛠️ Tech Stack
Component	Technology
Backend Framework	Django, Django REST Framework
Auth Mechanism	JWT (Token-based login)
Email Service	SMTP (Email confirmation)
Payment Gateway	SSLCommerz Sandbox
DB (Development)	SQLite
DB (Production)	Supabase (PostgreSQL)
Deployment	Vercel
API Docs	Swagger/OpenAPI

🔑 Core Features
🔐 Authentication & User Identity
User Registration & Email Verification

JWT-based login/logout system

Account activation via confirmation link

Role-based access control: Student, Teacher, Admin

👨‍🎓 Student Module
Register, verify email, login

Add courses to cart

Place orders and pay via SSLCommerz (sandbox)

View enrolled courses

👨‍🏫 Teacher Module
Add courses

View only self-created courses

🛡️ Admin Module
View all orders and courses

Change order status (e.g., mark as confirmed or cancel)

Full access control for moderation

Access course sales reports:

Last 7 days

Last 30 days

Add subjects and courses

🧾 Project Structure
ONLINE_SCHOOL_API/
├── adminApp/          # Admin-related utilities and configurations
├── api/               # Shared API-level configurations (urls, views, routers)
├── course/            # Course and subject management (Teacher role)
├── fixtures/          # Initial data fixtures (if any)
├── media/             # Media files (course thumbnails, etc.)
├── online_school/     # Django project settings and core configurations
├── order/             # Cart, order, and SSLCommerz payment logic
├── users/             # User registration, JWT auth, email verification, roles
├── .env               # Environment variable definitions
├── .gitignore         # Git ignored files
├── db.sqlite3         # Local development database
├── manage.py          # Django management script
├── venv/              # Python virtual environment

⚙️ Setup & Installation
✅ Requirements
Python 3.9+
pip

🔄 Local Installation
git clone https://github.com/your-username/Online-School-Api.git
cd Online-School-Api
pip install -r requirements.txt
⚙️ Environment Variables
Create a .env file and configure it like this:

SECRET_KEY=your_django_secret
DEBUG=True
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=your_email_password

# JWT
JWT_SECRET_KEY=your_jwt_secret
JWT_ACCESS_TOKEN_LIFETIME=5
JWT_REFRESH_TOKEN_LIFETIME=30

# SSLCommerz (Sandbox)
SSLCOMMERZ_STORE_ID=test_store_id
SSLCOMMERZ_STORE_PASSWORD=test_password
SSLCOMMERZ_SANDBOX=True

🚀 Running Locally
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

📦 API Endpoints
Interactive Swagger Documentation
http://localhost:8000/swagger/

🧪 Key Functional Workflows
🔁 Registration & Activation
User signs up

Receives verification email

Clicks link → account is activated

Logs in and accesses views based on role

💳 SSLCommerz Payment (Sandbox)
Student places an order

Redirects to SSLCommerz sandbox gateway

After payment, status is recorded and student gains access

📊 Sales Reporting (Admin Only)
http
GET http://127.0.0.1:8000/api/v1/admin-view-set/

🏗️ Deployment Notes
Database: Supabase PostgreSQL

Live Backend: Hosted on Vercel

Frontend Integration: Compatible with any modern frontend (React, Vue, etc.)

🚧 Future Roadmap
✅ Stripe/SSLCommerz live payment integration

✅ Supabase PostgreSQL migration

📜 License
This project is licensed under the MIT License.

👤 Author
Pritom Sarkar
📫 pritom.cse.29@gmail.com
🔗 https://github.com/pritomcse29

