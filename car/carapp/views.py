from django.shortcuts import render
from .models import Carlist , Showroomlist , Review
from .api_file.serializers import CarSerializer , ShowroomSerializer , ReviewSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.authentication import BasicAuthentication , SessionAuthentication , TokenAuthentication
from rest_framework.permissions import IsAuthenticated , AllowAny , IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.throttling import UserRateThrottle , ScopedRateThrottle
from .api_file.throttling import CarViewThrottle , CarDetailThrottle 
from .api_file.pagination import CarlistPagination

# Create your views here.

class Car_list_view (APIView):
    # authentication_classes = [BasicAuthentication]
    # authentication_classes = [SessionAuthentication]
    # authentication_classes = [TokenAuthentication]
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]
    # permission_classes = [IsAdminUser]
    # throttle_classes = [UserRateThrottle]
    # throttle_classes = [CarViewThrottle , UserRateThrottle]
    throttle_classes = [ScopedRateThrottle]
    # throttle_scope = 'car_list_scope'
    pagination_class = [CarlistPagination]
    
    def get (self , request):
        car = Carlist.objects.all ()
        seralizer = CarSerializer (car , many=True)
        return Response (seralizer.data)
    def post (self , request):
        serializer = CarSerializer (data=request.data)
        if serializer.is_valid ():
            serializer.save ()
            return Response (serializer.data)
        else :
            return Response (serializer.errors)
    
class Car_detail_view (APIView ) :
    # throttle_classes = [CarDetailThrottle , UserRateThrottle]
    def get (self , request , pk) :
        try :
            car = Carlist.objects.get (pk = pk)
        except:
            return Response ({'Error' : 'Car not found'} , status=status.HTTP_404_NOT_FOUND)
        seralizer = CarSerializer (car)
        return Response (seralizer.data)
    
    def put (self , request , pk):
        car = Carlist.objects.get (pk = pk)
        serializer = CarSerializer (car , data=request.data)
        if serializer.is_valid ():
            serializer.save ()
            return Response (serializer.data)
        else : 
            return Response (serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    def delete (self , request , pk):
        car = Carlist.objects.get (pk = pk)
        car.delete ()
        return Response (status=status.HTTP_204_NO_CONTENT)
    
class Showroom_view (APIView):
    def get (self , request):
        showroom = Showroomlist.objects.all ()
        serializer = ShowroomSerializer (showroom , many = True , context={'request' : request})
        return Response (serializer.data)
    
    def post (self , request):
        serializer = ShowroomSerializer (dat = request.data)
        if serializer.is_valid ():
            serializer.save ()
            return Response (serializer.data)
        else:
            return Response (serializer.errors)
        
# class Showroom_viewset (viewsets.ViewSet):
#     def list (self , request):
#         queryset  = Showroomlist.objects.all ()
#         serializer = ShowroomSerializer (queryset , many = True)
#         return Response (serializer.data)
    
#     def retrieve (self , request, pk = None):
#         queryset = Showroomlist.objects.all ()
#         user = get_object_or_404 (queryset , pk =pk)
#         serializer = ShowroomSerializer (user)
        # return Response (serializer.data)
    
    # def create (self , request) :
    #     serializer = ShowroomSerializer (data= request.data)
    #     if serializer.is_valid ():
    #         serializer.save ()
    #         return Response (serializer.data)
    #     else : 
    #         return Response (serializer.errors , status=status.HTTP_400_BAD_REQUEST)

class Showroom_viewset (viewsets.ModelViewSet):
    queryset = Showroomlist.objects.all ()
    serializer_class = ShowroomSerializer
        
class Showroom_detail(APIView):
    def get (self , request , pk):
        try :
            showroom = Showroomlist.objects.get (pk = pk)
        except :
            return Response ({'Error' : "Showroom not found"} , status=status.HTTP_404_NOT_FOUND)
        serializer = ShowroomSerializer (showroom)
        return Response (serializer.data)
    
    def put (self , request , pk):
        showroom = Showroomlist.objects.get (pk = pk)
        serializer = ShowroomSerializer (showroom , data=request.data)
        if serializer.is_valid ():
            serializer.save ()
            return Response (serializer.data)
        else : 
            return Response (serializer.errors , status=status.HTTP_400_BAD_REQUEST)
        
    def delete (self , request , pk):
        showroom = Showroomlist.objects.get (pk = pk)
        showroom.delete ()
        return Response (status= status.HTTP_204_NO_CONTENT) 
    
# class Reviewlist (mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Review.objects.all ()
#     serializer_class = ReviewSerializer

#     def get (self , request , *args , **kwargs):
#         return self.list (request , *args , **kwargs)
    
#     def post (self , request , *args , **kwargs):
#         return self.create (request , *args , **kwargs)
    
# class Review_detail (mixins.RetrieveModelMixin ,
#                      generics.GenericAPIView):
#     queryset = Review.objects.all ()
#     serializer_class = ReviewSerializer

#     def get(self , request , *args , **kwargs):
#         return self.retrieve (request , *args , **kwargs)

class Reviewlist (generics.ListCreateAPIView):
    # queryset = Review.objects.all ()
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        pk = self.kwargs ['pk']
        return Review.objects.filter (car = pk)
    
class Review_create (generics.CreateAPIView):
    serializer_class = ReviewSerializer
    def query_set (self):
        return Review.objects.all ()
    
    def perform_create(self, serializer):
        pk = self.kwargs ['pk']
        cars = Carlist.objects.get (pk = pk)
        useredit = self.request.user
        Review_queryset = Review.objects.filter (car = cars , apiuser = useredit )
        if Review_queryset.exists ():
            raise ValidationError ('You have already review this car')
        serializer.save (car = cars , apiuser = useredit)
    

    

class Review_detail (generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all ()
    serializer_class = ReviewSerializer