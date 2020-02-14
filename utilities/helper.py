import uuid
from flask_sqlalchemy import get_debug_queries


class Utility(object):
    @staticmethod
    def uuid():
        return str(uuid.uuid4())

    @staticmethod
    def dict2array(obj):
        """
        :param obj: python dictionary object
        :return: array with dict value
        """
        return list(map(lambda x: x[1], obj.items()))

    @staticmethod
    def sql_log():
        info = get_debug_queries()
        for i in info:
            print('\n--------\n')
            print('Query: ', i.statement, i.parameters)
            print('Execute time: ', i.duration)
            print('\n--------\n')

    @staticmethod
    def get_attribute(obj, attribute, default_value=None):
        """
        Get attribute if object is class instance and value of key if object is dicts
        :param obj: object need to retrieve value
        :param attribute: name of attribute
        :param default_value: return default value if none
        :return: value of attribute
        """
        return obj.get(attribute, default_value) if isinstance(obj, dict) else getattr(obj, attribute, default_value)


    @staticmethod
    def safe_bool(value):
        """
        Convert value to boolean
        :param value: a value
        :return: true or false
        """
        if isinstance(value, bool):
            return value
        return True if str(value).lower() in ['yes', 'true', '1'] else False
