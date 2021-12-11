import factory


class DownStatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "afip.Status"

    app = False
    db = True
    auth = True


class UpStatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "afip.Status"

    app = True
    db = True
    auth = True
