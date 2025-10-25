from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///seo_platform.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from models import db, Project, Page, Keyword, SEOChecklist, Backlink

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    projects = Project.query.all()
    return render_template('index.html', projects=projects)

@app.route('/dashboard')
def dashboard():
    projects = Project.query.all()
    total_projects = len(projects)
    total_pages = Page.query.count()
    total_keywords = Keyword.query.count()
    
    stats = {
        'total_projects': total_projects,
        'total_pages': total_pages,
        'total_keywords': total_keywords,
        'avg_seo_score': 0
    }
    
    if total_projects > 0:
        total_score = sum([p.seo_score or 0 for p in projects])
        stats['avg_seo_score'] = int(total_score / total_projects)
    
    return render_template('dashboard.html', projects=projects, stats=stats)

@app.route('/project/new', methods=['GET', 'POST'])
def new_project():
    if request.method == 'POST':
        project = Project(
            name=request.form.get('name'),
            niche=request.form.get('niche'),
            domain=request.form.get('domain'),
            target_keywords=request.form.get('target_keywords'),
            description=request.form.get('description')
        )
        db.session.add(project)
        db.session.commit()
        
        checklist = SEOChecklist(project_id=project.id)
        db.session.add(checklist)
        db.session.commit()
        
        flash('Project created successfully!', 'success')
        return redirect(url_for('project_detail', project_id=project.id))
    
    return render_template('new_project.html')

@app.route('/project/<int:project_id>')
def project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    pages = Page.query.filter_by(project_id=project_id).all()
    keywords = Keyword.query.filter_by(project_id=project_id).all()
    checklist = SEOChecklist.query.filter_by(project_id=project_id).first()
    
    if not checklist:
        checklist = SEOChecklist(project_id=project_id)
        db.session.add(checklist)
        db.session.commit()
    
    return render_template('project_detail.html', 
                         project=project, 
                         pages=pages, 
                         keywords=keywords,
                         checklist=checklist)

@app.route('/project/<int:project_id>/keywords')
def keywords(project_id):
    project = Project.query.get_or_404(project_id)
    keywords = Keyword.query.filter_by(project_id=project_id).all()
    return render_template('keywords.html', project=project, keywords=keywords)

@app.route('/project/<int:project_id>/keyword/add', methods=['POST'])
def add_keyword(project_id):
    keyword = Keyword(
        project_id=project_id,
        keyword=request.form.get('keyword'),
        search_volume=request.form.get('search_volume', type=int),
        difficulty=request.form.get('difficulty'),
        current_rank=request.form.get('current_rank', type=int)
    )
    db.session.add(keyword)
    db.session.commit()
    flash('Keyword added successfully!', 'success')
    return redirect(url_for('keywords', project_id=project_id))

@app.route('/project/<int:project_id>/pages')
def pages(project_id):
    project = Project.query.get_or_404(project_id)
    pages = Page.query.filter_by(project_id=project_id).all()
    return render_template('pages.html', project=project, pages=pages)

@app.route('/project/<int:project_id>/page/new', methods=['GET', 'POST'])
def new_page(project_id):
    project = Project.query.get_or_404(project_id)
    
    if request.method == 'POST':
        page = Page(
            project_id=project_id,
            title=request.form.get('title'),
            slug=request.form.get('slug'),
            page_type=request.form.get('page_type'),
            meta_title=request.form.get('meta_title'),
            meta_description=request.form.get('meta_description'),
            content=request.form.get('content', '')
        )
        db.session.add(page)
        db.session.commit()
        flash('Page created successfully!', 'success')
        return redirect(url_for('edit_page', project_id=project_id, page_id=page.id))
    
    return render_template('new_page.html', project=project)

@app.route('/project/<int:project_id>/page/<int:page_id>/edit', methods=['GET', 'POST'])
def edit_page(project_id, page_id):
    project = Project.query.get_or_404(project_id)
    page = Page.query.get_or_404(page_id)
    
    if request.method == 'POST':
        page.title = request.form.get('title')
        page.slug = request.form.get('slug')
        page.page_type = request.form.get('page_type')
        page.meta_title = request.form.get('meta_title')
        page.meta_description = request.form.get('meta_description')
        page.content = request.form.get('content')
        page.h1_tag = request.form.get('h1_tag')
        page.updated_at = datetime.utcnow()
        
        page.seo_score = calculate_seo_score(page)
        
        db.session.commit()
        flash('Page updated successfully!', 'success')
        return redirect(url_for('edit_page', project_id=project_id, page_id=page_id))
    
    return render_template('edit_page.html', project=project, page=page)

