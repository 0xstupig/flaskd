import random
import string
from datetime import datetime, timedelta

from google.auth._helpers import utcnow
from sqlalchemy.orm import with_polymorphic

from actions.base import BaseAction
from models.authorization.base_user import BaseUser
from models.authorization.user import User
from models.authorization.reset_token import ResetToken


class ResetTokenAction(BaseAction):
    def generate_reset_token(self, user):
        reset_token = ResetToken(
            token=self._generate_token(),
            user_id=user.id,
            expire=datetime.utcnow() + timedelta(minutes=5)
        )
        self.db.session.add(reset_token)
        self.db.session.commit()

        return reset_token

    def check_reset_token(self, email, token):
        base_user_and_user = with_polymorphic(BaseUser, User)

        token_ = ResetToken.query \
            .filter(ResetToken.expire > utcnow()) \
            .join(base_user_and_user) \
            .filter(base_user_and_user.User.email == email) \
            .order_by(ResetToken.creation_date.desc()) \
            .first()

        if not token_:
            return False

        return token_.token == token

    def _generate_token(self, size=6):
        chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
        return ''.join(random.SystemRandom().choice(chars) for _ in range(size))


reset_token_action = ResetTokenAction()
