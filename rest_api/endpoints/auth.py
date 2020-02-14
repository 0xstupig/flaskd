from flask import Blueprint, request, g

from actions.reset_token import reset_token_action
from actions.session import session_action
from actions.user import user_action
from rest_api.wrapper import SuccessResponse
from rest_api.decorators import is_authenticated
from models.authorization.user import User
from actions.blacklist_token import blacklist_token_action
from services.email import email_service
from services.facebook import facebook_service
from services.google import google_service
from utilities.exception import BadRequestException, DuplicateException, \
    UnauthorizedException, ErrorCode, MissingFieldException
from schemas.user import user_response_schema

auth_ctrl = Blueprint(name='auth_ctrl', import_name=__name__, url_prefix='/auth')


@auth_ctrl.route('/_register', methods=['POST'])
def register():
    data = request.get_json()
    user = user_action.register(data)
    session = session_action.generate_session(user)
    access_token = session_action.generate_access_token(user)

    return SuccessResponse({
        'access_token': access_token,
        'refresh_token': session.token,
        'user': user_response_schema.dump(user)
    }, 200)


@auth_ctrl.route('/_login', methods=['POST'])
def login():
    data = request.get_json()

    user = user_action.login(data['email'], data['password'])
    if user is None:
        raise UnauthorizedException()

    session = session_action.generate_session(user)
    access_token = session_action.generate_access_token(user, session)

    return SuccessResponse({
        'access_token': access_token,
        'refresh_token': session.token,
        'user': user_response_schema.dump(user)
    }, 200)


@auth_ctrl.route('/_logout', methods=['POST'])
@is_authenticated
def logout():
    payload = g.payload

    if 'session' in payload:
        session_action.remove_session(payload['custom:session'])

    blacklist_token_action.add(payload['jti'])

    return SuccessResponse({}, 200)


@auth_ctrl.route('/_access_tokens', methods=['POST'])
def generate_access_token():
    data = request.get_json()
    if ('refresh_token' not in data) or ('user_id' not in data):
        raise UnauthorizedException()

    user = User.query.get(data['user_id'])
    if user is None:
        raise UnauthorizedException()

    access_token = session_action.regenerate_access_token(data['refresh_token'], user)

    return SuccessResponse({
        'access_token': access_token,
    }, 200)


@auth_ctrl.route('/_facebook', methods=['POST'])
def login_with_facebook():
    data = request.get_json()

    if 'access_token' in data:
        access_token = data['access_token']
    else:
        raise MissingFieldException('access_token')

    facebook_user = facebook_service.get_logged_in_user(access_token)

    user = User.query.filter_by(facebook_id=facebook_user['id']).first()
    if user is None:
        if 'email' not in facebook_user:
            raise BadRequestException(code=ErrorCode.NO_VALID_EMAIL)

        user = User.query.filter_by(email=facebook_user['email']).first()
        if user is None:
            user = user_action.register({
                'email': facebook_user['email'],
                'facebook_id': facebook_user['id'],
                'full_name': facebook_user['name']
            })

            avatar = user_action.upload_user_profile(user_id=user.id, url=facebook_user['picture']['data']['url'])
            user_action.update(user_id=user.id, value={'avatar': avatar})
        else:
            avatar = user_action.upload_user_profile(user_id=user.id, url=facebook_user['picture']['data']['url'],
                                                     target_url=user.avatar)
            user_action.update(user_id=user.id, value={'facebook_id': facebook_user['id'], 'avatar': avatar})

    session = session_action.generate_session(user)
    access_token = session_action.generate_access_token(user, session)

    return SuccessResponse({
        'access_token': access_token,
        'refresh_token': session.token,
        'user': user_response_schema.dump(user)
    }, 200)


@auth_ctrl.route('/_google', methods=['POST'])
def login_with_google():
    data = request.get_json()

    if 'access_token' in data:
        access_token = data['access_token']
    else:
        raise MissingFieldException('access_token')

    google_user = google_service.get_logged_in_user(access_token)

    user = User.query.filter_by(google_id=google_user['id']).first()
    if user is None:
        if 'email' not in google_user:
            raise BadRequestException(code=ErrorCode.NO_VALID_EMAIL)

        user = User.query.filter_by(email=google_user['email']).first()
        if user is None:
            user = user_action.register({
                'email': google_user['email'],
                'name': google_user['name'],
                'google_id': google_user['id'],
                'full_name': google_user['name']
            })

            avatar = user_action.upload_user_profile(user_id=user.id, url=google_user['picture'])
            user_action.update(user_id=user.id, value={'avatar': avatar})
        else:
            avatar = user_action.upload_user_profile(user_id=user.id, url=google_user['picture'],
                                                     target_url=user.avatar)
            user_action.update(user_id=user.id, value={'google_id': google_user['id'], 'avatar': avatar})

    session = session_action.generate_session(user)
    access_token = session_action.generate_access_token(user, session)

    return SuccessResponse({
        'access_token': access_token,
        'refresh_token': session.token,
        'user': user_response_schema.dump(user)
    }, 200)


@auth_ctrl.route('/_forgot_password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    # TODO: check MissingFieldException and add field validations here

    user = User.query.filter_by(email=data['email']).first()
    if user is None:
        return SuccessResponse({}, 200)  # Return success response to prevent check used email through forgot password

    reset_token = reset_token_action.generate_reset_token(user)
    email_service.send_forgot_password_email(reset_token)

    return SuccessResponse({}, 200)


@auth_ctrl.route('/_check_reset_code', methods=['POST'])
def check_reset_code():
    data = request.get_json()
    is_valid = reset_token_action.check_reset_token(email=data['email'], token=data['reset_code'])

    return SuccessResponse(is_valid, 200)


@auth_ctrl.route('/_reset_password', methods=['POST'])
def reset_password():
    data = request.get_json()

    reset_token = reset_token_action.check_reset_token(email=data['email'], token=data['reset_code'])
    if reset_token is None:
        raise MissingFieldException('reset_token')

    user = User.query.filter_by(email=data['email']).first()
    user_action.update(user_id=user.id, value={'password': data['password']})

    return SuccessResponse({}, 200)


@auth_ctrl.route('/_check_email_exist', methods=['POST'])
def check_email_exist():
    data = request.get_json()

    exist = User.query.filter_by(email=data['email']).scalar()
    if exist:
        raise DuplicateException()

    return SuccessResponse(False, 200)
