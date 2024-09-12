from flask import Blueprint, render_template

home_bp = Blueprint('home_bp', __name__, template_folder='templates')


@home_bp.route("/")
@home_bp.route("/index")
def index():
    return render_template('home/index.html')


@home_bp.route('/about')
def about():
    return render_template('under_construction.html', page_name='About')


@home_bp.route('/test')
def test():
    return render_template('under_construction.html', page_name='Test')


@home_bp.route('/privacy')
def privacy():
    return render_template('under_construction.html', page_name='Privacy')


@home_bp.route('/termsofservice')
def termsofservice():
    return render_template('under_construction.html', page_name='Terms of service')
