from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    niche = db.Column(db.String(100))
    domain = db.Column(db.String(200))
    target_keywords = db.Column(db.Text)
    description = db.Column(db.Text)
    seo_score = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    pages = db.relationship('Page', backref='project', lazy=True, cascade='all, delete-orphan')
    keywords = db.relationship('Keyword', backref='project', lazy=True, cascade='all, delete-orphan')
    checklist = db.relationship('SEOChecklist', backref='project', lazy=True, cascade='all, delete-orphan')
    backlinks = db.relationship('Backlink', backref='project', lazy=True, cascade='all, delete-orphan')

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200))
    page_type = db.Column(db.String(50))
    meta_title = db.Column(db.String(200))
    meta_description = db.Column(db.Text)
    h1_tag = db.Column(db.String(200))
    content = db.Column(db.Text)
    seo_score = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

class Keyword(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    keyword = db.Column(db.String(200), nullable=False)
    search_volume = db.Column(db.Integer)
    difficulty = db.Column(db.String(50))
    current_rank = db.Column(db.Integer)
    target_rank = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SEOChecklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    
    domain_selected = db.Column(db.Boolean, default=False)
    hosting_setup = db.Column(db.Boolean, default=False)
    ssl_installed = db.Column(db.Boolean, default=False)
    core_pages_created = db.Column(db.Boolean, default=False)
    keyword_research_done = db.Column(db.Boolean, default=False)
    content_optimized = db.Column(db.Boolean, default=False)
    meta_tags_set = db.Column(db.Boolean, default=False)
    images_optimized = db.Column(db.Boolean, default=False)
    site_speed_optimized = db.Column(db.Boolean, default=False)
    mobile_friendly = db.Column(db.Boolean, default=False)
    analytics_setup = db.Column(db.Boolean, default=False)
    search_console_setup = db.Column(db.Boolean, default=False)
    sitemap_submitted = db.Column(db.Boolean, default=False)
    backlinks_started = db.Column(db.Boolean, default=False)
    
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_completion_percentage(self):
        total = 14
        completed = sum([
            self.domain_selected,
            self.hosting_setup,
            self.ssl_installed,
            self.core_pages_created,
            self.keyword_research_done,
            self.content_optimized,
            self.meta_tags_set,
            self.images_optimized,
            self.site_speed_optimized,
            self.mobile_friendly,
            self.analytics_setup,
            self.search_console_setup,
            self.sitemap_submitted,
            self.backlinks_started
        ])
        return round((completed / total) * 100)

class Backlink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    source_url = db.Column(db.String(500))
    target_url = db.Column(db.String(500))
    anchor_text = db.Column(db.String(200))
    domain_authority = db.Column(db.Integer)
    status = db.Column(db.String(50), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
