from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from repositories.user_repository import UserRepository
from repositories.consultation_repository import ConsultationRepository

admin_bp = Blueprint('admin', __name__)

# Dekorator untuk memastikan hanya admin yang bisa akses
def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Anda tidak memiliki akses ke halaman ini.', 'danger')
            return redirect(url_for('user.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    total_users = UserRepository.get_total_users('user')
    total_consultations = ConsultationRepository.get_total_count()
    popular_plants = ConsultationRepository.get_popular_plants(limit=5)
    recent_consultations = ConsultationRepository.get_recent(limit=10)
    
    return render_template('admin/dashboard.html', 
                           total_users=total_users,
                           total_consultations=total_consultations,
                           popular_plants=popular_plants,
                           recent_consultations=recent_consultations)