@app.route('/project/<int:project_id>/checklist', methods=['GET', 'POST'])
def checklist(project_id):
    project = Project.query.get_or_404(project_id)
    checklist = SEOChecklist.query.filter_by(project_id=project_id).first()
    
    if not checklist:
        checklist = SEOChecklist(project_id=project_id)
        db.session.add(checklist)
        db.session.commit()
    
    if request.method == 'POST':
        checklist.domain_selected = request.form.get('domain_selected') == 'on'
        checklist.hosting_setup = request.form.get('hosting_setup') == 'on'
        checklist.ssl_installed = request.form.get('ssl_installed') == 'on'
        checklist.core_pages_created = request.form.get('core_pages_created') == 'on'
        checklist.keyword_research_done = request.form.get('keyword_research_done') == 'on'
        checklist.content_optimized = request.form.get('content_optimized') == 'on'
        checklist.meta_tags_set = request.form.get('meta_tags_set') == 'on'
        checklist.images_optimized = request.form.get('images_optimized') == 'on'
        checklist.site_speed_optimized = request.form.get('site_speed_optimized') == 'on'
        checklist.mobile_friendly = request.form.get('mobile_friendly') == 'on'
        checklist.analytics_setup = request.form.get('analytics_setup') == 'on'
        checklist.search_console_setup = request.form.get('search_console_setup') == 'on'
        checklist.sitemap_submitted = request.form.get('sitemap_submitted') == 'on'
        checklist.backlinks_started = request.form.get('backlinks_started') == 'on'
        
        db.session.commit()
        
        project.seo_score = checklist.get_completion_percentage()
        db.session.commit()
        
        flash('Checklist updated successfully!', 'success')
        return redirect(url_for('checklist', project_id=project_id))
    
    return render_template('checklist.html', project=project, checklist=checklist)

@app.route('/project/<int:project_id>/speed-test')
def speed_test(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template('speed_test.html', project=project)

@app.route('/project/<int:project_id>/backlinks')
def backlinks(project_id):
    project = Project.query.get_or_404(project_id)
    backlinks = Backlink.query.filter_by(project_id=project_id).all()
    return render_template('backlinks.html', project=project, backlinks=backlinks)

@app.route('/project/<int:project_id>/backlink/add', methods=['POST'])
def add_backlink(project_id):
    backlink = Backlink(
        project_id=project_id,
        source_url=request.form.get('source_url'),
        target_url=request.form.get('target_url'),
        anchor_text=request.form.get('anchor_text'),
        domain_authority=request.form.get('domain_authority', type=int),
        status=request.form.get('status', 'pending')
    )
    db.session.add(backlink)
    db.session.commit()
    flash('Backlink added successfully!', 'success')
    return redirect(url_for('backlinks', project_id=project_id))

@app.route('/project/<int:project_id>/google-integration')
def google_integration(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template('google_integration.html', project=project)

@app.route('/api/seo-score', methods=['POST'])
def api_seo_score():
    data = request.json
    score = {
        'title_score': 0,
        'meta_score': 0,
        'content_score': 0,
        'overall_score': 0,
        'suggestions': []
    }
    
    if data:
        title = data.get('title', '')
        meta = data.get('meta_description', '')
        content = data.get('content', '')
        
        if len(title) >= 30 and len(title) <= 60:
            score['title_score'] = 100
        elif len(title) > 0:
            score['title_score'] = 50
            score['suggestions'].append('Title should be between 30-60 characters')
        else:
            score['suggestions'].append('Add a title tag')
        
        if len(meta) >= 120 and len(meta) <= 160:
            score['meta_score'] = 100
        elif len(meta) > 0:
            score['meta_score'] = 50
            score['suggestions'].append('Meta description should be between 120-160 characters')
        else:
            score['suggestions'].append('Add a meta description')
        
        if len(content) >= 300:
            score['content_score'] = 100
        elif len(content) > 0:
            score['content_score'] = 50
            score['suggestions'].append('Content should be at least 300 words')
        else:
            score['suggestions'].append('Add page content')
        
        score['overall_score'] = round((score['title_score'] + score['meta_score'] + score['content_score']) / 3)
    
    return jsonify(score)

def calculate_seo_score(page):
    score = 0
    
    if page.meta_title and len(page.meta_title) >= 30 and len(page.meta_title) <= 60:
        score += 20
    
    if page.meta_description and len(page.meta_description) >= 120 and len(page.meta_description) <= 160:
        score += 20
    
    if page.h1_tag:
        score += 20
    
    if page.content and len(page.content) >= 300:
        score += 20
    
    if page.slug and '/' in page.slug:
        score += 20
    
    return score

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
