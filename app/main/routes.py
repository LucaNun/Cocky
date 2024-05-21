from app.main import bp

from flask import render_template, request, redirect, url_for
from app.db import get_db

@bp.route('/')
def index():
    return "Hello"

