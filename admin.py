from flask import Blueprint, render_template, request, redirect, flash, make_response
from flask_login import current_user
from functools import wraps
from .models import Announcements
from . import db
import datetime

admin = Blueprint('admin', __name__)

def admin_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect('/login')
        if not current_user.has_roles('admin'):
            return redirect('/')
        return func(*args, **kwargs)
    return wrapper

# def admin_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if not current_user.is_authenticated or "admin" not in current_user.roles:
#             abort(403)
#         return f(*args, **kwargs)
#     return decorated_function

@admin.route('/review')
@admin_only
def review():
    from .models import Product
    products = Product.query.filter(Product.status != 0)
    print(products)
    #return 'test'
    return render_template('review.html', products=products)

@admin.route('/add_product')
@admin_only
def add_product():
    return render_template('add_product.html')

@admin.route('/add_announcement', methods=['GET'])
@admin_only
def add_announcement():
    return render_template('add_announcement.html')

@admin.route('/add_announcement', methods=['POST'])
@admin_only
def add_announcement_post():
    title = request.form['title']
    body = request.form['body']
    author = current_user.username
    current_time = datetime.datetime.now()
    
    new_announcement = Announcements(title=title, body=body, author=author ,time=current_time)
    db.session.add(new_announcement)
    db.session.commit()

    return 'Announcement added'
