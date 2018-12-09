from rest_framework import serializers
from .models import User


class AuthSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uid','telephone','username','data_joined','is_active','is_stuff')





