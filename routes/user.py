import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from models.consultation import Consultation
from repositories.consultation_repository import ConsultationRepository
from services.ai_service import GeminiAIService
from services.storage_service import LocalStorageService
from services.monitoring_service import MonitoringService

user_bp = Blueprint('user', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@user_bp.route('/')
@user_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        return redirect(url_for('admin.dashboard'))
        
    consultations = ConsultationRepository.get_by_user_id(current_user.id, limit=5)
    total_consultations = ConsultationRepository.count_by_user_id(current_user.id)
    
    return render_template('user/dashboard.html', consultations=consultations, total_consultations=total_consultations)

@user_bp.route('/consult', methods=['GET', 'POST'])
@login_required
def consult():
    if current_user.role == 'admin':
        return redirect(url_for('admin.dashboard'))
        
    if request.method == 'POST':
        plant_name = request.form.get('plant_name')
        symptoms = request.form.get('symptoms')
        image = request.files.get('image')
        
        if not plant_name or not symptoms:
            flash('Nama tanaman dan gejala wajib diisi!', 'danger')
            return redirect(url_for('user.consult'))
            
        image_url = None
        local_file_path = None
        
        if image and allowed_file(image.filename):
            # Abstraksi Storage Service
            # Saat ini masih lokal, nantinya bisa di-switch ke GCPStorageService()
            storage_service = LocalStorageService(current_app.config['UPLOAD_FOLDER'])
            saved_filename = storage_service.save_file(image)
            image_url = saved_filename
            local_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], saved_filename)
            
        # Panggil AI Service Abstraction
        MonitoringService.log_event("AIConsultationRequest", {"user_id": current_user.id, "plant_name": plant_name})
        ai_result = GeminiAIService.analyze_plant(plant_name, symptoms, local_file_path)
        
        # Simpan ke database menggunakan Repository
        new_consultation = Consultation(
            user_id=current_user.id,
            plant_name=plant_name,
            symptoms=symptoms,
            ai_result=ai_result,
            image_url=image_url
        )
        
        ConsultationRepository.save(new_consultation)
        
        flash('Analisis berhasil! Berikut adalah hasil dari AI.', 'success')
        return redirect(url_for('user.detail', consultation_id=new_consultation.id))
        
    return render_template('user/consult.html')

@user_bp.route('/history')
@login_required
def history():
    if current_user.role == 'admin':
        return redirect(url_for('admin.dashboard'))
        
    consultations = ConsultationRepository.get_by_user_id(current_user.id)
    return render_template('user/history.html', consultations=consultations)

@user_bp.route('/consultation/<int:consultation_id>')
@login_required
def detail(consultation_id):
    consultation = ConsultationRepository.get_by_id(consultation_id)
    
    # Validasi kepemilikan
    if consultation.user_id != current_user.id and current_user.role != 'admin':
        MonitoringService.log_error(f"Unauthorized access attempt by user_id: {current_user.id} to consultation_id: {consultation_id}")
        flash('Anda tidak memiliki akses ke konsultasi ini.', 'danger')
        return redirect(url_for('user.dashboard'))
        
    return render_template('user/detail.html', consultation=consultation)

@user_bp.route('/consultation/<int:consultation_id>/delete', methods=['POST'])
@login_required
def delete(consultation_id):
    consultation = ConsultationRepository.get_by_id(consultation_id)
    
    # Validasi kepemilikan
    if consultation.user_id != current_user.id and current_user.role != 'admin':
        MonitoringService.log_error(f"Unauthorized delete attempt by user_id: {current_user.id} to consultation_id: {consultation_id}")
        flash('Anda tidak memiliki akses untuk menghapus konsultasi ini.', 'danger')
        return redirect(url_for('user.history'))
        
    ConsultationRepository.delete(consultation)
    flash('Riwayat konsultasi berhasil dihapus.', 'success')
    return redirect(url_for('user.history'))
