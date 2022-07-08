from account_books.models import AccountCategory
from account_books.serializers import (
    AcoountCategoryPatchSerializer,
    AcoountCategoryPostializer,
    AcoountCategorySerializer,
)
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class AcoountCategoryView(APIView):

    '''카테고리 View

    Writer: 이동연
    Date: 2022-07-05

    카테고리 CRUD를 담당하고 있습니다.
    '''

    permission_classes = [IsAuthenticated]

    # 로그인 처리가 된 사용자의 삭제안된/삭제된 카테고리 리스트를 조회합니다.
    @swagger_auto_schema(responses={200: AcoountCategorySerializer})
    def get(self, req):
        account_categorise = AccountCategory.objects.filter(
            user=req.user.id, delete_flag=req.GET.get('deleted', False)
        )
        serializer = AcoountCategorySerializer(account_categorise, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 카테고리 생성합니다.
    @swagger_auto_schema(request_body=AcoountCategoryPostializer, responses={201: AcoountCategoryPostializer})
    def post(self, req):
        category_name = req.data.get('category_name')
        account_category = AcoountCategoryPostializer(data={'category_name': category_name, 'user': req.user.id})
        if account_category.is_valid():
            account_category.save()
            return Response({'success': '카테고리를 생성하였습니다.'}, status=status.HTTP_201_CREATED)
        return Response(account_category.errors, status=status.HTTP_400_BAD_REQUEST)

    # 카테고리를 수정합니다.
    @swagger_auto_schema(request_body=AcoountCategoryPatchSerializer, responses={200: AcoountCategoryPatchSerializer})
    def patch(self, req, account_category_id):
        account_category = get_object_or_404(AccountCategory, id=account_category_id, user=req.user.id)
        account_category = AcoountCategoryPatchSerializer(data=req.data, instance=account_category)
        if account_category.is_valid():
            account_category.save()
            return Response({'success': '카테고리를 수정하였습니다.'}, status=status.HTTP_200_OK)
        return Response(account_category.errors, status=status.HTTP_400_BAD_REQUEST)

    # 카테고리를 논리 삭제/복구 합니다.
    @api_view(['PATCH'])
    @swagger_auto_schema(request_body={}, responses={200: {}})
    def toggle_active(req, account_category_id):
        account_category = get_object_or_404(AccountCategory, id=account_category_id)
        account_category.toggle_active()
        return Response(account_category.delete_message, status=status.HTTP_200_OK)
