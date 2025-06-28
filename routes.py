from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import app, users_db, activities_db, challenges_db, rewards_db, ecological_points
from models import User, Activity

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Check if user already exists
        for user in users_db.values():
            if user.username == username or user.email == email:
                flash('Usuario o email ya existe', 'error')
                return render_template('register.html')
        
        # Create new user
        user_id = len(users_db) + 1
        password_hash = generate_password_hash(password)
        user = User(user_id, username, email, password_hash)
        users_db[user_id] = user
        
        login_user(user)
        flash('¡Registro exitoso! Bienvenido a EcoTrujillo', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Find user
        user = None
        for u in users_db.values():
            if u.username == username:
                user = u
                break
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('¡Bienvenido de vuelta!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Get user's recent activities
    user_activities = [a for a in activities_db if a.user_id == current_user.id][-5:]
    
    # Calculate progress for current challenges
    challenge_progress = []
    for challenge in challenges_db:
        progress = calculate_challenge_progress(current_user.id, challenge)
        challenge_progress.append({
            'challenge': challenge,
            'progress': progress
        })
    
    return render_template('dashboard.html', 
                         user_activities=user_activities,
                         challenge_progress=challenge_progress)

@app.route('/activity', methods=['GET', 'POST'])
@login_required
def activity():
    if request.method == 'POST':
        activity_type = request.form['activity_type']
        description = request.form['description']
        
        # Calculate points based on activity type
        points_map = {
            'reciclaje': 50,
            'transporte_eco': 30,
            'limpieza': 100,
            'ahorro_energia': 40,
            'reforestacion': 80,
            'educacion': 60
        }
        
        points = points_map.get(activity_type, 25)
        
        # Create activity
        activity_id = len(activities_db) + 1
        activity = Activity(activity_id, current_user.id, activity_type, description, points)
        activities_db.append(activity)
        
        # Add points to user
        current_user.add_points(points)
        current_user.add_activity(activity)
        
        # Check for achievements
        check_achievements(current_user)
        
        flash(f'¡Actividad registrada! Has ganado {points} puntos EcoTrujillo', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('activity.html')

@app.route('/map')
def map_view():
    return render_template('map.html', ecological_points=ecological_points)

@app.route('/leaderboard')
def leaderboard():
    # Sort users by points
    sorted_users = sorted(users_db.values(), key=lambda x: x.points, reverse=True)
    return render_template('leaderboard.html', users=sorted_users)

@app.route('/challenges')
@login_required
def challenges():
    challenge_progress = []
    for challenge in challenges_db:
        progress = calculate_challenge_progress(current_user.id, challenge)
        challenge_progress.append({
            'challenge': challenge,
            'progress': progress
        })
    
    return render_template('challenges.html', challenge_progress=challenge_progress)

@app.route('/rewards')
@login_required
def rewards():
    available_rewards = []
    claimed_rewards = []
    
    for reward in rewards_db:
        if current_user.points >= reward['points_required']:
            available_rewards.append(reward)
        else:
            claimed_rewards.append(reward)
    
    return render_template('rewards.html', 
                         available_rewards=available_rewards,
                         claimed_rewards=claimed_rewards)

def calculate_challenge_progress(user_id, challenge):
    """Calculate user's progress for a specific challenge"""
    user_activities = [a for a in activities_db if a.user_id == user_id]
    
    if challenge['name'] == 'Reto Reciclaje Semanal':
        # Count recycling activities this week
        recycling_count = len([a for a in user_activities if a.activity_type == 'reciclaje'])
        return min(recycling_count, challenge['target'])
    elif challenge['name'] == 'Transporte Eco':
        # Count eco transport activities
        transport_count = len([a for a in user_activities if a.activity_type == 'transporte_eco'])
        return min(transport_count, challenge['target'])
    elif challenge['name'] == 'Limpieza Comunitaria':
        # Count cleaning activities
        cleaning_count = len([a for a in user_activities if a.activity_type == 'limpieza'])
        return min(cleaning_count, challenge['target'])
    
    return 0

def check_achievements(user):
    """Check and award achievements to user"""
    achievements = [
        {'name': 'Primer Paso', 'requirement': 1, 'type': 'activities'},
        {'name': 'Eco Activo', 'requirement': 10, 'type': 'activities'},
        {'name': 'Centenario', 'requirement': 100, 'type': 'points'},
        {'name': 'Reciclador', 'requirement': 5, 'type': 'recycling'},
    ]
    
    activity_count = len(user.activities)
    recycling_count = len([a for a in user.activities if a.activity_type == 'reciclaje'])
    
    for achievement in achievements:
        if achievement['name'] not in user.achievements:
            if achievement['type'] == 'activities' and activity_count >= achievement['requirement']:
                user.add_achievement(achievement['name'])
            elif achievement['type'] == 'points' and user.points >= achievement['requirement']:
                user.add_achievement(achievement['name'])
            elif achievement['type'] == 'recycling' and recycling_count >= achievement['requirement']:
                user.add_achievement(achievement['name'])
