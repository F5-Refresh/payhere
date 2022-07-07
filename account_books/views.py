from django.shortcuts import render

# Create your views here.
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from account_books.models import AccountBook
from account_books.serializers import AccountBookCreatePatchSerializer, AccountBookListSerializer


class AccountBookList(APIView):
    """
    date : 2022-07-05
    writer : 전기원
    """
class AccountBookView(APIView):
    def get_object(self, book_id):
        try:
            return AccountBook.objects.get(id=book_id)
        except AccountBook.DoesNotExist:
            Response(status=status.HTTP_404_NOT_FOUND)
            
    def get(self, request):
        queryset = self.get_objects.filter(delete_flag=False)
        serializer = AccountBookListSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AccountBookCreatePatchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    #가계부를 수정합니다.
    def patch(self, request, book_id, format=None):
        queryset = self.get_object(book_id)
        serializer = AccountBookCreatePatchSerializer(queryset, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #가계부의 삭제리스트를 보여줍니다
    @api_view(['GET'])
    def deleted_list(self, format=None):
        queryset = self.get_object.filter(delete_flag=True)
        serializer = AccountBookListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
