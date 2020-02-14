from os import path
from string import Template

from flask_mail import Message, Mail

from schemas.create_business_registration_request import BusinessRegistrationStatus
from utilities.constant import root_dir


class EmailService:
    def __init__(self):
        self._cached_template = {}
        self.sender = Mail()

    def load_body_template(self, name):
        body_template = self._cached_template.get(name, None)
        if body_template is None:
            dir_name = root_dir()
            file_path = path.join(dir_name, 'templates', name)
            try:
                with open(file_path) as fp:
                    body_template = Template(fp.read())
                    self._cached_template[name] = body_template
            except Exception as _:
                raise FileNotFoundError

        return body_template

    def send_forgot_password_email(self, reset_token):
        body_template = self.load_body_template('forgot_password')

        body = body_template.substitute(reset_token=reset_token.token)

        message = Message(
            subject='Reset password',
            recipients=[reset_token.user.email],
            body=body
        )

        self.sender.send(message)

    def registration_notify(self, record_id, restaurant_name, owner_name, email, status):
        body_template = None
        if status == BusinessRegistrationStatus.COMPLETED:
            body_template = self.load_body_template('completed_business_registration')
        elif status == BusinessRegistrationStatus.APPROVED:
            body_template = self.load_body_template('approved_business_registration')
        elif status == BusinessRegistrationStatus.REJECTED:
            body_template = self.load_body_template('rejected_business_registration')

        if body_template:
            body = body_template.substitute(
                owner_name=owner_name,
                restaurant_name=restaurant_name,
            )
            subject = 'GoEat Business Registration {} (#{})'.format(restaurant_name, record_id)

            message = Message(
                subject=subject,
                recipients=[email],
                body=body
            )

            self.sender.send(message)


email_service = EmailService()
