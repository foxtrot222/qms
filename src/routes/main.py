from flask import Blueprint, render_template, session, redirect, url_for

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/help')
def help():
    return render_template('help.html')

@main_bp.route('/contact')
def contact():
    return render_template('contact.html')

@main_bp.route('/user/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))
