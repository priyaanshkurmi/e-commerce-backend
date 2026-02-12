# 🛒 Ecommerce Django Project

Backend + Frontend template-based e-commerce application built with Django.


⸻

**📌 Overview**

# This project is a full-featured e-commerce platform with:
*	•	Product listing & details
	•	Cart management
	•	Checkout & Razorpay payment integration
	•	Order tracking & status updates
	•	User authentication & profile management
	•	Invoice generation & email notifications
	•	Address management

**Tech Stack:**
*	•	Backend: Django 6
	•	Database: SQLite (development), can be switched to PostgreSQL
	•	Frontend: Django Templates (HTML, CSS)
	•	Payment Gateway: Razorpay
	•	PDF Generation: ReportLab / WeasyPrint (for invoices)

⸻

**⚡ Features**

# 1️⃣ User Management
*	•	Signup / Login / Logout
	•	Dashboard showing orders & payment status
	•	Profile & address management
	•	Secure password hashing & session management

# 2️⃣ Product Management
*	•	Product listing on homepage
	•	Product detail page
	•	Add to cart functionality from listing or detail page
	•	Cart persists across sessions

# 3️⃣ Cart & Checkout
*	•	Add, remove, or update quantity of items
	•	Checkout with address selection
	•	Razorpay integration for payments
	•	Payment status automatically updates orders

# 4️⃣ Orders & Status
*	•	Order model with statuses: Pending → Paid → Shipped →  		Delivered
	•	Admin can update order status
	•	Color-coded status in dashboard & order details

# 5️⃣ Invoices & Emails
*	•	Generate PDF invoice after successful payment
	•	Email sent automatically with invoice attached (requires SMTP setup)

# 6️⃣ Admin Panel
*	•	Full control over users, products, orders, payments
	•	Filter orders by status
	•	Update products & stock

⸻

**🚀 Installation & Setup**

# 1️⃣ Clone the Repository

* git clone https://github.com/priyaanshkurmi/ecommerce.git
  cd ecommerce

# 2️⃣ Create Virtual Environment

python3 -m venv venv
source venv/bin/activate   # macOS / Linux
venv\Scripts\activate      # Windows

# 3️⃣ Install Dependencies

pip install -r requirements.txt

# 4️⃣ Configure Environment Variables

**Create a .env file:**

*	SECRET_KEY=your-django-secret-key
	DEBUG=True
	RAZORPAY_KEY_ID=your-key-id
	RAZORPAY_KEY_SECRET=your-key-secret
	EMAIL_HOST=smtp.example.com
	EMAIL_PORT=587
	EMAIL_HOST_USER=your-email@example.com
	EMAIL_HOST_PASSWORD=your-email-password


⸻

# 5️⃣ Run Migrations

python manage.py migrate

# 6️⃣ Create Superuser

python manage.py createsuperuser

# 7️⃣ Run Development Server

python manage.py runserver

* Open in browser:

http://127.0.0.1:8000/


⸻

# 🛠 Usage

**Home Page**
*	•	Browse products
	•	Add products to cart
	•	Login/Signup if you want to checkout

**Cart**
*	•	View added products
	•	Update quantity or remove items
	•	Proceed to checkout

**Checkout & Payment**
*	•	Choose address
	•	Make payment using Razorpay test keys
	•	Success page with invoice & email notification

**Dashboard**
*	•	View orders
	•	Check payment status
	•	Update address/profile

⸻

# 🔐 Authentication
*	•	Public users can browse products
	•	Login/signup required for checkout & dashboard
	•	Admin access via /admin/

⸻

# 📁 Project Structure

	ecommerce/
	├─ accounts/        # User auth & dashboard
	├─ products/        # Product listing & details
	├─ orders/          # Cart & Order models
	├─ payments/        # Razorpay integration
	├─ templates/       # HTML templates
	├─ static/          # CSS & JS
	├─ config/          # Project settings & URLs
	└─ manage.py


⸻

# 💳 Payments
*	•	Razorpay integration (test environment)
	•	Stores payment details in database
	•	Updates order status automatically
	•	Supports multiple products per order

⸻

# 📜 Invoice
*	•	Generates PDF invoice after successful payment
	•	Includes order details, payment info, and address
	•	Can be downloaded by user from dashboard

⸻

# 📧 Email Notifications
*	•	Sends email automatically after payment success
	•	Includes invoice attachment
	•	Requires SMTP configuration in .env

⸻

**⚙️ Future Improvements**
	•	AJAX-based Add to Cart (no page reload)
	•	Social login (Google/Github)
	•	Wishlist / Favorites feature
	•	Product reviews & ratings
	•	Coupon codes & discounts
	•	Search & filter products
	•	Responsive mobile-friendly design

⸻

**🛠 Tech Stack**

#	Layer 	Technology
#	Backend	 Django 6, Python
#	Database	SQLite/PostgreSQL
#	Frontend	Django Templates, HTML, CSS
#	Payments	Razorpay
#	PDF Generation	ReportLab/WeasyPrint
#	Email	SMTP


⸻

# 📌 Notes
	•	For local testing, use Razorpay test keys
	•	Home page is publicly accessible
	•	Logged out users see Login/Signup buttons
	•	Logged in users see Dashboard & Logout

⸻

# 👑 Author

****Priyansh Patel**
	Full Stack Developer | Python | Django | Odoo | Web Development
		•	Email: priyanshkurmi2004@gmail.com
		•	LinkedIn: https://www.linkedin.com/in/priyaanshkurmi


⸻