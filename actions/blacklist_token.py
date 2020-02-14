from actions.base import BaseAction
from models.authorization.blacklist_token import BlacklistToken


class BlacklistTokenAction(BaseAction):
    def check(self, token_id):
        token = self.model.query.filter_by(token_id=token_id).first()
        return token is not None

    def add(self, token_id):
        token_entity = BlacklistToken(token_id=token_id)
        self.db.session.add(token_entity)
        self.db.session.commit()


blacklist_token_action = BlacklistTokenAction(model=BlacklistToken)

