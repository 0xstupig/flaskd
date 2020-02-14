import uuid
import jwt
from flask import current_app
from datetime import timedelta, datetime

from actions.base import BaseAction
from models.authorization.session import Session
from schemas.session import session_schema
from utilities.exception import InvalidRefreshTokenException


class SessionAction(BaseAction):
    def generate_session(self, user):
        token = uuid.uuid4().hex
        
        session = session_schema.load({'token': token})
        session.user = user
        self.db.session.add(session)
        self.db.session.commit()
        
        return session
    
    def remove_session(self, session_id):
        session = Session.query.get(session_id)
        if session is not None:
            self.db.session.delete(session)
            self.db.session.commit()
    
    def generate_access_token(self, user, session=None):
        payload = {
            'jti': uuid.uuid4().hex,
            'sub': user.id,
            'exp': datetime.now() + timedelta(seconds=current_app.config['JWT_EXPIRE']),
            'custom:user_type': user.type,
            'custom:role': user.role.name,
        }
        
        if session is not None:
            payload['custom:session'] = session.id
        
        return jwt.encode(payload, current_app.config['JWT_SECRET'], algorithm='HS256').decode('utf8')
    
    def regenerate_access_token(self, refresh_token, user):
        session = Session.query. \
            filter_by(token=refresh_token). \
            filter_by(user_id=user.id). \
            first()
        
        if session is None:
            raise InvalidRefreshTokenException()
        
        return self.generate_access_token(user, session)


session_action = SessionAction(model=Session)
