from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import *
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny


class RegisterAPI(APIView):
    def post(self, request):
        try:
            serializer = RegisterUserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Registration successful. Please check your email.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
            return Response({'message': 'Registration Failed.', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': 'Internal Server Error', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OtpVerificationAPI(APIView):
    def post(self, request):
        try:
            serializer = otpVerificationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'OTP verificed.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
            return Response({'message': 'Verification Failed.', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': 'Internal Server Error', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginAPI(APIView):
    def post(self, request):
        try:
            serializers = LoginUserSerializer(data=request.data)
            if serializers.is_valid():
                user = serializers.validated_data['user']

                refresh = RefreshToken.for_user(user)
                return Response({'message': 'Login Successful.', 'access': str(refresh.access_token), 'refresh': str(refresh), }, status=status.HTTP_202_ACCEPTED)

            return Response({'message': 'Invalid Username or Password', 'errors': serializers.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': 'Internal Server Error.', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({'error': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logout successful.'}, status=status.HTTP_200_OK)
        except TokenError:
            return Response({'error': 'Token is invalid or expired.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': 'Internal Server Error', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ForgotPasswordOtpAPI(APIView):
    def post(self, request):
        try:
            serializer = ForgotPasswordOtpSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'OTP sent to your email.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ForgotPasswordResetAPI(APIView):
    def post(self, request):
        try:
            serializer = ForgotPasswordResetSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Password reset successful.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RefreshAccessTokenAPI(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response({'error': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            return Response({
                'access_token': access_token
            }, status=status.HTTP_200_OK)

        except TokenError as e:
            return Response({'error': str(e)}, status=401)


class UserDataAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            serializer = UserDataSerializer(user)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Internal Server Error', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateUserAPI(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        try:
            serializer = UpdateUserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Profile updated successfully.', 'data': serializer.data}, status=status.HTTP_200_OK)
            return Response({'message': 'Invalid input.', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': 'Internal Server Error', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeactivateUserAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = DeactivateUserSerializer(data=request.data)
            if serializer.is_valid():
                user = request.user
                user.is_active = False
                user.save()
                return Response({'message': 'Account deactivated successfully.'}, status=status.HTTP_200_OK)
            return Response({'message': 'Invalid request.', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': 'Internal Server Error', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SkillListCreateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        skills = Skill.objects.filter(user=request.user)
        serializer = SkillSerializer(skills, many=True)
        return Response({'skills': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SkillSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Skill added.', 'skill': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SkillDetailAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Skill.objects.get(pk=pk, user=user)
        except Skill.DoesNotExist:
            return None

    def get(self, request, pk):
        skill = self.get_object(pk, request.user)
        if not skill:
            return Response({'error': 'Skill not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = SkillSerializer(skill)
        return Response(serializer.data)

    def put(self, request, pk):
        skill = self.get_object(pk, request.user)
        if not skill:
            return Response({'error': 'Skill not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = SkillSerializer(skill, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Skill updated.', 'skill': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        skill = self.get_object(pk, request.user)
        if not skill:
            return Response({'error': 'Skill not found.'}, status=status.HTTP_404_NOT_FOUND)
        skill.delete()
        return Response({'message': 'Skill deleted.'}, status=status.HTTP_204_NO_CONTENT)


class CVAPI(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # <== ADD THIS LINE

    def get(self, request):
        try:
            cv = request.user.cv
            serializer = CVSerializer(cv)
            return Response({'cv': serializer.data}, status=status.HTTP_200_OK)
        except CV.DoesNotExist:
            return Response({'cv': None}, status=status.HTTP_200_OK)

    def post(self, request):
        # Check if CV already exists
        cv_exists = hasattr(request.user, 'cv')

        if cv_exists:
            # Update existing CV
            cv = request.user.cv
            serializer = CVSerializer(
                cv, data=request.data, context={'request': request})
            is_update = True
        else:
            # Create new CV
            serializer = CVSerializer(
                data=request.data, context={'request': request})
            is_update = False

        if serializer.is_valid():
            serializer.save()
            if is_update:
                return Response({
                    'message': 'CV updated successfully',
                    'cv': serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'message': 'CV uploaded successfully',
                    'cv': serializer.data
                }, status=status.HTTP_201_CREATED)
        return Response({
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            cv = request.user.cv
        except CV.DoesNotExist:
            return Response({'error': 'CV does not exist. Use POST to upload.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CVSerializer(
            cv, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'CV updated.', 'cv': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            cv = request.user.cv
            cv.delete()
            return Response({'message': 'CV deleted.'}, status=status.HTTP_204_NO_CONTENT)
        except CV.DoesNotExist:
            return Response({'error': 'CV does not exist.'}, status=status.HTTP_404_NOT_FOUND)
