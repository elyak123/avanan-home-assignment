import json

from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from slack_bolt.adapter.django import SlackRequestHandler

from avanan.slack.serializers import DeleteMessageSerializer
from avanan.slack.slack_listeners import app
from avanan.slack.utils import delete_message


handler = SlackRequestHandler(app=app)


@csrf_exempt
def event_view(request):
    if request.method == "POST":
        payload = json.loads(request.body)
        if payload.get("challenge"):
            return JsonResponse({'challenge': payload['challenge']})
        else:
            print(payload)
            # SQS message sent in utils
            response = handler.handle(request)
            return response


@csrf_exempt
def delete_message_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        serializer = DeleteMessageSerializer(data=data)
        validity = serializer.is_valid()
        if validity:
            response = delete_message(**data)
            if not isinstance(response, dict):
                response = {"response": response}
            return JsonResponse(response)
        else:
            print(serializer.errors)
