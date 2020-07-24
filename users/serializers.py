from django.contrib.auth import get_user_model

from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields =  "__all__"


class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), write_only=True, allow_null=True, source='role')
    
    class Meta:
        model = get_user_model()

        # fields = ['id','email', 'phone_number', 'first_name', 'last_name',
        # 'role', 'role_id', 'password', 'date_joined']
        fields = "__all__"
        extra_kwargs = {'id': {'read_only': True}, 'password': {'write_only': True}}


    '''
    overwrite create method to use create_users for user objects so as to 
    use password hashing
    '''
    def create(self, validated_data):
        return self.Meta.model.objects.create_user(**validated_data)


class LoginSerializer(TokenObtainPairSerializer):

    '''
    DRF simple-jwt does not update user last login after getting a new token.
    Fix is to subclass the TokenObtainPairSerializer and add the user_id to the
    serializer response data
    '''
    def validate(self, attrs):
        data = super(LoginSerializer, self).validate(attrs)
        data.update({'user': UserSerializer(self.user).data})
        return data