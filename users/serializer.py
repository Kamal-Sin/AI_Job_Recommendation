from .models import *
from rest_framework import serializers
import random
from django.core.mail import send_mail
from django.contrib.auth import authenticate


class RegisterUserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model= Users
        fields= ['first_name','last_name','username', 'email','phone','password','confirm_password','address']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self,validate_data):
        if validate_data['password']!=validate_data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return validate_data
    
    def create(self, validated_data):
        otp=str(random.randint(100000,999999))
        validated_data.pop('confirm_password')

        user=Users.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            password=validated_data['password'],
            address=validated_data['address'],
            otp=otp,
            is_active=False
        )
        
        send_otp_email(user.email, otp)
        return user

def send_otp_email(email, otp):
    subject = 'Verification Otp for E-Commerce Platform'
    message = f'Your verification otp = {otp}'
    from_email = 'nauman1283@gmail.com'
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)


class otpVerificationSerializer(serializers.Serializer):
    email=serializers.CharField()
    otp=serializers.CharField()

    def validate(self, validate_data):
        email = validate_data.get('email')
        otp = validate_data.get('otp')
        user=Users.objects.get(email=email,otp=otp,is_active=False)
        if Users.DoesNotExist:
            serializers.ValidationError("Error")
        validate_data['user']=user
        return validate_data

    def save(self):
        user = self.validated_data['user']
        user.is_active = True
        user.otp = None  
        user.save()
        return user



class LoginUserSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()

    def validate(self, validate_data):
        username=validate_data.get('username')
        password=validate_data.get('password')

        user=authenticate(username=username, password=password)

        if user.DoesNotExist:
            serializers.ValidationError("Error")

        validate_data['user']=user
        return validate_data
    

class ForgotPasswordOtpSerializer(serializers.Serializer):
    email=serializers.EmailField()
    def validate(self, data):
        try:
            email=data.get('email')
            user=Users.objects.get(email=email)
            if not user.is_active:
                raise serializers.ValidationError("User is not active.")
            self.context['user'] = user
            return data
        except Users.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        
    def save(self):
        user=self.context['user']
        otp = str(random.randint(1000, 9999))  
        user.otp = otp
        user.save()
        send_otp_email(user.email, otp)

class ForgotPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=4)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        otp = attrs.get('otp')
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        if new_password != confirm_password:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})

        try:
            user = Users.objects.get(email=email, otp=otp)
        except Users.DoesNotExist:
            raise serializers.ValidationError({"otp": "Invalid OTP or email."})

        attrs['user'] = user
        return attrs

    def save(self):
        user = self.validated_data['user']
        user.set_password(self.validated_data['new_password'])
        user.otp = None  
        user.save()
        return user
    

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'username', 'phone', 'address']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class DeactivateUserSerializer(serializers.Serializer):
    confirm = serializers.BooleanField()

    def validate(self, data):
        if not data.get('confirm'):
            raise serializers.ValidationError({"confirm": "Please confirm account deactivation."})
        return data

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id','skill_name']

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
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'phone', 'address', 'skills', 'cv']