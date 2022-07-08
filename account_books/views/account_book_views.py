from account_books.models import AccountBook
from account_books.serializers import AccountBookCreatePatchSerializer, AccountBookListSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class AccountBookView(APIView):
    '''가계부 구현 View

    writer : 전기원
    date : 2022-07-05

    가계부의 CRUD 와 삭제리스트 구현
    '''

    permission_classes = [IsAuthenticated]
    # 가계부를 조회합니다.
    def get(self, request):
        queryset = AccountBook.objects.filter(delete_flag=False)
        serializer = AccountBookListSerializer(queryset, many=True)
        return Response(serializer.data)

    # 가계부를 생성합니다.
    def post(self, request):
        serializer = AccountBookCreatePatchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 가계부를 수정합니다.
    def patch(self, request, book_id, format=None):
        account_book = get_object_or_404(AccountBook, id=book_id)

        serializer = AccountBookCreatePatchSerializer(data=request.data, instance=account_book)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 가계부를 삭제합니다.
    @api_view(['PATCH'])
    def deleted_patch(request, book_id, format=None):
        account_book = get_object_or_404(AccountBook, id=book_id)
        message = '레코드가 복구되었습니다.' if account_book.delete_flag else '레코드가 삭제되었습니다.'
        account_book.toggle_active()
        return Response({'detail': message}, status=status.HTTP_200_OK)

    # 가계부의 삭제리스트를 조회합니다.
    @api_view(['GET'])
    def deleted_list(format=None):
        queryset = AccountBook.objects.filter(delete_flag=True)
        serializer = AccountBookListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
