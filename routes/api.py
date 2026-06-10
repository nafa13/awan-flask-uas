from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from repositories.consultation_repository import ConsultationRepository
from repositories.user_repository import UserRepository

api_bp = Blueprint('api', __name__)

@api_bp.route('/health')
def health_check():
    """
    Endpoint untuk load balancer (ALB/ELB) checking health dari backend VPC.
    """
    return jsonify({
        "status": "success",
        "message": "FarmAssist AI API is running"
    }), 200

@api_bp.route('/consultations', methods=['GET'])
@login_required
def get_consultations():
    """
    Mengembalikan daftar konsultasi user saat ini dalam bentuk JSON.
    Berguna jika Frontend VPC (React/Vue) dipisah.
    """
    consultations = ConsultationRepository.get_by_user_id(current_user.id)
    data = []
    for c in consultations:
        data.append({
            "id": c.id,
            "plant_name": c.plant_name,
            "symptoms": c.symptoms,
            "ai_result": c.ai_result,
            "image_url": c.image_url,
            "created_at": c.created_at.isoformat()
        })
    return jsonify({"status": "success", "data": data}), 200
