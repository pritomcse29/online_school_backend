from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer , UserSerializer as BaseUserSerializer
from rest_framework import serializers
from django.contrib.auth.models import Group
from .models import User

# from django.contrib.auth.models import User, Group

class GroupSerializer(serializers.ModelSerializer):
        class Meta:
            model = Group
            fields = ('name',) # Only expose the group name
# class UserSerializer(serializers.ModelSerializer):
#         groups = GroupSerializer(many=True, read_only=True) # Nested serializer for groups

#         class Meta:
#             model = User
#             fields = ('id','email','groups')


class UserCreateSerializer(BaseUserCreateSerializer):
    # groups = GroupSerializer(many=True,read_only=True)
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
        
# class UserSerializer(BaseUserSerializer):
#     class Meta(BaseUserSerializer.Meta):
#         ref_name = 'CustomUser'
#         fields =['id','first_name','last_name','email','password','number','address','is_staff']
#         read_only = ['is_staff']


class UserSerializer(BaseUserSerializer):
    groups = GroupSerializer(many=True, read_only=True)

    class Meta(BaseUserSerializer.Meta):
        ref_name = 'CustomUser'
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'password',
            'number',
            'address',
            'is_staff',
            'groups',  # <-- Add this to expose the group names
        ]
        read_only_fields = ['is_staff', 'groups']


