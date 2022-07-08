from account_books.models import AccountDetail
from account_books.serializers import AccountDetailSerializer
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class AccountBookDetailAPI(APIView):

    '''
    date : 2022-07-05
    writer : 남효정

    ------------------

    각 가계부의 단일 내역을 Read, Update 합니다.
    GET: 가계부 내역 상세조회
    Update: 가계부 내역 수정
    '''

    serializer_class = AccountDetailSerializer
    permission_classes = [IsAuthenticated]

    # 가계부 내역 상세조회: 가계부 id, 가계부 내역 id를 받고 해당되는 단일 내역을 보여줍니다.
    def get(self, request, book_id, accounts_id):
        account_detail = get_object_or_404(AccountDetail, account_book=book_id, id=accounts_id)
        serializer = AccountDetailSerializer(account_detail)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 가계부 내역 수정: 가계부 id, 가계부 내역 id를 받고 해당되는 단일 내역을 수정합니다.
    def patch(self, request, book_id, accounts_id):
        account_detail = get_object_or_404(AccountDetail, account_book=book_id, id=accounts_id)
        serializer = AccountDetailSerializer(account_detail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
