import factories
import pytest
from afip import services, selectors, models


@pytest.mark.django_db
def test_down_status_check():
    status = factories.DownStatusFactory()
    assert not status.is_up()


@pytest.mark.django_db
def test_up_status_check():
    status = factories.UpStatusFactory()
    assert status.is_up()


@pytest.mark.django_db
def test_status_check_with_save():
    status = services.check_status(True)
    assert type(status) == bool
    assert models.Status.objects.count() == 1


def test_status_check():
    status = services.check_status()
    assert type(status) == bool


@pytest.mark.django_db
def test_list_check_history():
    status = factories.UpStatusFactory.create_batch(2)
    history = selectors.list_check_history()
    assert history.count() == 2
