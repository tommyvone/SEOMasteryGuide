from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
from datetime import datetime, timedelta
from functools import wraps
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///seo_agency.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from models import db, User, ServicePackage, Client, Deliverable, Invoice, Payment, SEOMetric, TrackedKeyword

db.init_app(app)

with app.app_context():
    db.create_all()
    
    if not ServicePackage.query.first():
        basic = ServicePackage(
            name='Basic SEO',
            description='Perfect for small businesses starting with SEO',
            monthly_price=299.00,
            features='10 Keywords Tracked, 5 Pages Optimized, 5 Backlinks/Month, Monthly Report',
            keywords_tracked=10,
            pages_optimized=5,
            backlinks_monthly=5,
            monthly_reports=1
        )
        standard = ServicePackage(
            name='Standard SEO',
            description='Ideal for growing businesses',
            monthly_price=599.00,
            features='25 Keywords Tracked, 15 Pages Optimized, 15 Backlinks/Month, Bi-weekly Reports',
            keywords_tracked=25,
            pages_optimized=15,
            backlinks_monthly=15,
            monthly_reports=2
        )
        premium = ServicePackage(
            name='Premium SEO',
            description='Comprehensive SEO for established businesses',
            monthly_price=1299.00,
            features='50 Keywords Tracked, 30 Pages Optimized, 30 Backlinks/Month, Weekly Reports, Dedicated Manager',
            keywords_tracked=50,
            pages_optimized=30,
            backlinks_monthly=30,
            monthly_reports=4
        )
        db.session.add_all([basic, standard, premium])
        
        admin = User(email='admin@seoagency.com', name='Admin User', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        
        db.session.commit()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        user = User.query.get(session['user_id'])
        if not user or user.role != 'admin':
            flash('Admin access required', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    packages = ServicePackage.query.filter_by(is_active=True).all()
    return render_template('index.html', packages=packages)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['user_role'] = user.role
            session['user_name'] = user.name
            
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('client_dashboard'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    total_clients = Client.query.count()
    active_clients = Client.query.filter_by(status='active').count()
    total_revenue = db.session.query(db.func.sum(Invoice.amount)).filter(
        Invoice.status == 'paid'
    ).scalar() or 0
    
    pending_deliverables = Deliverable.query.filter_by(status='pending').count()
    
    recent_clients = Client.query.order_by(Client.created_at.desc()).limit(5).all()
    pending_invoices = Invoice.query.filter_by(status='unpaid').order_by(Invoice.due_date).limit(5).all()
    
    stats = {
        'total_clients': total_clients,
        'active_clients': active_clients,
        'total_revenue': total_revenue,
        'pending_deliverables': pending_deliverables
    }
    
    return render_template('admin/dashboard.html', stats=stats, recent_clients=recent_clients, 
                         pending_invoices=pending_invoices)

@app.route('/admin/clients')
@admin_required
def admin_clients():
    clients = Client.query.join(User).order_by(Client.created_at.desc()).all()
    return render_template('admin/clients.html', clients=clients)

@app.route('/admin/client/<int:client_id>')
@admin_required
def admin_client_detail(client_id):
    client = Client.query.get_or_404(client_id)
    deliverables = Deliverable.query.filter_by(client_id=client_id).order_by(Deliverable.created_at.desc()).all()
    invoices = Invoice.query.filter_by(client_id=client_id).order_by(Invoice.issue_date.desc()).all()
    metrics = SEOMetric.query.filter_by(client_id=client_id).order_by(SEOMetric.metric_date.desc()).limit(12).all()
    keywords = TrackedKeyword.query.filter_by(client_id=client_id).all()
    
    return render_template('admin/client_detail.html', client=client, deliverables=deliverables,
                         invoices=invoices, metrics=metrics, keywords=keywords)

@app.route('/admin/client/new', methods=['GET', 'POST'])
@admin_required
def admin_new_client():
    if request.method == 'POST':
        user = User(
            email=request.form.get('email'),
            name=request.form.get('name'),
            role='client'
        )
        user.set_password(request.form.get('password'))
        db.session.add(user)
        db.session.flush()
        
        client = Client(
            user_id=user.id,
            package_id=request.form.get('package_id', type=int),
            company_name=request.form.get('company_name'),
            website_url=request.form.get('website_url'),
            industry=request.form.get('industry')
        )
        db.session.add(client)
        
        invoice_number = f"INV-{datetime.now().strftime('%Y%m')}-{Client.query.count() + 1:04d}"
        invoice = Invoice(
            client_id=client.id,
            invoice_number=invoice_number,
            amount=ServicePackage.query.get(client.package_id).monthly_price,
            due_date=datetime.now() + timedelta(days=30),
            description=f"Monthly SEO Services - {datetime.now().strftime('%B %Y')}"
        )
        db.session.add(invoice)
        
        db.session.commit()
        
        flash('Client added successfully!', 'success')
        return redirect(url_for('admin_clients'))
    
    packages = ServicePackage.query.filter_by(is_active=True).all()
    return render_template('admin/new_client.html', packages=packages)

@app.route('/admin/packages')
@admin_required
def admin_packages():
    packages = ServicePackage.query.all()
    return render_template('admin/packages.html', packages=packages)

@app.route('/admin/deliverables')
@admin_required
def admin_deliverables():
    deliverables = Deliverable.query.join(Client).join(User).order_by(Deliverable.due_date).all()
    return render_template('admin/deliverables.html', deliverables=deliverables)

@app.route('/admin/deliverable/add/<int:client_id>', methods=['POST'])
@admin_required
def admin_add_deliverable(client_id):
    deliverable = Deliverable(
        client_id=client_id,
        title=request.form.get('title'),
        description=request.form.get('description'),
        category=request.form.get('category'),
        due_date=datetime.strptime(request.form.get('due_date'), '%Y-%m-%d') if request.form.get('due_date') else None
    )
    db.session.add(deliverable)
    db.session.commit()
    flash('Deliverable added successfully!', 'success')
    return redirect(url_for('admin_client_detail', client_id=client_id))

@app.route('/admin/deliverable/<int:deliverable_id>/complete', methods=['POST'])
@admin_required
def admin_complete_deliverable(deliverable_id):
    deliverable = Deliverable.query.get_or_404(deliverable_id)
    deliverable.status = 'completed'
    deliverable.completed_date = datetime.now()
    deliverable.notes = request.form.get('notes', '')
    db.session.commit()
    flash('Deliverable marked as completed!', 'success')
    return redirect(request.referrer or url_for('admin_deliverables'))

@app.route('/admin/invoices')
@admin_required
def admin_invoices():
    invoices = Invoice.query.join(Client).join(User).order_by(Invoice.issue_date.desc()).all()
    return render_template('admin/invoices.html', invoices=invoices)

@app.route('/admin/invoice/<int:invoice_id>/pay', methods=['POST'])
@admin_required
def admin_pay_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    payment = Payment(
        invoice_id=invoice_id,
        amount=request.form.get('amount', type=float),
        payment_method=request.form.get('payment_method'),
        transaction_id=request.form.get('transaction_id')
    )
    db.session.add(payment)
    
    invoice.status = 'paid'
    invoice.paid_date = datetime.now()
    db.session.commit()
    
    flash('Payment recorded successfully!', 'success')
    return redirect(url_for('admin_invoices'))

@app.route('/client/dashboard')
@login_required
def client_dashboard():
    user = User.query.get(session['user_id'])
    if user.role == 'admin':
        return redirect(url_for('admin_dashboard'))
    
    client = Client.query.filter_by(user_id=user.id).first()
    if not client:
        flash('Client profile not found', 'danger')
        return redirect(url_for('index'))
    
    recent_deliverables = Deliverable.query.filter_by(client_id=client.id).order_by(
        Deliverable.created_at.desc()).limit(5).all()
    
    recent_metrics = SEOMetric.query.filter_by(client_id=client.id).order_by(
        SEOMetric.metric_date.desc()).limit(6).all()
    
    pending_invoices = Invoice.query.filter_by(client_id=client.id, status='unpaid').all()
    
    keywords = TrackedKeyword.query.filter_by(client_id=client.id).all()
    
    return render_template('client/dashboard.html', client=client, deliverables=recent_deliverables,
                         metrics=recent_metrics, invoices=pending_invoices, keywords=keywords)

@app.route('/client/deliverables')
@login_required
def client_deliverables():
    user = User.query.get(session['user_id'])
    client = Client.query.filter_by(user_id=user.id).first()
    deliverables = Deliverable.query.filter_by(client_id=client.id).order_by(Deliverable.created_at.desc()).all()
    return render_template('client/deliverables.html', client=client, deliverables=deliverables)

@app.route('/client/invoices')
@login_required
def client_invoices():
    user = User.query.get(session['user_id'])
    client = Client.query.filter_by(user_id=user.id).first()
    invoices = Invoice.query.filter_by(client_id=client.id).order_by(Invoice.issue_date.desc()).all()
    return render_template('client/invoices.html', client=client, invoices=invoices)

@app.route('/client/reports')
@login_required
def client_reports():
    user = User.query.get(session['user_id'])
    client = Client.query.filter_by(user_id=user.id).first()
    metrics = SEOMetric.query.filter_by(client_id=client.id).order_by(SEOMetric.metric_date.desc()).all()
    keywords = TrackedKeyword.query.filter_by(client_id=client.id).all()
    return render_template('client/reports.html', client=client, metrics=metrics, keywords=keywords)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
