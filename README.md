# SEO Agency Client Management Platform

A comprehensive web application for SEO agencies to manage clients, sell monthly service packages, track deliverables, handle invoicing, and provide detailed SEO performance reports.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supported-blue)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple)

## 🚀 Features

### For SEO Agencies (Admin)
- **Client Management** - Onboard and manage unlimited clients
- **Service Package Management** - Create and edit tiered SEO packages
- **Deliverable Tracking** - Track SEO tasks (keyword research, on-page SEO, content, backlinks, reports)
- **Invoice & Payment Management** - Generate monthly invoices and record payments
- **Performance Monitoring** - View client SEO metrics and keyword rankings
- **Content Editor** - Edit website content and packages directly in browser
- **Dashboard Analytics** - Real-time stats on revenue, active clients, and pending tasks

### For Clients
- **Personal Dashboard** - View SEO package and performance metrics
- **Deliverables Tracker** - Monitor progress on SEO tasks
- **SEO Reports** - Interactive charts showing traffic, rankings, backlinks, and domain authority
- **Keyword Rankings** - Track keyword positions with historical data
- **Invoice Management** - View billing history and payment status
- **Self-Service Registration** - Sign up and create account online

## 📦 Default Service Packages

- **Basic SEO** - $299/month
  - 10 keywords tracked
  - 5 pages optimized
  - 5 backlinks per month
  - Monthly reports

- **Standard SEO** - $599/month
  - 25 keywords tracked
  - 15 pages optimized
  - 15 backlinks per month
  - Bi-weekly reports

- **Premium SEO** - $1,299/month
  - 50 keywords tracked
  - 30 pages optimized
  - 30 backlinks per month
  - Weekly reports

## 🛠️ Technology Stack

- **Backend**: Python 3.11, Flask, SQLAlchemy
- **Frontend**: Bootstrap 5, JavaScript, jQuery, Chart.js
- **Database**: PostgreSQL (production) / SQLite (development)
- **Authentication**: Session-based with password hashing (Werkzeug)
- **Icons**: Bootstrap Icons

## 📋 Prerequisites

- Python 3.8 or higher
- PostgreSQL (optional, for production)
- pip (Python package manager)

## ⚡ Quick Start (Development)

### 1. Clone or Download the Project

```bash
git clone <your-repo-url>
cd seo-agency-platform
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python app.py
```

### 5. Access the Application

Open your browser and navigate to:
```
http://localhost:5000
```

**Default Admin Login:**
- Email: `admin@seoagency.com`
- Password: `admin123`

## 🐘 PostgreSQL Setup (Production)

### Using pgAdmin4

1. **Create Database in pgAdmin4:**
   - Right-click "Databases" → Create → Database
   - Name: `seo_agency_db`
   - Click "Save"

2. **Create `.env` File:**

```env
SESSION_SECRET=your-secret-key-change-this
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/seo_agency_db
```

3. **Initialize Database:**

```bash
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

4. **Run Application:**

```bash
python app.py
```

5. **View Data in pgAdmin4:**
   - Expand: Servers → PostgreSQL → Databases → seo_agency_db
   - Navigate to: Schemas → public → Tables
   - Right-click any table → "View/Edit Data" → "All Rows"

📖 **For detailed PostgreSQL setup**, see [SETUP_POSTGRESQL.md](SETUP_POSTGRESQL.md)

## 📁 Project Structure

```
seo-agency-platform/
├── app.py                      # Main Flask application
├── models.py                   # Database models
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── README.md                  # This file
├── SETUP_POSTGRESQL.md        # Detailed PostgreSQL guide
├── templates/
│   ├── base.html             # Base template
│   ├── index.html            # Homepage
│   ├── login.html            # Login page
│   ├── signup.html           # Registration page
│   ├── admin/                # Admin portal templates
│   │   ├── dashboard.html
│   │   ├── clients.html
│   │   ├── client_detail.html
│   │   ├── new_client.html
│   │   ├── packages.html
│   │   ├── edit_packages.html
│   │   ├── edit_content.html
│   │   ├── deliverables.html
│   │   └── invoices.html
│   └── client/               # Client portal templates
│       ├── dashboard.html
│       ├── deliverables.html
│       ├── invoices.html
│       └── reports.html
├── static/
│   └── css/
│       └── style.css         # Custom styles
└── instance/
    ├── seo_agency.db         # SQLite database (auto-created)
    └── site_content.json     # Editable site content
