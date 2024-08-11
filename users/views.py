from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from .permissions import IsAdminOrAuthenticated 
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.html import strip_tags
from django.core.mail import send_mail
from .models import OTP, Users
from rest_framework import status
import random


class GenerateOTPView(APIView):
    permission_classes = [AllowAny]
    """
    API to generate OTP and send it to the email
    """
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"message": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        otp = f'{random.randint(1000, 9999)}' # Generate 4 digit OTP
        try:
            OTP.objects.update_or_create(email=email, defaults={'otp': otp})
        except Exception as e:
            return Response({"message": "Unable to save OTP."}, status=status.HTTP_400_BAD_REQUEST)
        print("OTP", otp)
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp}',
            'from@example.com',
            [email],
            fail_silently=False,
        )
        
        return Response({"message": "OTP sent to email."}, status=status.HTTP_200_OK)
    
class VerifyOTPView(APIView):
    permission_classes = [AllowAny]
    """
    POST API method to verify OTP and generate Auth Token, and PATCH method to logout
    """
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        
        try:
            otp_record = OTP.objects.get(email=email, otp=otp)
        except OTP.DoesNotExist:
            return Response({"message": "Invalid OTP or email."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Getting user object if exists otherwise creating
        user, created = Users.objects.get_or_create(email=email)

        # Generate or get the Auth Token for the user
        token, created = Token.objects.get_or_create(user=user)
        otp_record.delete()  # deleting otp after successful verification
        
        return Response({
            'token': str(token.key),
        })
    
class Logout(APIView):
    permission_classes = [IsAuthenticated]
    """
    API to logout user
    """

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            try:
                token = Token.objects.get(user=user)
                token.delete()  # Deleting token to logout user
                return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
            except Token.DoesNotExist:
                return Response({"detail": "Token does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "User not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)        
        
class UserView(APIView):
    permission_classes = [IsAdminOrAuthenticated]

    def get(self, request):
        """
        API to list all the users for Admin and individual details for users
        """
        user = request.user
        
        if user.is_staff:
            users = Users.objects.filter(is_active=True).all()
        else:
            users = Users.objects.filter(id=user.id).all()

        data = UserSerializer(users, many=True).data
        return Response({
            'data': data,
            'message': 'Data retrieved successfully'
        })
    
    def post(self, request):
        """
        API to add a User
        """
        email = strip_tags(request.data.get('email', ''))
        full_name = strip_tags(request.data.get('full_name', ''))
        mobile = request.data.get('mobile')

        # Validate input
        if not all([email, full_name, mobile]):
            return Response({'data': [],
                             "message": "Email, Full Name, and Mobile are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate email is already registered
        if Users.objects.filter(email=email).exists():
            return Response({'data': [],
                             "message": "Email already registered."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the user
        users = Users.objects.create(
            email=email,
            mobile=mobile,
            full_name=full_name,
        )
        
        # Serialize the created user
        serializer = UserSerializer(users)
        return Response({
            'data': [serializer.data],
            'message': 'User added successfully'
        }, status=status.HTTP_201_CREATED)
    
    def patch(self, request):
        """
        API to update details of all the user for Admin and individual details for user
        """
        user = request.user
        id_ = request.data.get('id')

        # Validate id_ existence
        try:
            users = Users.objects.get(id=id_)
        except Users.DoesNotExist:
            return Response({'data': [],
                            "message": "ID does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        # Clean input data to prevent script injection
        cleaned_data = {key: strip_tags(value) for key, value in request.data.items()}

        # Validate user is authorized to update
        if user.is_superuser:
            # Admin can update all fields
            serializer = UserSerializer(users, data=cleaned_data, partial=True)
        else:
            if users.id != user.id:
                return Response({'data': [],
                                "message": "You are not authorized to update other users."}, status=status.HTTP_403_FORBIDDEN)
            else:
                allowed_fields = ['gender', 'dob', 'address', 'city', 'state', 'country', 'pincode', 'bank_name', 'account_no', 'account_holder_name', 'ifsc_code', 'upi_id']  # Replace with actual field names
                
                # Check if any disallowed fields are present in the request data
                disallowed_fields = [key for key in cleaned_data if key not in allowed_fields and key != 'id']
                if disallowed_fields:
                    return Response({'data': [disallowed_fields],
                                    "message": "You are not allowed to update these fields."}, status=status.HTTP_403_FORBIDDEN)
                
                data = {key: cleaned_data[key] for key in allowed_fields if key in cleaned_data}            
                serializer = UserSerializer(users, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'data': [serializer.data],
                            "message": "Details updated successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({'data': [serializer.data],
                            "message": "Invalid data.", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request):
        """
        API to delete User
        """
        user = request.user
        id_ = request.data.get('id')

        # Validate id_ existence
        try:
            users = Users.objects.get(id=id_)
        except Users.DoesNotExist:
            return Response({'data': [],
                            "message": "ID does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        if users and users.is_active == True:
            users.is_active = False
            users.save()
            serializer = UserSerializer(users)
        else:
            return Response({'data': [],
                            "message": "User already deleted."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'data': [serializer.data],
            'message': 'User deleted successfully'
        })