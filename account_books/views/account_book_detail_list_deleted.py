from account_books.models import AccountDetail
from account_books.serializers import AccountDetailSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class AccountBookDetailListDeletedAPI(APIView):

    '''
    date : 2022-07-05
    writer : 남효정

    ------------------

    각 가계부 내역의 삭제내역 리스트 Read(List)를 구현합니다.
    GET: 가계부 내역 삭제 리스트
    '''

    serializer_class = AccountDetailSerializer

    # 가계부 내역 삭제 리스트: 가계부 id를 받고, 해당 가계부에서 삭제된 내역 리스트를 보여줍니다.
    def get(self, request, book_id):
        account_details_deleted = AccountDetail.objects.filter(account_book=book_id, delete_flag=True)
        serializer = AccountDetailSerializer(account_details_deleted, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
