from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer , UserSerializer as BaseUserSerializer
from rest_framework import serializers
from django.contrib.auth.models import Group
from .models import User
class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):

        fields =['id','first_name','last_name','email','password','number','address']

        # def validated_role(self,value):
     
        #     if value=='admin' and  not self.context['request'].user.is_staff:
        #         raise serializers.ValidationError("Only staff users can set the 'admin' role.")
        #     return value
        
        def create(self,validated_data):
            user = User.objects.create_user(**validated_data)
            student_group = Group.objects.get(name='student') 
            user.groups.add(student_group)
            return user
            # role = self.validated_role.pop('role','student')
            # user = self.create(validated_data)
            # user.role = role
            # user.save()
            # return user
        
class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        ref_name = 'CustomUser'
        fields =['id','first_name','last_name','email','password','number','address','is_staff']
        read_only = ['is_staff']




