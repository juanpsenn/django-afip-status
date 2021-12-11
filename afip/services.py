from afip import models
from afip.clients import get_client


def check_status(save: bool = False) -> bool:
    client = get_client("wsfe")
    r = client.service.FEDummy()

    status = models.Status(
        app=r.AppServer == "OK",
        db=r.DbServer == "OK",
        auth=r.AuthServer == "OK",
    )
    if save:
        status.save()

    return status.is_up()
