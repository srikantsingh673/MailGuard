from rest_framework import serializers
from .models import Users

        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        exclude = ['password', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'last_login']