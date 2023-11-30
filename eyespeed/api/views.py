from .forms import VideoForm 
from django.core import serializers 
from django.http import JsonResponse 
from .models import VideoUpload
from .serializers import VideoUploadSerializer
import json, cv2, os, datetime
from django.shortcuts import render, redirect , HttpResponse
from django.contrib import messages 
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
from .helper import get_vehicle, read_license_plate, write_csv

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
            vid = request.FILES.get('videofile').name
            form.save()
        CONFIDENCE_THRESHOLD = 0.6
        GREEN = (0, 255, 0)
        WHITE = (255, 255, 255)
        results = {}
        tracker = DeepSort(max_age=50)
        detect_model = "api/models/vehicle_detect.pt"
        vehicle_detect = YOLO(detect_model)
        license_model = "api/models/license.pt"
        license_detect = YOLO(license_model)
        vid_path = os.path.join('media', vid)
        cap = cv2.VideoCapture(vid_path)
        frame_nmr = -1
        while cap.isOpened():
            frame_nmr += 1
            ret, frame = cap.read()
            if ret:
                results[frame_nmr] = {}
                detections = vehicle_detect(frame)[0]
                # print(detections)
                detections_ = []
                for detection in detections.boxes.data.tolist():
                    x1, y1, x2, y2, score, class_id = detection
                    confidence = score
                    if float(confidence) < CONFIDENCE_THRESHOLD:
                        continue
                    x1 = int(x1)
                    y1 = int(y1)
                    x2 = int(x2)
                    y2 = int(y2)
                    detections_.append([[x1, y1, x2, y2], score])
                tracks = tracker.update_tracks(detections_, frame=frame)
                # print(tracks)
                for track in tracks:
                    if not track.is_confirmed():
                        continue
                    # track_id = track.track_id

                    # Gets current position in bounding box format `(min x, miny, max x, max y)
                    # returns the bounding box
                    # ltrb = track.to_ltrb()

                    # x1, y1, x2, y2 = int(ltrb[0]), int(ltrb[1]), int(ltrb[2]), int(ltrb[3])
                    # bbox = [[x1, x2, y1, y2]]
                license_plates = license_detect(frame)[0]
                for license_plate in license_plates.boxes.data.tolist():
                    x1, y1, x2, y2, score, class_id = license_plate
                    confidence = score
                    if float(confidence) < CONFIDENCE_THRESHOLD:
                        continue
                    xcar1, ycar1, xcar2, ycar2, vehicle_id = get_vehicle(license_plate, tracks)
                    if vehicle_id != -1:
                        license_plate_crop = frame[int(y1):int(y2), int(x1): int(x2), :]
                        license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
                        _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_gray, 64, 255, cv2.THRESH_BINARY_INV)

                        # Visualizing both images
                        # cv2.imshow('Cropped license plate', license_plate_crop)
                        # cv2.imshow('Threshold plate', license_plate_crop_thresh)
                        #
                        # cv2.waitKey(0)
                        license_plate_text, license_plate_text_score = read_license_plate(license_plate_crop_thresh)

                        if license_plate_text is not None:
                            results[frame_nmr][vehicle_id] = {'vehicle': {'bbox': [xcar1, ycar1, xcar2, ycar2]},
                                                            'license_plate': {'bbox': [x1, y1, x2, y2],
                                                                                'text': license_plate_text,
                                                                                'bbox_score': score,
                                                                                'text_score': license_plate_text_score}}
                ######################################
                # SPEED ESTIMATION- yet to be implemented
                ######################################


        # write results
        write_csv(results, './results.csv')
        return redirect(displayvideo)
    return render(request, 'upload.html', {'form': VideoForm})

def displayvideo(request):
    return render(request, 'display.html')

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