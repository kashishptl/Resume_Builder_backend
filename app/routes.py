from flask import Blueprint
from .controllers import (
    signup,
    login,
    refresh_token,
    create_resume,
    get_all_resumes,
    get_single_resume,
    update_resume,
    delete_resume
)
from flask_jwt_extended import jwt_required

routes = Blueprint('routes', __name__)


# ================= AUTH ROUTES =================
routes.route('/signup', methods=['POST'])(signup)
routes.route('/login', methods=['POST'])(login)

# Refresh access token
routes.route('/refresh', methods=['POST'])(
    jwt_required(refresh=True)(refresh_token)
)


# ================= RESUME ROUTES =================
# Create Resume
routes.route('/resume', methods=['POST'])(
    jwt_required()(create_resume)
)

# Get All Resumes
routes.route('/resume', methods=['GET'])(
    jwt_required()(get_all_resumes)
)

# Get Single Resume
routes.route('/resume/<int:id>', methods=['GET'])(
    jwt_required()(get_single_resume)
)

# Update Resume
routes.route('/resume/<int:id>', methods=['PUT'])(
    jwt_required()(update_resume)
)

# Delete Resume
routes.route('/resume/<int:id>', methods=['DELETE'])(
    jwt_required()(delete_resume)
)