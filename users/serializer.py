from .models import *
from rest_framework import serializers
from django.contrib.auth import authenticate


class RegisterUserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        style={'input_type': 'password'}, 
        write_only=True,
        required=True
    )
    
    class Meta:
        model = Users
        fields = [
            'first_name', 'last_name', 'username', 'email', 
            'phone', 'password', 'confirm_password', 'address'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'phone': {'required': False},
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({
                "password": "Passwords do not match."
            })
        
        if Users.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({
                "username": "A user with this username already exists."
            })
        
        if Users.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({
                "email": "A user with this email already exists."
            })
        
        return data
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = Users.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            email=validated_data['email'],
            phone=validated_data.get('phone', ''),
            password=validated_data['password'],
            address=validated_data['address'],
            is_active=True  # Activate immediately - no OTP needed
        )
        return user


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError({
                "error": "Username and password are required."
            })

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError({
                "error": "Invalid username or password."
            })

        if not user.is_active:
            raise serializers.ValidationError({
                "error": "Your account is inactive. Please contact support."
            })

        data['user'] = user
        return data


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'username', 'phone', 'address']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({
                "confirm_password": "New passwords do not match."
            })
        return data


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'skill_name']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class CVSerializer(serializers.ModelSerializer):
    class Meta:
        model = CV
        fields = ['id', 'cv_file']
    
    def validate_cv_file(self, value):
        if not value.name.lower().endswith('.pdf'):
            raise serializers.ValidationError("Only PDF files are allowed.")
        return value

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class UserDataSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    cv = CVSerializer(read_only=True)

    class Meta:
        model = Users
        fields = [
            'id', 'first_name', 'last_name', 'username', 'email', 
            'phone', 'address', 'skills', 'cv'
        ]
