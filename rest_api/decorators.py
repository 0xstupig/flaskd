import jwt
from functools import wraps
from flask import request, current_app, g

from actions.blacklist_token import blacklist_token_action
from actions.permission import permission_action
from utilities.exception import ForbiddenException, UnauthorizedException


def is_authenticated(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'authorization' not in request.headers:
            raise UnauthorizedException()
        
        authorization_info = request.headers['authorization'].split(' ')

        if len(authorization_info) != 2:
            raise UnauthorizedException()

        auth_type, token = authorization_info

        if auth_type != 'Bearer':
            raise UnauthorizedException()
        
        if token is None:
            raise UnauthorizedException()
        
        try:
            payload = jwt.decode(token, current_app.config['JWT_SECRET'], algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise UnauthorizedException()
        except jwt.PyJWTError:
            raise UnauthorizedException()

        # Todo: must load blacklist token into app context or memory cache
        if blacklist_token_action.check(payload['jti']):
            raise UnauthorizedException()
        
        g.payload = payload
        
        return f(*args, **kwargs)
    
    return decorated_function


def is_authorized(permissions):
    def decorator_factory(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            role = g.payload.get('custom:role')
            
            # Backward compatible
            if not role:
                raise ForbiddenException()

            if not permission_action.is_granted(permissions):
                raise ForbiddenException()
            
            return f(*args, **kwargs)
        
        return decorated_function
    
    return decorator_factory


def allow_anonymous(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        g.payload = {'sub': 0}

        if 'authorization' in request.headers:
            authorization_info = request.headers['authorization'].split(' ')

            if len(authorization_info) != 2:
                return f(*args, **kwargs)

            auth_type, token = authorization_info

            if auth_type != 'Bearer':
                return f(*args, **kwargs)

            if token is None:
                return f(*args, **kwargs)

            try:
                payload = jwt.decode(token, current_app.config['JWT_SECRET'], algorithms='HS256')
            except jwt.ExpiredSignatureError:
                return f(*args, **kwargs)
            except jwt.PyJWTError:
                return f(*args, **kwargs)

            if blacklist_token_action.check(payload['jti']):
                return f(*args, **kwargs)

            g.payload = payload

        return f(*args, **kwargs)

    return decorated_function


def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        key = current_app.config['SITEMAP_API_KEY']
        if request.headers.get('x-api-key') and request.headers.get('x-api-key') == key:
            return f(*args, **kwargs)

        raise ForbiddenException()

    return decorated_function
