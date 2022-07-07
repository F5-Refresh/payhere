from account_books.models import AccountCategory, AccountDetail
from account_books.serializers import AccountDetailPostSerializer, AccountDetailSerializer
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


class AccountBookDetailDeleteAPI(APIView):

    '''
    date : 2022-07-07
    writer : 남효정

    ------------------

    각 가계부 내역을 삭제합니다.
    (delete_flag를 이용했기 때문에 실제 DB에서의 삭제가 아니라, delete_flag 상태만 변화하게 됩니다.)
    PATCH: 가계부 내역 삭제
    '''

    serializer_class = AccountDetailSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, book_id, accounts_id):

        # delete_flag 상태만 변경해서 삭제를 구현했습니다.
        account_detail = get_object_or_404(AccountDetail, account_book=book_id, id=accounts_id)
        message = '레코드가 복구되었습니다.' if account_detail.delete_flag else '레코드가 삭제되었습니다.'
        account_detail.toggle_active()
        return Response({'detail': message, 'account_detail': account_detail}, status=status.HTTP_200_OK)


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
    permission_classes = [IsAuthenticated]

    # 가계부 내역 전체 리스트: 가계부 id를 받고, 해당 가계부의 전체 내역을 보여줍니다.
    def get(self, request, book_id):
        account_details = AccountDetail.objects.filter(account_book=book_id)
        serializer = AccountDetailSerializer(account_details, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 가계부 내역 생성: 가계부 id를 받고, 해당 가계부에서 내역을 작성합니다. + 해당하는 카테고리가 없을 경우 에러가 발생합니다.
    def post(self, request, book_id):

        # 카테고리 id로 객체를 찾아서 가져옵니다. / 유효하지 않는 카테고리일 경우 404 에러가 나옵니다.
        category_detail = get_object_or_404(
            AccountCategory, user=request.user.id, id=request.data['account_category'], delete_flag=False
        )

        serializer = AccountDetailPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountBookDetailListDeletedAPI(APIView):

    '''
    date : 2022-07-05
    writer : 남효정

    ------------------

    각 가계부 내역의 삭제내역 리스트 Read(List)를 구현합니다.
    GET: 가계부 내역 삭제 리스트
    '''

    serializer_class = AccountDetailSerializer
    permission_classes = [IsAuthenticated]

    # 가계부 내역 삭제 리스트: 가계부 id를 받고, 해당 가계부에서 삭제된 내역 리스트를 보여줍니다.
    def get(self, request, book_id):
        account_details_deleted = AccountDetail.objects.filter(account_book=book_id, delete_flag=True)
        serializer = AccountDetailSerializer(account_details_deleted, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
