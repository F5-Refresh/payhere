from account_books.models import AccountBook, AccountCategory, AccountDetail
from account_books.serializers import AccountDetailPostSerializer, AccountDetailSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class AccountBookDetailView(APIView):

    '''가계부 내역 구현 View

    writer : 남효정
    date : 2022-07-08

    가계부 내역의 CRUD 구현
    GET: 가계부 내역 전체 리스트
    POST: 가계부 내역 생성
    PATCH: 가계부 내역 수정
    detail.GET: 가계부 내역 상세조회
    toggle_active.PATCH: 가계부 내역 삭제, 복구
    '''

    serializer_class = AccountDetailSerializer
    permission_classes = [IsAuthenticated]

    # 가계부 내역 전체 리스트: 가계부 id를 받고, 해당 가계부의 전체 내역을 보여줍니다. + 쿼리스트링으로 delete_flag 여부에 따른 리스트 필터링 가능.
    @swagger_auto_schema(responses={200: AccountDetailSerializer})
    def get(self, request, book_id):
        account_book = get_object_or_404(AccountBook, id=book_id, user=request.user.id)
        account_details = account_book.account_details.filter(delete_flag=request.GET.get('deleted', False))
        serializer = AccountDetailSerializer(account_details, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 가계부 내역 생성: 가계부 id를 받고, 해당 가계부에서 내역을 작성합니다. + 해당하는 카테고리가 없을 경우 에러가 발생합니다.
    @swagger_auto_schema(request_body=AccountDetailPostSerializer, responses={200: AccountDetailPostSerializer})
    def post(self, request, book_id):

        # 카테고리 id로 객체를 찾아서 가져옵니다. / 유효하지 않는 카테고리일 경우 404 에러가 나옵니다.
        category = AccountCategory.objects.filter(
            user=request.user.id, id=request.data.get('account_category'), delete_flag=False
        ).first()
        serializer = AccountDetailPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 가계부 내역 수정: 가계부 id, 가계부 내역 id를 받고 해당되는 단일 내역을 수정합니다.
    @swagger_auto_schema(request_body=AccountDetailPostSerializer, responses={200: AccountDetailPostSerializer})
    def patch(self, request, book_id, accounts_id):
        account_book = get_object_or_404(AccountBook, id=book_id, user=request.user.id)  # 가계부
        account_detail = get_object_or_404(AccountDetail, account_book=account_book.id, id=accounts_id)  # 가계부 내역
        serializer = AccountDetailPostSerializer(account_detail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 가계부 내역 상세조회: 가계부 id, 가계부 내역 id를 받고 해당되는 단일 내역을 보여줍니다.
    @api_view(['GET'])
    @swagger_auto_schema(responses={200: AccountDetailPostSerializer})
    def detail(request, book_id, accounts_id):
        account_book = get_object_or_404(AccountBook, id=book_id, user=request.user.id)  # 가계부
        account_detail = get_object_or_404(AccountDetail, account_book=account_book.id, id=accounts_id)  # 가계부 내역
        serializer = AccountDetailSerializer(account_detail)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 가계부 내역 삭제, 복구: delete_flag 상태만 변경해서 삭제를 구현했습니다.
    @api_view(['PATCH'])
    @swagger_auto_schema(request_body={}, responses={200: {}})
    def toggle_active(request, book_id, accounts_id):
        account_book = get_object_or_404(AccountBook, id=book_id, user=request.user.id)  # 가계부
        account_detail = get_object_or_404(AccountDetail, account_book=account_book.id, id=accounts_id)  # 가계부 내역
        account_detail.toggle_active()
        return Response(account_detail.delete_message, status=status.HTTP_200_OK)
