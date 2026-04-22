from flask import request, jsonify
from .model import db, User, Resume, Experience, Education, Project, Achievement, Language, Hobby
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import get_jwt_identity, create_access_token, create_refresh_token

# ✅ Import ALL validators
from .validators import (
    validate_signup,
    validate_login,
    validate_resume,
    clean_string
)


# ===================== SIGNUP =====================

def signup():
    data = request.get_json() or {}

    errors = validate_signup(data)
    if errors:
        return jsonify({"message": "Validation failed", "errors": errors}), 400

    email = data.get("email").lower()

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "User already exists"}), 400

    user = User(
        name=data.get("name"),
        email=email,
        password=generate_password_hash(data.get("password"))
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User registered successfully",
        "access_token": create_access_token(identity=str(user.user_id)),
        "refresh_token": create_refresh_token(identity=str(user.user_id))
    }), 201


# ===================== LOGIN =====================

def login():
    data = request.get_json() or {}

    error = validate_login(data)
    if error:
        return jsonify(error), 400

    email = data.get("email").lower()
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid credentials"}), 401

    return jsonify({
        "message": "Login successful",
        "access_token": create_access_token(identity=str(user.user_id)),
        "refresh_token": create_refresh_token(identity=str(user.user_id))
    }), 200


# ===================== REFRESH =====================

def refresh_token():
    user_id = int(get_jwt_identity())

    return jsonify({
        "access_token": create_access_token(identity=str(user_id))
    }), 200


# ===================== CREATE RESUME =====================

def create_resume():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}

    errors = validate_resume(data)
    if errors:
        return jsonify({"message": "Validation failed", "errors": errors}), 400

    try:
        resume = Resume(
            user_id=user_id,
            full_name=clean_string(data.get('full_name')),
            email=clean_string(data.get('email')),
            phone=clean_string(data.get('phone')),
            location=clean_string(data.get('location')),
            professional_summary=clean_string(data.get('professional_summary')),
            skills=",".join(data.get('skills', []))
        )

        db.session.add(resume)
        db.session.flush()

        # EXPERIENCE
        for exp in data.get('experiences', []):
            if exp.get('company') and exp.get('role'):
                db.session.add(Experience(
                    resume_id=resume.resume_id,
                    company=clean_string(exp.get('company')),
                    role=clean_string(exp.get('role')),
                    duration=clean_string(exp.get('duration')),
                    description=clean_string(exp.get('description'))
                ))

        # EDUCATION
        for edu in data.get('education', []):
            if edu.get('degree'):
                db.session.add(Education(
                    resume_id=resume.resume_id,
                    degree=clean_string(edu.get('degree')),
                    institution=clean_string(edu.get('institution')),
                    year=clean_string(edu.get('year'))
                ))

        # PROJECTS
        for proj in data.get('projects', []):
            if proj.get('title'):
                db.session.add(Project(
                    resume_id=resume.resume_id,
                    title=clean_string(proj.get('title')),
                    description=clean_string(proj.get('description'))
                ))

        # ACHIEVEMENTS
        for ach in data.get('achievements', []):
            if ach.get('title'):
                db.session.add(Achievement(
                    resume_id=resume.resume_id,
                    title=clean_string(ach.get('title')),
                    description=clean_string(ach.get('description'))
                ))

        # LANGUAGES
        for lang in data.get('languages', []):
            if lang:
                db.session.add(Language(
                    resume_id=resume.resume_id,
                    language_name=clean_string(lang)
                ))

        # HOBBIES
        for hob in data.get('hobbies', []):
            if hob:
                db.session.add(Hobby(
                    resume_id=resume.resume_id,
                    hobby_name=clean_string(hob)
                ))

        db.session.commit()

        return jsonify({
            "message": "Resume created successfully",
            "resume_id": resume.resume_id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "message": "Something went wrong",
            "error": str(e)
        }), 500

# ===================== GET ALL =====================

def get_all_resumes():
    try:
        # ✅ Get user from JWT token
        user_id = get_jwt_identity()

        if not user_id:
            return jsonify({
                "message": "Unauthorized access"
            }), 401

        # ✅ Fetch resumes for that user
        resumes = Resume.query.filter_by(user_id=user_id).all()

        # ✅ If no data found
        if not resumes:
            return jsonify({
                "message": "No resumes found",
                "count": 0,
                "data": []
            }), 200

        # ✅ Format response
        data = []
        for r in resumes:
            data.append({
                "resume_id": r.resume_id,
                "full_name": r.full_name,
                "email": r.email,
                "phone": getattr(r, "phone", ""),
                "skills": r.skills.split(",") if isinstance(r.skills, str) else r.skills,
                "template": getattr(r, "template", "default"),
                "created_at": getattr(r, "created_at", None)
            })

        return jsonify({
            "message": "Resumes fetched successfully",
            "count": len(data),
            "data": data
        }), 200

    except Exception as e:
        return jsonify({
            "message": "Internal server error",
            "error": str(e)
        }), 500

# ===================== GET SINGLE =====================

def get_single_resume(id):
    user_id = int(get_jwt_identity())

    resume = Resume.query.filter_by(resume_id=id, user_id=user_id).first()

    if not resume:
        return jsonify({"message": "Not found"}), 404

    return jsonify({
        "resume_id": resume.resume_id,
        "full_name": resume.full_name,
        "email": resume.email,
        "phone": resume.phone,
        "location": resume.location,
        "experience": [exp.to_dict() for exp in resume.experiences],
        "education": [edu.to_dict() for edu in resume.educations],
        "professional_summary": resume.professional_summary,
        "skills": resume.skills.split(",") if resume.skills else []
    }), 200


# ===================== UPDATE =====================

def update_resume(id):
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}

    resume = Resume.query.filter_by(resume_id=id, user_id=user_id).first()

    if not resume:
        return jsonify({"message": "Not found"}), 404

    # ✅ validate only if fields present
    if "email" in data:
        from .validators import validate_email
        email_error = validate_email(data.get("email"))
        if email_error:
            return jsonify({"message": email_error}), 400

    resume.full_name = clean_string(data.get('full_name', resume.full_name))
    resume.email = clean_string(data.get('email', resume.email))
    resume.phone = clean_string(data.get('phone', resume.phone))
    resume.location = clean_string(data.get('location', resume.location))
    resume.professional_summary = clean_string(data.get('professional_summary', resume.professional_summary))

    if 'skills' in data and isinstance(data['skills'], list):
        resume.skills = ",".join(data['skills'])

    db.session.commit()

    return jsonify({"message": "Updated successfully"}), 200


# ===================== DELETE =====================

def delete_resume(id):
    user_id = int(get_jwt_identity())

    resume = Resume.query.filter_by(resume_id=id, user_id=user_id).first()

    if not resume:
        return jsonify({"message": "Not found"}), 404

    db.session.delete(resume)
    db.session.commit()

    return jsonify({"message": "Deleted successfully"}), 200