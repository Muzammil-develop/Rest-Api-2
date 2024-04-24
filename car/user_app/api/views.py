from rest_framework.views import APIView 
from rest_framework.response import Response
from user_app.api.serializer import RegisterSerializer
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

class Registration_view (APIView):
    # refresh = RefreshToken.for_user (account)
    # data ['token'] = {
        # 'refresh' : str (refresh),
    #     'access' : str (refresh.access_token),
    # }
    def post (self , request):
        serializer = RegisterSerializer (data=request.data)
        if serializer.is_valid ():
            serializer.save ()
            return Response (serializer.data)
        
class Logout_view (APIView):
    authentication_classes = ['TokenAuthentication']
    def post (self , request) :
        request.user.auth_token.delete ()
        return Response (status=status.HTTP_200_OK)