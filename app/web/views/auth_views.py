from flask import Blueprint, g, request, session, jsonify, current_app, url_for, make_response
from app.web.db.models import User
from app.web.utils import generate_confirmation_token, send_email
from flask_cors import CORS
import jwt

bp = Blueprint("auth", __name__, url_prefix="/api/auth")
CORS(bp, supports_credentials=True)


@bp.route("/user", methods=["GET"])
def get_user():
    if g.user is not None:
        return g.user.as_dict()

    return jsonify(None)


@bp.route("/signup", methods=["POST"])
def signup():
    email = request.json.get("email")
    token = generate_confirmation_token(email)
    frontend_url = current_app.config.get('FRONTEND_URL')
    confirm_url = f"{frontend_url}/confirm/{token}"
    html = f"<p>Please click the link to confirm your email address: <a href='{confirm_url}'>{confirm_url}</a></p>"
    send_email(email, "Confirm Your Email Address", html)
    return {"message": "A confirmation email has been sent."}, 200


@bp.route("/confirm/<token>", methods=["GET"])
def confirm_email(token):
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        email = payload['email']
        user = User.create_with_wallet(email=email)
        session["user_id"] = user.id

        response = make_response({"message": "Email confirmed and user created.", "user": user.as_dict()}, 200)
        response.set_cookie("auth_token", token, httponly=True, secure=True, samesite='Strict')

        return response
    except jwt.ExpiredSignatureError:
        return {"message": "The confirmation link has expired."}, 400
    except jwt.InvalidTokenError:
        return {"message": "Invalid token."}, 400


@bp.route("/signout", methods=["POST"])
def signout():
    session.clear()
    response = make_response({"message": "Successfully logged out."})
    response.delete_cookie("auth_token")
    return response
