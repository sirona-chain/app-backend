import os
from flask import Blueprint

bp = Blueprint(
    "client",
    __name__,
)


@bp.route("/", defaults={"path": ""})
def catch_all(path):
   return {"message": "hello world"}
