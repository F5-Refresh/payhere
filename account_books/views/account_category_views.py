from rest_framework.response import Response
from rest_framework import status
from account_books.models import AccountCategory
from rest_framework.views import APIView
from account_books.serializers import AcoountCategoryPutSerializer, AcoountCategoryPostSerializer, AcoountCategorySerializer
from rest_framework.permissions import  IsAuthenticated

from users.models import User

class AcoountCategoryView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, req):
        account_categorise = AccountCategory.objects.filter(user=req.user.id, delete_flag=False)
        serializer = AcoountCategorySerializer(account_categorise, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, req):
        category_name = req.data.get('category_name')
        account_category = AcoountCategoryPostSerializer(data={'category_name': category_name, 'user': req.user.id})
        if account_category.is_valid():
            account_category.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(account_category.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, req, account_category_id):
        account_category = AccountCategory.objects.filter(id=account_category_id).first()

        if account_category == None:
            return Response({'detail': '레코드가 존재하지 않습니다.'},status=status.HTTP_404_NOT_FOUND)
        
        account_category = AcoountCategoryPutSerializer(data=req.data, instance=account_category)
        if account_category.is_valid():
            account_category.save()
            return Response(status=status.HTTP_200_OK)
        return Response(account_category.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, req, account_category_id):
        account_category = AccountCategory.objects.filter(id=account_category_id).first()
        if account_category == None:
            return Response({'detail': '레코드가 존재하지 않습니다.'},status=status.HTTP_404_NOT_FOUND)
        account_category.toggle_active()
        return Response(status=status.HTTP_200_OK)