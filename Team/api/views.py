from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.middleware.csrf import get_token
from Account.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from Team.api.serializers import EmployeeSerializer
from Team.models import Employee

@api_view(["POST"])
def main_login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    qr_code_token = request.data.get('qr_code_token')  # Token sent from the frontend

    if email and password:
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return Response({'message': 'Login successful'})
        return Response({'error': 'Invalid Email or Password'}, status=status.HTTP_400_BAD_REQUEST)

    elif qr_code_token:
        try:
            user = get_object_or_404(User, qr_code_token=qr_code_token)  # Match the token
            login(request, user)
            return Response({'message': 'Login successful'})
        except User.DoesNotExist:
            return Response({'error': 'Invalid QR Code'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'error': 'Invalid login method'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def logout_user(request):
    logout(request)
    return JsonResponse({'message': 'Logout successful'})


@api_view(["GET"])
def csrf_token_view(request):
    token = get_token(request)
    return JsonResponse({'csrfToken': token})


@api_view(['GET'])
def get_logged_in_user(request):

    if request.user.is_authenticated:

        user = request.user

        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'authenticated': True,
        }
        return Response(user_data)
    else:
        return Response({'authenticated': False})
    
    
    
# create employee view
class EmployeeCreationView(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]