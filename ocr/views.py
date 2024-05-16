# In views.py
import json
from datetime import time

from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import codecs

class OCRView(APIView):
    def post(self, request):
        # Add your OCR logic here
        endpoint = 'https://dyslexiaforthewin.cognitiveservices.azure.com/'
        subscription_key = '4450bab3e7c14b03b3af039979aedc34'
        text_recognition_url = endpoint + "vision/v3.2/read/analyze"

        # Read image data from the request
        image_data=request.data['file']
        language = request.data['language']



        headers = {
            'Ocp-Apim-Subscription-Key': subscription_key,
            'Content-Type': 'application/octet-stream',
            'Accept': 'application/json',
            'language': language  # Assuming Arabic language
        }

        # Make the API call with the image data
        response = requests.post(text_recognition_url, headers=headers, data=image_data)
        response.raise_for_status()
        analysis = {}

        poll = True
        while poll:
            response_final = requests.get(
                response.headers["Operation-Location"], headers=headers)
            analysis = response_final.json()


            if "analyzeResult" in analysis:
                poll = False
            if "status" in analysis and analysis["status"] == "failed":
                poll = False

        paragraphs = []
        if "analyzeResult" in analysis:
            # Extract the recognized text, with bounding boxes.
            lines = analysis["analyzeResult"]["readResults"][0]["lines"]

            # Accumulate the text from all lines into a single paragraph
            paragraph = ""
            for i, line in enumerate(lines):
                text = line["text"]

                # Check if the text is in Unicode escape sequences
                if "\\u" in text:
                    # Convert Unicode escape sequences to readable text
                    text = codecs.decode(text, 'unicode-escape')

                # Concatenate the text to the paragraph
                paragraph += text + " "

            # Add the paragraph to the list of paragraphs
            paragraphs.append(paragraph)

        response_data = {'paragraphs': paragraphs}
        return JsonResponse(response_data, status=200)
