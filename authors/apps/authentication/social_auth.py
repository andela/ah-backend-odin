
from .serializers import RegistrationSerializer
from .models import User

def create_user(strategy, details, backend, user=None, *args, **kwargs):

    exists= User.objects.filter(username=details.get("username"), provider=backend.name).exists()
    if exists:
        return {'is_new':False}
    

    serializer=RegistrationSerializer(data={

        "username": details.get('username'),
        "email": details.get('email'),
        "provider": backend.name,
        "password":"Secret2018!"


    })

    serializer.is_valid(raise_exception=True)

    serializer.save()

    return {
        'is_new': True,
        'user': serializer.instance
    }

