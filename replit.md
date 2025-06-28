# EcoTrujillo - Environmental Gamification Platform

## Overview

EcoTrujillo is a gamified environmental engagement platform designed for the city of Trujillo, Peru. The application encourages citizens to participate in ecological activities by offering a point-based reward system, challenges, leaderboards, and real-world incentives from local businesses. Users can register environmental activities, participate in weekly challenges, track their ecological impact, and redeem rewards.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 with Flask for server-side rendering
- **CSS Framework**: Bootstrap 5.3.0 for responsive design
- **JavaScript**: Vanilla JavaScript with custom modules
- **Mapping**: Leaflet.js for interactive ecological points map
- **Icons**: Font Awesome 6.4.0 for consistent iconography

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Authentication**: Flask-Login for session management
- **Password Security**: Werkzeug for password hashing
- **Deployment**: Gunicorn WSGI server with autoscale deployment target

### Data Storage
- **Current**: In-memory storage using Python dictionaries and lists
- **Structure**: Separate storage for users, activities, challenges, and rewards
- **Models**: Object-oriented design with User, Activity, and Challenge classes

## Key Components

### User Management System
- User registration and authentication
- Session management with Flask-Login
- User profiles with points, activities, achievements tracking
- Level progression system (Eco Principiante to Eco Maestro)

### Activity Tracking System
- Multiple activity types: recycling, sustainable transport, community cleaning, energy saving, reforestation
- Point allocation system based on activity type
- Activity verification workflow
- Historical activity tracking per user

### Gamification Engine
- Point-based reward system
- Weekly challenges with progress tracking
- User level progression based on accumulated points
- Achievement system for milestone recognition

### Interactive Map
- Leaflet.js integration for ecological points visualization
- Different marker types for various ecological locations
- Real-time location data for environmental activities

### Reward System
- Point redemption catalog
- Integration with local business partnerships
- Real-world incentive structure

## Data Flow

1. **User Registration**: New users create accounts with username, email, and password
2. **Activity Logging**: Users submit environmental activities through web forms
3. **Point Calculation**: System awards points based on predefined activity values
4. **Challenge Participation**: Users can join weekly challenges and track progress
5. **Leaderboard Updates**: User rankings update based on accumulated points
6. **Reward Redemption**: Users can exchange points for real-world benefits

## External Dependencies

### Python Packages
- Flask 3.1.1 - Web framework
- Flask-Login 0.6.3 - Authentication management
- Flask-SQLAlchemy 3.1.1 - Database ORM (prepared for future use)
- Gunicorn 23.0.0 - Production WSGI server
- Werkzeug 3.1.3 - Security utilities
- Email-validator 2.2.0 - Email validation
- Psycopg2-binary 2.9.10 - PostgreSQL adapter (prepared for future use)

### Frontend Libraries
- Bootstrap 5.3.0 - UI framework
- Font Awesome 6.4.0 - Icon library
- Leaflet.js 1.9.4 - Interactive mapping

### Infrastructure
- Nix package manager for system dependencies
- OpenSSL and PostgreSQL system packages
- Python 3.11 runtime environment

## Deployment Strategy

### Development Environment
- Replit-based development with hot reload
- Gunicorn development server with reload capability
- Port 5000 with reuse-port configuration

### Production Deployment
- Autoscale deployment target on Replit
- Gunicorn production server configuration
- ProxyFix middleware for reverse proxy compatibility
- Environment-based configuration for secrets

### Configuration Management
- Environment variables for sensitive data (SESSION_SECRET)
- Modular Flask application structure
- Separate route definitions for maintainability

## User Preferences

Preferred communication style: Simple, everyday language.

## Changelog

Changelog:
- June 19, 2025. Initial setup
- June 19, 2025. Created comprehensive VS Code development guide with complete project structure and setup instructions