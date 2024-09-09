from django.contrib.auth.models import User, Group
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'groups']
    
    def update(self, instance, validated_data):
        groups_data = validated_data.pop('groups', None)
        instance = super().update(instance, validated_data)

        if groups_data:
            group = Group.objects.get(name=groups_data['name'])
            instance.groups.clear()
            instance.groups.add(group)
        
        return instance
