from afip import models
from datetime import datetime


def list_check_history():
    today = datetime.now()
    history = models.Status.objects.filter(
        created_at__month=today.month, created_at__year=today.year
    )
    return history.order_by("-created_at")
