from app.main import bp

from flask import render_template, request, redirect, url_for
from app.extensions import mysql

@bp.route('/')
def index():
    return "Hello"

