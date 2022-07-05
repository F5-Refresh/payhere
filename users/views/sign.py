from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView, status
from rest_framework_simplejwt.tokens import RefreshToken
from users.serializers import UserInfoSerializer, UserSignInSerializer

# Create your views here.


class UserSignInView(APIView):
    """로그인 구현 View

    Writer: 조병민
    Date: 2022-07-05

    Post 메서드를 통해 로그인자격증명을 하며 자격증명 성공 시 토큰을 발급해준다.

    param :
        email       - 이메일 주소
        password    - 비밀번호
    """

    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=UserSignInSerializer, responses={201: UserInfoSerializer})
    def post(self, request):
        serializer = UserSignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.user_signin, status=status.HTTP_200_OK)


class UserSignOutView(APIView):
    """로그아웃 구현 view

    Writer: 조병민
    Date: 2022-07-05

    refresh_token을 받아 해당 토큰을 폐기한다.

    param :
        refresh_token   - 토큰
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=UserSignInSerializer, responses={201: UserInfoSerializer})
    def post(self, request):
        Refresh_token = request.data["refresh_token"]
        token = RefreshToken(Refresh_token)
        token.blacklist()
        return Response({"detail": "success, signout"}, status=status.HTTP_200_OK)
