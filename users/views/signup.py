from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import UserSignUpSerializer


class UserSignUpView(APIView):
    """
    date : 2022-07-05
    writer : 김동규
    """
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
         