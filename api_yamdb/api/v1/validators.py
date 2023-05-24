from rest_framework.exceptions import ValidationError
from users.models import User


def validate(data):
    if data == 'me':
        raise ValidationError('Недопустимое имя пользователя!')

    if User.objects.filter(email=data['email'],
                           username=data['username']).exists:
        return data

    if User.objects.filter(username=data).exists():
        raise ValidationError('Пользователь с таким именем '
                              'уже зарегистрирован')

    if User.objects.filter(email=data).exists():
        raise ValidationError('Пользователь с такой почтой '
                              'уже зарегистрирован')
    return data
