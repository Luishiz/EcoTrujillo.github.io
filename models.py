from flask_login import UserMixin
from datetime import datetime

class User(UserMixin):
    def __init__(self, id, username, email, password_hash, points=0):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.points = points
        self.activities = []
        self.achievements = []
        self.joined_date = datetime.now()
    
    def get_id(self):
        return str(self.id)
    
    def add_points(self, points):
        self.points += points
    
    def add_activity(self, activity):
        self.activities.append(activity)
    
    def add_achievement(self, achievement):
        if achievement not in self.achievements:
            self.achievements.append(achievement)
    
    def get_level(self):
        if self.points < 100:
            return "Eco Principiante"
        elif self.points < 500:
            return "Eco Activo"
        elif self.points < 1000:
            return "Eco Comprometido"
        elif self.points < 2000:
            return "Eco Líder"
        else:
            return "Eco Maestro"

class Activity:
    def __init__(self, id, user_id, activity_type, description, points, date=None):
        self.id = id
        self.user_id = user_id
        self.activity_type = activity_type
        self.description = description
        self.points = points
        self.date = date or datetime.now()
        self.verified = False

class Challenge:
    def __init__(self, id, name, description, points, challenge_type, target, unit):
        self.id = id
        self.name = name
        self.description = description
        self.points = points
        self.type = challenge_type
        self.target = target
        self.unit = unit
        self.participants = []

class Achievement:
    def __init__(self, id, name, description, icon, requirement):
        self.id = id
        self.name = name
        self.description = description
        self.icon = icon
        self.requirement = requirement
