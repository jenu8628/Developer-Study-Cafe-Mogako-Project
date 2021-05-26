from rest_framework import generics, permissions, mixins, serializers, viewsets, status
from django.contrib.auth import login as django_login, logout as django_logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.parsers import FileUploadParser, FormParser, MultiPartParser

from .models import User, Profile
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, ProfileSerializer, ProfileLiteSerializer

from groups.models import Study, Apply
from groups.serializers import StudySerializer

# Register API
class RegisterAPI(generics.GenericAPIView):
    '''
    이메일, 비밀번호, 닉네임을 입력받아 회원을 생성하고, 저장합니다.
    username, password, email은 전부 필수 입력값입니다. 
    '''
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['username'] = request.data['email']
        serializer.validated_data['email'] = request.data['username']
        user = serializer.save()
        return Response({"Successfully created"})
        


class LoginAPI(generics.GenericAPIView):
    '''
    이메일, 비밀번호를 입력받아 로그인합니다.
    username, email은 전부 필수 입력값입니다. 
    '''
    serializer_class = LoginSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token = Token.objects.filter(user=user)

        if token:
            token = Token.objects.get(user=user)
        else:
            token = Token.objects.create(user=user)

        django_login(request, user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token.key
        })


class LogoutAPI(APIView):
    '''
    로그인된 사용자를 로그아웃합니다.
    '''
    def get(self, request, format=None):
        login_user = User.objects.get(email=request.user)
        user_token = Token.objects.get(user=request.user.id)
        django_logout(request)
        
        return Response({"logout"})


class ProfileViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    '''
    사용자의 프로필과 관련된 읽기, 수정하기 기능을 제공합니다.
    '''
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    parser_classes = [MultiPartParser, FormParser] 

    def list(self, request):
        '''
        모든 사용자의 프로필을 조회할 수 있습니다.
        '''
        queryset = Profile.objects.all()
        serializer = ProfileLiteSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        '''
        pk번째 사용자의 프로필을 조회할 수 있습니다.
        사용자가 지금까지 참여한 스터디의 정보들을 조회할 수 있습니다.
        '''
        queryset = Profile.objects.get(id=pk)
        serializer = ProfileSerializer(queryset)
        return Response(serializer.data)

    def update(self, request, pk=None):
        '''
        pk번째 사용자의 프로필을 수정할 수 있습니다.
        현재 로그인된 사용자가 프로필의 대상이 아닌 경우 수정 시도시 오류가 발생합니다.
        '''
        queryset = Profile.objects.get(id=pk)
        data = request.data
        login_user = request.user
        image_before = ProfileSerializer(queryset).data['profile_image']

        if queryset.user != login_user:
            return Response("수정 권한이 없습니다.", status=status.HTTP_400_BAD_REQUEST)

        serializer = ProfileSerializer(queryset, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        image_now = ProfileSerializer(queryset).data['profile_image']
        if image_before != image_now:
            queryset.img_url = 'https://k4b205.p.ssafy.io:7799' + ProfileSerializer(queryset).data['profile_image']
            queryset.save()

        return Response(serializer.data)