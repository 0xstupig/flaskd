from cloudinary.uploader import upload

from actions.base import BaseAction
from actions.role import ROLE
from models.authorization import Role
from models.authorization.user import User
from schemas.user import user_schema, UserProfileSchema
from utilities import constant
from utilities.exception import EntityNotFoundException, ForbiddenException
from utilities.helper import Utility


class UserAction(BaseAction):
    def register(self, data):
        consumer_role = Role.get_role_by_name(ROLE.Consumer.value)
        fixed_value = {
            'role_id': consumer_role.id,
        }
        validated_data = user_schema.load({
            **data,
            **fixed_value,
        })

        user = User(**validated_data)

        self.db.session.add(user)
        self.db.session.commit()
        
        return user
    
    def login(self, email, password):
        user = User.query.filter_by(email=email).first()
        
        if user is None:
            return None
        
        if not user.verify_password(password):
            return None
        
        return user
    
    def update(self, user_id, value):
        user = User.query.get(user_id)

        if not user:
            raise EntityNotFoundException(user_id, 'User')

        user.update(value)
        self.db.session.commit()

        return user_schema.dump(user)

    def get_user_profile(self, user_id):
        user = User.query.get(user_id)

        if user is None:
            return None

        return UserProfileSchema().dump(user)

    def upload_user_profile(self, user_id, url='', file=None, target_url=''):
        upload_file = url if url else file

        if not target_url:
            public_id = Utility.uuid()
            gallery = '{}/{}'.format(constant.cloudinary_user_url(), user_id)
            upload(upload_file, public_id=public_id, folder=gallery)
            public_id = '{}/{}'.format(gallery, public_id)
        else:
            public_id = target_url
            upload(upload_file, public_id=target_url)

        return public_id

    def update_credential(self, user_id, password, update_password):
        user = User.query.get_or_404(user_id)

        if not user.verify_password(password):
            raise ForbiddenException()

        user.password = update_password
        self.db.session.commit()


user_action = UserAction(model=User)

