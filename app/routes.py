from flask import Blueprint, jsonify, request, redirect, url_for, render_template, flash
from flask_login import login_required, current_user, login_user, logout_user
from app import db, bcrypt
from app.models import Landlord, Tenant, User
from app.forms import LoginForm, RegistrationForm

bp = Blueprint('api', __name__)

# CRUD for Landlords
@bp.route('/landlords', methods=['GET'])
@login_required
def get_landlords():
    landlords = Landlord.query.all()
    return jsonify([landlord.to_dict() for landlord in landlords])

@bp.route('/landlords', methods=['POST'])
@login_required
def create_landlord():
    data = request.get_json()
    landlord = Landlord(
        name=data['name'],
        phone=data.get('phone'),
        email=data['email'],
        address=data.get('address'),
        contract=data.get('contract')
    )
    db.session.add(landlord)
    db.session.commit()
    return jsonify(landlord.to_dict()), 201

@bp.route('/landlords/<int:id>', methods=['GET'])
@login_required
def get_landlord(id):
    landlord = Landlord.query.get_or_404(id)
    return jsonify(landlord.to_dict())

@bp.route('/landlords/<int:id>', methods=['PUT'])
@login_required
def update_landlord(id):
    landlord = Landlord.query.get_or_404(id)
    data = request.get_json()
    landlord.name = data.get('name', landlord.name)
    landlord.phone = data.get('phone', landlord.phone)
    landlord.email = data.get('email', landlord.email)
    landlord.address = data.get('address', landlord.address)
    landlord.contract = data.get('contract', landlord.contract)
    db.session.commit()
    return jsonify(landlord.to_dict())

@bp.route('/landlords/<int:id>', methods=['DELETE'])
@login_required
def delete_landlord(id):
    landlord = Landlord.query.get_or_404(id)
    db.session.delete(landlord)
    db.session.commit()
    return '', 204

# CRUD for Tenants
@bp.route('/tenants', methods=['GET'])
@login_required
def get_tenants():
    tenants = Tenant.query.all()
    return jsonify([tenant.to_dict() for tenant in tenants])

@bp.route('/tenants', methods=['POST'])
@login_required
def create_tenant():
    data = request.get_json()
    tenant = Tenant(
        name=data['name'],
        phone=data.get('phone'),
        email=data['email'],
        property_address=data.get('property_address'),
        landlord_id=data['landlord_id']
    )
    db.session.add(tenant)
    db.session.commit()
    return jsonify(tenant.to_dict()), 201

@bp.route('/tenants/<int:id>', methods=['GET'])
@login_required
def get_tenant(id):
    tenant = Tenant.query.get_or_404(id)
    return jsonify(tenant.to_dict())

@bp.route('/tenants/<int:id>', methods=['PUT'])
@login_required
def update_tenant(id):
    tenant = Tenant.query.get_or_404(id)
    data = request.get_json()
    tenant.name = data.get('name', tenant.name)
    tenant.phone = data.get('phone', tenant.phone)
    tenant.email = data.get('email', tenant.email)
    tenant.property_address = data.get('property_address', tenant.property_address)
    tenant.landlord_id = data.get('landlord_id', tenant.landlord_id)
    db.session.commit()
    return jsonify(tenant.to_dict())

@bp.route('/tenants/<int:id>', methods=['DELETE'])
@login_required
def delete_tenant(id):
    tenant = Tenant.query.get_or_404(id)
    db.session.delete(tenant)
    db.session.commit()
    return '', 204

# Auth Routes
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('api.get_landlords'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('api.get_landlords'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    
    return render_template('login.html', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('api.login'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('api.get_landlords'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('api.login'))
    
    return render_template('register.html', form=form)


