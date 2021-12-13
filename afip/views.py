from rest_framework import views, serializers
from rest_framework.response import Response

from afip import services, selectors, models
from afip.helpers import is_authenticated

import os
from datetime import datetime


class CheckStatusApi(views.APIView):
    def post(self, request):
        auth = is_authenticated(request.headers.get("Authorization", None))
        if auth:
            status = services.check_status(True)
        else:
            status = services.check_status()
        return Response(
            {
                "request_type": "authenticated" if auth else "anonymous",
                "datetime": datetime.now(),
                "status": status,
            },
            201,
        )


class ListCheckStatusApi(views.APIView):
    def get(self, request):
        history = selectors.show_statistics()
        return Response(
            {"history": list(history)},
            200,
        )
