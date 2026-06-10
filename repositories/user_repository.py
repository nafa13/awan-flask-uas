from models import db
from models.user import User

class UserRepository:
    @staticmethod
    def get_by_id(user_id):
        return User.query.get(int(user_id))
        
    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()
        
    @staticmethod
    def get_total_users(role='user'):
        return User.query.filter_by(role=role).count()
        
    @staticmethod
    def save(user):
        db.session.add(user)
        db.session.commit()
        return user
