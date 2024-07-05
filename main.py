from flask import Flask, request, flash, redirect, url_for, render_template, Blueprint, request, make_response, render_template_string
from flask_login import LoginManager, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
import pickle
import os
import base64

main = Blueprint('main', __name__)

@main.route('/')
def index():
    from .models import Product
    products = Product.query.filter(Product.id <= 2)
    print(products)

    if not request.cookies.get('display_name'):
        return render_template('index.html', display_name='', products=products)

    # I have no idea about the security consequences of this code
    serialized_data_b64 = request.cookies.get('display_name')
    serialized_data = base64.b64decode(serialized_data_b64)
    display_name = pickle.loads(serialized_data)

    return render_template('index.html', display_name=display_name, products=products)

@main.route('/products', methods=['GET'])
def products():
    from .models import Product
    products = Product.query.filter(Product.status == 0)
    print(products)
    #return 'test'
    return render_template('products.html', products=products)

@main.route('/auth')
def auth_check():
    if current_user.is_authenticated:
        return 'You are authenticated'
    else:
        return 'You are not authenticated'

@main.route('/role')
def role_check():
    if not current_user.is_authenticated: # has_roles isn't defined for unauthenticated users
        return 'You are not authenticated'
    if current_user.has_roles('admin'):
        return 'You are an admin'
    else:
        return 'You are not an admin'

# @main.route('/announcements')
# def announcements():
#     from .models import Announcements
#     announcements = Announcements.query.all()
#     return render_template('announcements.html', announcements=announcements)

@main.route('/announcements')
def announcements():
    from .models import Announcements
    announcements_rev = Announcements.query.all()
    announcements = []
    for item in reversed(announcements_rev):
        announcements.append(item)

    template = '''
    {% extends "layout.html" %}
    {% block content %}
    '''
    for announcement in announcements:
        template += '''
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">{}</h5>
                <p class="card-text">{}</p>
                <p class="card-text">Announcement from: {}</p>
                <p class="card-text">Posted at: {}</p>
            </div>
        </div>
        '''.format(announcement.title, announcement.body, announcement.author, announcement.time)
    template += '{% endblock %}'
    # This fixes some bootstrap issues I was having. There's probably a better way to do this but oh well
    return render_template_string(template)
