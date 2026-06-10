from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import bcrypt
from models.user import User
from repositories.user_repository import UserRepository
from services.monitoring_service import MonitoringService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('user.dashboard'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = UserRepository.get_by_email(email)
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            MonitoringService.log_event("UserLogin", {"user_id": user.id, "role": user.role})
            flash('Login berhasil!', 'success')
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            if user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('user.dashboard'))
        else:
            MonitoringService.log_error(f"Failed login attempt for email: {email}")
            flash('Login gagal. Periksa kembali email dan password Anda.', 'danger')
            
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard'))
        
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Password dan konfirmasi password tidak cocok!', 'danger')
            return redirect(url_for('auth.register'))
            
        existing_user = UserRepository.get_by_email(email)
        if existing_user:
            flash('Email sudah terdaftar. Silakan gunakan email lain.', 'warning')
            return redirect(url_for('auth.register'))
            
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(name=name, email=email, password_hash=hashed_password, role='user')
        
        UserRepository.save(new_user)
        MonitoringService.log_event("UserRegistered", {"email": email})
        
        flash('Registrasi berhasil! Silakan login.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    MonitoringService.log_event("UserLogout", {"user_id": current_user.id})
    logout_user()
    flash('Anda telah berhasil logout.', 'success')
    return redirect(url_for('auth.login'))
