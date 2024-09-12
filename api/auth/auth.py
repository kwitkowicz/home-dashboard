from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from api.extensions import db
from api.models import user
from api.decorators import access_forbidden

auth_bp = Blueprint('auth_bp', __name__, template_folder='templates')


@auth_bp.route('/login')
def login():
    if current_user.is_authenticated:
        # return redirect(url_for('home_bp.index'))
        return render_template('under_construction.html', page_name='Dashboard')
    return render_template('auth/login.html')


@auth_bp.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    actual_user = user.User.query.filter_by(email=email).first()

    if not actual_user or not check_password_hash(actual_user.password, password):
        flash('Invalid email or password', 'alert-warning')
        return redirect(url_for('auth_bp.login'))

    login_user(actual_user, remember=remember)

    # return redirect(url_for('dashboard_bp.main'))
    return render_template('under_construction.html', page_name='Dashboard')


@auth_bp.route('/signup')
def signup():
    return render_template('auth/signup.html')


@auth_bp.route('/signup', methods=['POST'])
@access_forbidden
def signup_post():
    name = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    actual_user = user.User.query.filter_by(email=email).first()

    if actual_user:
        flash("You already have an account", category='alert-success')
        return redirect(url_for('auth_bp.login'))

    new_user = user.User(email=email, username=name, password=generate_password_hash(password))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth_bp.login'))


@auth_bp.route('/forgotkey')
def forgotkey():
    return render_template('under_construction.html', page_name='Forgot key')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home_bp.index'))
