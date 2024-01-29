from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from .models import Item
from .serializers import ItemSerializer
from datetime import datetime, timedelta
from django.http import JsonResponse
from .google_calendar import create_calendar_event, get_upcoming_events

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
# from .serializers import LoginSerializer
# from rest_framework_simplejwt.tokens import RefreshToken
from google.oauth2 import id_token
from google.auth.transport import requests
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

def verify_google_token(id_token_string):
    try:
        # Verify the token using Google's API
        id_info = id_token.verify_oauth2_token(id_token_string, requests.Request())
        
        # Extract user information
        user_info = {
            'email': id_info['email'],
            'name': id_info.get('name', ''),
            'photo': id_info.get('photo', ''),
            # Add more user information as needed
        }

        return user_info
    except ValueError as e:
        # Handle invalid token
        return None



@csrf_exempt  # Disable CSRF for this view, handle CSRF in production
@login_required
def google_auth_verify(request):
    if request.method == 'POST':
        id_token_string = request.POST.get('id_token')

        if id_token_string:
            user_info = verify_google_token(id_token_string)

            if user_info:
                # Handle user verification and additional logic
                return JsonResponse({'message': 'User verified successfully', 'user_info': user_info})
            else:
                return JsonResponse({'message': 'Invalid Google token'}, status=400)

        return JsonResponse({'message': 'id_token parameter missing'}, status=400)

    return JsonResponse({'message': 'Invalid request method'}, status=405)

# @api_view(['GET'])
# @authentication_classes([])
# @permission_classes([])
# @login_required
# def google_auth_verify(request):
#     user = request.user

#     # Here you can handle user verification and additional logic
#     # For demonstration purposes, I'm assuming you want to generate JWT tokens

#     refresh = RefreshToken.for_user(user)
#     access_token = str(refresh.access_token)

#     return Response({
#         'message': 'User verified successfully',
#         'access_token': access_token,
#     }, status=status.HTTP_200_OK)


# class LoginView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             username = serializer.validated_data['username']
#             password = serializer.validated_data['password']

#             user = authenticate(request, username=username, password=password)
#             if user:
#                 login(request, user)

#                 # Generate and return access token
#                 refresh = RefreshToken.for_user(user)
#                 access_token = str(refresh.access_token)

#                 return Response({'message': 'Login successful', 'access_token': access_token}, status=status.HTTP_200_OK)
#             else:
#                 return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         logout(request)

#         # Revoke the refresh token to ensure it cannot be used for token refreshing
#         refresh_token = request.data.get('refresh_token')
#         if refresh_token:
#             try:
#                 RefreshToken(refresh_token).blacklist()
#             except Exception as e:
#                 pass  # Handle any exceptions if needed

#         return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)



class ItemListAPIView(generics.ListAPIView):
    queryset = Item.objects.all().order_by('expiration_date')
    serializer_class = ItemSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    # permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # Add color bar indicators based on priority and expiration date
        data = serializer.data
        current_date = datetime.now().date()

        for item in data:
            expiration_date_str  = item['expiration_date']
            priority = item['priority']
                 # Convert expiration_date_str to datetime.date
            expiration_date = datetime.strptime(expiration_date_str, '%Y-%m-%d').date()

            if expiration_date < current_date:
                # Item has expired, set color to red
                item['priority_color'] = 'red'
            elif priority == 0:
                # Low priority, set color to green
                item['priority_color'] = 'green'
            elif priority == 1:
                # Medium priority, set color to yellow
                item['priority_color'] = 'yellow'
            else:
                # High priority, set color to red
                item['priority_color'] = 'red'

        return Response(data)
    
class ItemCreateAPIView(generics.CreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    # permission_classes = [IsAuthenticated]

class ItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    # permission_classes = [IsAuthenticated]

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def set_preferences(request):
    try:
        enable_notifications = request.data.get('enable_notifications', True)
        notification_time = request.data.get('notification_time', '12:00')
        days_before_expiry = request.data.get('days_before_expiry', 3)

        # Implement your preferences logic here
        # For demonstration purposes, just printing the preferences
        print(f"Enable Notifications: {enable_notifications}")
        print(f"Notification Time: {notification_time}")
        print(f"Days Before Expiry: {days_before_expiry}")

        return Response({"message": "Preferences set successfully"}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def scan_barcode(request):
    try:
        barcode = request.data.get('barcode')

        # Implement barcode scanning logic here
        # For demonstration purposes, just printing the scanned barcode
        print(f"Scanned Barcode: {barcode}")

        # You can add more logic here to retrieve item details based on the scanned barcode

        return Response({"message": "Barcode scanned successfully"}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def perform_ocr(request):
    try:
        # Implement OCR logic here
        # For demonstration purposes, just printing a success message
        print("OCR performed successfully")

        # You can add more logic here to extract text from the OCR result

        return Response({"message": "OCR performed successfully"}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def create_event_view(request):
    # Your expiration date logic here
    expiration_date = datetime.datetime.utcnow() + datetime.timedelta(days=7)

    # Example usage
    summary = 'Product Expiry'
    description = 'Product XYZ is expiring soon.'
    start_datetime = expiration_date.isoformat() + 'Z'
    end_datetime = expiration_date.isoformat() + 'Z'

    try:
        created_event = create_calendar_event(summary, description, start_datetime, end_datetime)
        
        return JsonResponse({"message": "Event created successfully", "event": created_event})
    except Exception as e:
        
        return JsonResponse({"error": str(e)}, status=500)
       

    


def get_upcoming_events_view(request):
    upcoming_events = get_upcoming_events()
    return JsonResponse({"upcoming_events": upcoming_events})