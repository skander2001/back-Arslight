import base64
import json
import os

import requests
from django.http import JsonResponse
from rest_framework import status, views, permissions

class GenerateImageAPIView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        # Set up the Stability.ai API endpoint and headers
        path = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
        image_folder = '/Users/skander/Desktop/pi/front/src/generated_images'
        headers = {
            "Accept": "application/json",
            "Authorization": "Bearer sk-Pp4IryhwERHJva77wKtKT2RdD5x2SKFpsyJZshGLd86tkc4b",
            "Content-Type": "application/json",
        }

        # Set up the request body
        text_prompt = request.data.get("text_prompt")
        if not text_prompt:
            return JsonResponse({"error": "Missing 'text_prompt' field in request data."}, status=status.HTTP_400_BAD_REQUEST)

        body = {
            "text_prompts": [{"text": text_prompt, "weight": 1}],
            "samples": 1,
            "cfg_scale": 5,
            "width": 1024,
            "height": 1024,
            "steps": 40,
            "seed": 0,
        }

        # Make the API request
        response = requests.post(path, headers=headers, data=json.dumps(body))

        # Check for a successful response
        if response.status_code != 200:
            return JsonResponse({"error": f"Non-200 response: {response.text}"})

        # Process and save the image artifacts
        response_json = response.json()
        artifacts = response_json["artifacts"]
        for idx, artifact in enumerate(artifacts):
            base64_image = artifact["base64"]
            image_data = base64.b64decode(base64_image)
            filename = f"txt2img_{artifact['seed']}.png"
            file_path = os.path.join(image_folder, filename)
            with open(file_path, "wb") as f:
                f.write(image_data)

        # Encode the image data as base64
        with open(file_path, "rb") as f:
            encoded_image_data = base64.b64encode(f.read()).decode("utf-8")

        # Return a JSON response with the filename and base64-encoded image data
        return JsonResponse({"filename": filename, "image_data": encoded_image_data})
