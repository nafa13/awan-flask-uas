from models import db
from models.consultation import Consultation
from sqlalchemy import func

class ConsultationRepository:
    @staticmethod
    def get_by_id(consultation_id):
        return Consultation.query.get_or_404(consultation_id)
        
    @staticmethod
    def get_by_user_id(user_id, limit=None):
        query = Consultation.query.filter_by(user_id=user_id).order_by(Consultation.created_at.desc())
        if limit:
            return query.limit(limit).all()
        return query.all()
        
    @staticmethod
    def count_by_user_id(user_id):
        return Consultation.query.filter_by(user_id=user_id).count()
        
    @staticmethod
    def get_total_count():
        return Consultation.query.count()
        
    @staticmethod
    def get_recent(limit=10):
        return Consultation.query.order_by(Consultation.created_at.desc()).limit(limit).all()
        
    @staticmethod
    def get_popular_plants(limit=5):
        return db.session.query(
            Consultation.plant_name, 
            func.count(Consultation.id).label('total')
        ).group_by(Consultation.plant_name).order_by(func.count(Consultation.id).desc()).limit(limit).all()
        
    @staticmethod
    def save(consultation):
        db.session.add(consultation)
        db.session.commit()
        return consultation

    @staticmethod
    def delete(consultation):
        db.session.delete(consultation)
        db.session.commit()
