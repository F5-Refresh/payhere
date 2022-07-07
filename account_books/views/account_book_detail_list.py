from account_books.models import AccountDetail
from account_books.serializers import AccountDetailPostSerializer, AccountDetailSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class AccountBookDetailListAPI(APIView):

    '''
    date : 2022-07-05
    writer : 남효정

    ------------------

    각 가계부 내역의 Create, Read(List)를 구현합니다.
    GET: 가계부 내역 전체 리스트 조회
    POST: 가계부 내역 생성
    '''

    serializer_class = AccountDetailSerializer

    # 가계부 내역 전체 리스트: 가계부 id를 받고, 해당 가계부의 전체 내역을 보여줍니다.
    def get(self, request, book_id):
        account_details = AccountDetail.objects.filter(account_book=book_id)
        serializer = AccountDetailSerializer(account_details, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 가계부 내역 생성: 가계부 id를 받고, 해당 가계부에서 내역을 작성합니다.
    def post(self, request, book_id):
        serializer = AccountDetailPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
