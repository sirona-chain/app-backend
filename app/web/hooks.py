import functools
import logging
from flask import g, session, request
from sqlalchemy.exc import IntegrityError, NoResultFound
from werkzeug.exceptions import Unauthorized, BadRequest
from app.web.db.models import User, Model

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return {"message": "Unauthorized"}, 401
        return view(**kwargs)

    return wrapped_view

def add_headers(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        try:
            g.user = User.find_by(id=user_id)
        except Exception:
            g.user = None

def handle_error(err):
    if isinstance(err, IntegrityError):
        logging.error(err)
        return {"message": "In use"}, 400
    elif isinstance(err, NoResultFound):
        logging.error(err)
        return {"message": "Not found"}, 404
    elif isinstance(err, Unauthorized):
        logging.error(err)
        return {"message": err.description}, 401
    elif isinstance(err, BadRequest):
        logging.error(err)
        return {"message": err.description}, 401

    raise err