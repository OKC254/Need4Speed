from .forms import VideoForm 
from django.core import serializers 
from django.http import JsonResponse 
from .models import VideoUpload
from .serializers import VideoUploadSerializer
import json
from django.shortcuts import render, redirect , HttpResponse
from django.contrib import messages 

#class uploadVideo(APIView):
    #def get(self, request):
        #pass
    
    #def post(self, request):
        #file = request.FILES['video']
        #file_name = file.name
        #destination = 'media/'
        #output = f'{destination}{file_name}'
        #print(file_name)
        #fn = open(output, 'wb+')
        #for chunk in file.chunks():
            #fn.write(chunk)
        #fn.close()
        #return HttpResponse("%s is uploaded to the server successfully" % file_name)

#class VideoUploadAPIView(APIView):
        #parser_classes = (MultiPartParser, FormParser)
        #serializer_class = VideoUploadSerializer

        #def post(self, request, *args, **kwargs):
            #serializer = self.serializer_class(data=request.data)
            #if serializer.is_valid():
                #serializer.save()
                #return Response(
                # serializer.data,
                # status = status.HTTP_201_CREATED
                # )
            #return Response(
            # serializer.errors,
            # status = status.HTTP_400_BAD_REQUEST
            # )


def index(request):
    return render(request, 'index.html')

def upload(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        print(request.FILES)
        if form.is_valid():
            form.save()
        return redirect(index)
    return render(request, 'upload.html', {'form': VideoForm})



#class VideoFormView(generics.CreateAPIView):
    #serializer_class = VideoUploadSerializer
    #queryset = VideoUpload.objects.all()

    #def create(self, request, *args, **kwargs):
        #serializers = self.get_serializer(data = request.data)
        #serializers.is_valid(raise_exception = True)
        #caption = serializers.validated_data['caption']
        #videofile = serializers.validated_data['videofile']
        #speedlimit = serializers.validated_data['speedlimit']
        #serializers.save()
        #return Response(serializers.data)