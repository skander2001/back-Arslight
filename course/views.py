from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Course, Review
from .serializers import CourseSerializer, ReviewSerializer

class CourseListCreateAPIView(APIView):
    def post(self, request):

        # Get the logged-in user

        # Attach the teacher to the request data
        request.data['teacher'] = 1

        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Serializer will handle saving the teacher field
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class ReviewListCreateAPIView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
