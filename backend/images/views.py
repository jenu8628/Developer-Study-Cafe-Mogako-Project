from rest_framework import viewsets
from rest_framework.parsers import FileUploadParser, FormParser, MultiPartParser
from rest_framework.response import Response

from .models import Image
from .serializers import ImageSerializer
# Create your views here.


class ImageViewSet(viewsets.ModelViewSet):
    '''
    사진을 전송받으면 해당 사진을 서버에 저장하고, 해당 이미지의 URL을 돌려줍니다.
    해당 URL을 클릭하면 이미지를 확인할 수 있습니다.
    '''
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    parser_classes = [MultiPartParser, FormParser] 

    # 해당 코드를 통해 저장된 이미지들을 전부 확인할 수 있습니다.
    # 일시적으로 주석처리하였습니다.
    # 추후 settings.py에서 pagination을 구현해 요청을 보낼 때 params에 추가적으로 인자를 넘겨 몇 개까지 보여줄 것인지 추가할 수 있습니다.
    # def list(self, request):
    #     queryset = Image.objects.all()
    #     serializer = ImageSerializer(queryset, many=True)
    #     return Response(serializer.data)