```

## 💻 Usage Guide

### Admin Workflows

1. **Login as Admin**
   - Navigate to `/login`
   - Use admin credentials

2. **Add New Client**
   - Go to "Clients" → "Add New Client"
   - Fill in client details and assign package
   - Client receives auto-generated invoice

3. **Edit Service Packages**
   - Click "Content" → "Edit Packages"
   - Update pricing, features, or create new packages
   - Changes appear on homepage immediately

4. **Edit Website Content**
   - Click "Content" → "Edit Site Content"
   - Update headlines, descriptions, features
   - Save and view changes on homepage

5. **Track Deliverables**
   - View client detail page
   - Add deliverables (keyword research, SEO tasks, etc.)
   - Mark as completed when done

6. **Manage Invoices**
   - Go to "Invoices"
   - Record payments for unpaid invoices
   - Track payment methods and transaction IDs

### Client Workflows

1. **Sign Up**
   - Click "Sign Up" on homepage
   - Fill in registration form
   - Auto-login to client dashboard

2. **View Dashboard**
   - See package details and metrics
   - Track deliverables progress
   - View recent keyword rankings

3. **Check SEO Reports**
   - Navigate to "Reports"
   - View interactive performance charts
   - Monitor keyword position changes

4. **Review Invoices**
   - Go to "Invoices"
   - View billing history and payment status

## 🔒 Security Features

- ✅ Password hashing with Werkzeug
- ✅ Session-based authentication
- ✅ Role-based access control (admin/client)
- ✅ CSRF protection via Flask sessions
- ✅ Email uniqueness validation
- ✅ Environment-based secret keys

## 🎨 Customization

### Change Service Packages
Login as admin → Content → Edit Packages

### Update Homepage Content
Login as admin → Content → Edit Site Content

### Modify Styling
Edit `static/css/style.css`

### Add New Features
- Database models: `models.py`
- Routes and logic: `app.py`
- Templates: `templates/`

## 🗄️ Database Schema

**8 Main Tables:**
- `users` - User authentication (admin/client)
- `service_packages` - SEO package offerings
- `clients` - Client profiles and company info
- `deliverables` - SEO tasks and completion tracking
- `invoices` - Monthly billing invoices
- `payments` - Payment records
- `seo_metrics` - Monthly performance snapshots
- `tracked_keywords` - Keyword ranking history

## 🚢 Deployment

### Environment Variables

Create `.env` file with:

```env
SESSION_SECRET=<generate-random-secret-key>
DATABASE_URL=postgresql://user:password@host:5432/database
```

### Production Recommendations

- Use PostgreSQL instead of SQLite
- Set strong `SESSION_SECRET`
- Use production WSGI server (Gunicorn, uWSGI)
- Enable HTTPS
- Set `debug=False` in production
- Configure proper logging

## 📊 Default Data

The application auto-generates on first run:
- 1 Admin user
- 3 Service packages (Basic, Standard, Premium)

## 🐛 Troubleshooting

**Port 5000 already in use:**
```python
# In app.py, change the last line:
app.run(debug=True, host='0.0.0.0', port=5001)
```

**Database connection errors:**
- Check PostgreSQL is running
- Verify credentials in `.env` file
- Ensure database exists in pgAdmin4

**Import errors:**
- Activate virtual environment
- Run `pip install -r requirements.txt`

**Tables not created:**
- Run database initialization commands
- Check database connection string

## 📝 License

This project is available for use and modification.

## 🤝 Contributing

Feel free to fork, modify, and submit pull requests!

## 📞 Support

For issues or questions:
- Check `SETUP_POSTGRESQL.md` for database setup
- Review this README for common solutions
- Check application logs for error details

---

**Built with ❤️ for SEO Agencies**

Made with Python Flask, Bootstrap, and PostgreSQL
