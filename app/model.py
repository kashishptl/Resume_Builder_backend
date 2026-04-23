from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ===================== USER =====================

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index = True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    resumes = db.relationship('Resume', backref='user', lazy=True,cascade = "all, delete-orphan")

# ===================== RESUME =====================

class Resume(db.Model):
    __tablename__ = 'resumes'

    resume_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, index = True)

    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    location = db.Column(db.String(100))
    professional_summary = db.Column(db.Text)
    skills = db.Column(db.JSON)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    experiences = db.relationship('Experience', backref='resume', lazy=True, cascade="all, delete-orphan")
    educations = db.relationship('Education', backref='resume', lazy=True, cascade="all, delete-orphan")
    projects = db.relationship('Project', backref='resume', lazy=True, cascade="all, delete-orphan")
    achievements = db.relationship('Achievement', backref='resume', lazy=True, cascade="all, delete-orphan")
    languages = db.relationship('Language', backref='resume', lazy=True, cascade="all, delete-orphan")
    hobbies = db.relationship('Hobby', backref='resume', lazy=True, cascade="all, delete-orphan")

# ===================== EXPERIENCE =====================

class Experience(db.Model):
    __tablename__ = 'experiences'

    experience_id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.resume_id'), nullable=True, index=True)

    company = db.Column(db.String(100))
    role = db.Column(db.String(100))
    duration = db.Column(db.String(50))
    description = db.Column(db.Text)

    def to_dict(self):
        return {
            "id": self.experience_id,
            "company": self.company,
            "role": self.role,
            "duration": self.duration,
            "description": self.description
        }

# ===================== EDUCATION =====================

class Education(db.Model):
    __tablename__ = 'educations'

    education_id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.resume_id'), nullable=True, index=True)

    degree = db.Column(db.String(100))
    institution = db.Column(db.String(150))
    year = db.Column(db.String(10))

    def to_dict(self):
        return {
            "id" : self.education_id,
            "degree" : self.degree,
            "institution" : self.institution,
            "year" : self.year
        }
    
# ===================== PROJECT =====================

class Project(db.Model):
    __tablename__ = 'projects'

    project_id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.resume_id'), nullable=False, index=True)

    title = db.Column(db.String(150))
    description = db.Column(db.Text)
    
    def to_dict(self):
        return {
            "id" : self.project_id,
            "title" : self.title,
            "description" : self.description
        }


# ===================== ACHIEVEMENT =====================

class Achievement(db.Model):
    __tablename__ = 'achievements'

    achievement_id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.resume_id'), nullable=False, index=True)

    title = db.Column(db.String(150))
    description = db.Column(db.Text)
    
    def to_dict(self):
        return {
            "id" : self.achievement_id,
            "title" : self.title,
            "description" : self.description
        }    

# ===================== LANGUAGE =====================

class Language(db.Model):
    __tablename__ = 'languages'

    language_id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.resume_id'), nullable=False, index=True)

    language_name = db.Column(db.String(50))
    
    def to_dict(self):
        return {
            "id" : self.language_id,
            "language_name" : self.language_name
        }   

   
# ===================== HOBBY =====================

class Hobby(db.Model):
    __tablename__ = 'hobbies'

    hobby_id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.resume_id'), nullable=False,index=True)

    hobby_name = db.Column(db.String(100))
    
    def to_dict(self):
        return{
            "id" : self.hobby_id,
            "hobby_name":self.hobby_name
        }
    


