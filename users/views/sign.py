from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView, status
from rest_framework_simplejwt.tokens import RefreshToken
from users.serializers import UserInfoSerializer, UserSignInSerializer, UserSignUpSerializer


# Create your views here.
class UserSignUpView(APIView):
    """회원가입 구현 View

    Writer: 김동규
    Date: 2022-07-05

    Post 메서드를 통해 회원가입 조건을 만족하면 DB에 회원가입 정보를 저장한다.

    param :
        email       - 이메일 주소
        nickname    - 닉네임
        password    - 비밀번호
    """

    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=UserSignUpSerializer, responses={201: UserSignUpSerializer})
    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class UserSignInView(APIView):
    """로그인 구현 View

    Writer: 조병민
    Date: 2022-07-05

    post: 로그인 자격증명 성공 시 JWT를 발급

    """

    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=UserSignInSerializer, responses={200: UserInfoSerializer})
    def post(self, request):
        serializer = UserSignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.user_signin(data=request.data), status=status.HTTP_200_OK)


class UserSignOutView(APIView):
    """로그아웃 구현 view

    Writer: 조병민
    Date: 2022-07-05

    post: refresh token을 받아 해당 access token을 폐기

    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=UserSignInSerializer, responses={200: UserInfoSerializer})
    def post(self, request):
        Refresh_token = request.data["refresh"]
        token = RefreshToken(Refresh_token)
        token.blacklist()

        return Response({"detail": "success, signout"}, status=status.HTTP_200_OK)
