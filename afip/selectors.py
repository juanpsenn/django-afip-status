from afip import models
from datetime import datetime
from django.db.models import Count, Case, When, Value


def list_check_history():
    today = datetime.now()
    history = models.Status.objects.filter(
        created_at__month=today.month, created_at__year=today.year
    )
    return history.order_by("-created_at")


def show_statistics():
    today = datetime.now()
    history = models.Status.objects.filter(
        created_at__month=today.month, created_at__year=today.year
    )
    stats = (
        history.extra({"date": "date(created_at)"})
        .values("date")
        .annotate(down_app=Count(Case(When(app=False, then=Value(1)))))
        .annotate(up_app=Count(Case(When(app=True, then=Value(1)))))
        .annotate(down_db=Count(Case(When(db=False, then=Value(1)))))
        .annotate(up_db=Count(Case(When(db=True, then=Value(1)))))
        .annotate(down_auth=Count(Case(When(auth=False, then=Value(1)))))
        .annotate(up_auth=Count(Case(When(auth=True, then=Value(1)))))
    )
    return stats
