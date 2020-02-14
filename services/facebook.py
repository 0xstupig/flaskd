import requests
from requests import HTTPError

from utilities.exception import BadRequestException, ErrorCode


class FacebookService:
    def get_logged_in_user(self, access_token):
        try:
            request = requests.get('https://graph.facebook.com/me', {
                "access_token": access_token,
                "fields": "email,last_name,first_name,id,name,picture"
            })

            request.raise_for_status()

            return request.json()
        except HTTPError as err:
            if 400 <= err.response.status_code < 500:
                raise BadRequestException(code=ErrorCode.INVALID_TOKEN)

            raise err


facebook_service = FacebookService()
