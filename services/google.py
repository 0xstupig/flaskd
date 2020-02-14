import google.oauth2.credentials as google
from googleapiclient import discovery


class GoogleService:
    def get_logged_in_user(self, access_token):
        credentials = google.Credentials(access_token)
        user_info_service = discovery.build('oauth2', 'v2', credentials=credentials)
        return user_info_service.userinfo().get().execute()


google_service = GoogleService()
