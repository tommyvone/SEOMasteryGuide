# SEO Agency Client Management Platform

## Overview
A comprehensive Flask-based web application for SEO agencies to sell and manage monthly SEO service packages to clients. This platform enables agencies to onboard clients, track deliverables, manage invoices, and provide client-facing SEO performance reports.

## Project Purpose
Help SEO agencies manage their business by providing:
- **Service Package Management**: Create and manage tiered monthly SEO packages (Basic, Standard, Premium)
- **Client Onboarding**: Easy client registration with package assignment
- **Deliverable Tracking**: Track SEO work completion for each client
- **Invoice Management**: Generate and track monthly invoices and payments
- **Client Portal**: Allow clients to view their SEO progress, reports, and invoices
- **Admin Dashboard**: Agency owner can manage all clients, services, and revenue
- **SEO Metrics**: Track and display keyword rankings, traffic, backlinks, and domain authority

## Recent Changes (2025-10-25)
- Complete rebuild from SEO website builder to SEO agency platform
- Created database models for Users, Clients, ServicePackages, Deliverables, Invoices, Payments, SEOMetrics, TrackedKeywords
- Implemented role-based authentication (admin/client)
- Built admin dashboard with client management, deliverable tracking, and invoice management
- Created client portal with performance dashboards, deliverable tracking, and reports
- Added seed data with 3 service packages (Basic $299, Standard $599, Premium $1299)
- Implemented charts and visualizations for SEO performance tracking

## Project Architecture

### Backend (Flask)
- **app.py**: Main Flask application with authentication and business logic
- **models.py**: SQLAlchemy database models with relationships
- **Database**: SQLite for development (production-ready for PostgreSQL)

### Frontend (Bootstrap + JavaScript)
- **Public Pages**: Landing page with package pricing
- **Admin Portal**: Dashboard, clients, packages, deliverables, invoices
- **Client Portal**: Dashboard, deliverables, invoices, SEO reports
- **Charts**: Chart.js for performance visualization

### Key Features
1. **Role-Based Access**: Separate admin and client portals with authentication
2. **Service Packages**: Pre-configured Basic, Standard, and Premium tiers
3. **Client Management**: Complete client lifecycle from onboarding to service delivery
4. **Deliverable System**: Track keyword research, on-page SEO, content, backlinks, technical SEO, and reports
5. **Invoice & Payment Tracking**: Generate monthly invoices and record payments
6. **SEO Performance Metrics**: Track organic traffic, keyword rankings, backlinks, domain authority
7. **Keyword Tracking**: Monitor keyword positions with historical data and trend indicators
8. **Visual Reports**: Interactive charts showing performance trends

## Technology Stack
- **Backend**: Python 3.11, Flask, SQLAlchemy, Werkzeug (password hashing)
- **Frontend**: Bootstrap 5, jQuery, Chart.js, HTML5
- **Database**: SQLite (development)
- **Icons**: Bootstrap Icons
- **Styling**: Custom CSS with gradient themes

## Database Models
- **User**: Authentication and user management (admin/client roles)
- **ServicePackage**: Monthly SEO service packages with features and pricing
- **Client**: Client profiles linked to users and packages
- **Deliverable**: SEO tasks and deliverables with status tracking
- **Invoice**: Monthly invoices with payment tracking
- **Payment**: Payment records linked to invoices
- **SEOMetric**: Monthly SEO performance snapshots
- **TrackedKeyword**: Keyword tracking with ranking history

## User Workflows

### Admin Workflow
1. Login to admin portal
2. View dashboard with stats (clients, revenue, pending tasks)
3. Add new clients with package assignment
4. Track deliverables and mark them complete
5. Generate and manage invoices
6. Record payments
7. View client performance metrics

### Client Workflow
1. Login to client portal
2. View dashboard with package info and SEO metrics
3. Track deliverables and completion status
4. View SEO performance reports with charts
5. Monitor keyword rankings
6. View and track invoices

## Default Credentials
- **Admin**: admin@seoagency.com / admin123

## Service Packages
- **Basic SEO**: $299/month - 10 keywords, 5 pages, 5 backlinks, monthly report
- **Standard SEO**: $599/month - 25 keywords, 15 pages, 15 backlinks, bi-weekly reports
- **Premium SEO**: $1299/month - 50 keywords, 30 pages, 30 backlinks, weekly reports

## Development Notes
- Server runs on port 5000
- Debug mode enabled for development
- Flash messages for user feedback
- Session-based authentication
- Auto-generated seed data on first run
