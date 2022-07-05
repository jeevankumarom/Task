from rest_framework import serializers
from .models import Account_Module,Destination_Module

### POST API SERIALIZERS
class Account_serializer(serializers.ModelSerializer):
    class Meta:
        model=Account_Module
        fields='__all__'

### POST API SERIALIZERS
class Destination_serializers(serializers.ModelSerializer):
    class Meta:
        model=Account_Module
        fields='__all__'