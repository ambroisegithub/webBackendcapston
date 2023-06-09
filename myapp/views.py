
from django.shortcuts import render
from rest_framework import generics
from .models import MenuItem
from .serializers import  MenuItemSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import UserSerializer
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

class MenuItemView(generics.ListCreateAPIView):
    
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    
class SingletMenuItemView(generics.RetrieveUpdateAPIView,generics.DestroyAPIView):
    
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    

@api_view(['GET', 'POST'])
def menu_items(request):
    if request.method == 'GET':
        items = MenuItem.objects.all()  
        serialized_items = MenuItemSerializer(items, many=True)
        return Response(serialized_items.data)
    elif request.method == 'POST':
        reservation_data = request.data.get('reservation_data')
        reservation_slot = request.data.get('reservation_slot')

        # Check if reservation already exists with the same data and slot
        existing_reservation = MenuItem.objects.filter(reservation_data=reservation_data, reservation_slot=reservation_slot).first()
        if existing_reservation:
            return Response({"error": "Reservation already exists for the same data and slot."}, status=status.HTTP_400_BAD_REQUEST)

        serialized_items = MenuItemSerializer(data=request.data)
        serialized_items.is_valid(raise_exception=True)
        serialized_items.save()
        return Response(serialized_items.data, status=status.HTTP_201_CREATED)

    # return Response(items.values())
 
# handling single items
  
  
def single_items(request,id):
    items = get_object_or_404(MenuItem, pk=id)
    serialized_items = MenuItemSerializer(items)
    return Response(serialized_items.data)     
 
#  handling html
def base(request):
    return render(request,'base.html')
def allreservations(request):
    return render(request,'allreservations.html')




class UserSignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            password2 = serializer.validated_data['password2']

            if User.objects.filter(username=username).exists():
                return Response({'error': 'Username is already taken.'}, status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(email=email).exists():
                return Response({'error': 'Email is already taken.'}, status=status.HTTP_400_BAD_REQUEST)

            if password != password2:
                return Response({'error': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create_user(username=username, email=email, password=password)
            token, _ = Token.objects.get_or_create(user=user)

            response_data = {
                'message': 'User created successfully.',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                },
                'token': token.key
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

       
class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)

            response_data = {
                'message': 'User logged in successfully.',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                },
                'token': token.key
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        
        
class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)     
    
    
#  handling html
def base(request):
    return render(request,'base.html')
def allreservations(request):
    return render(request,'allreservations.html') 

def signup(request):
    return render(request,'signup.html')  

def login(request):
    return render(request,'login.html')      