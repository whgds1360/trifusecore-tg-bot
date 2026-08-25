from pytest import fixture
from features.temp_mail.temp_mail_manager import TempMailManager
from asyncio import run


@fixture
def load_test_data() -> TempMailManager:
    email = TempMailManager()
    return email


def test_temp_mail(load_test_data) -> None:

    assert (load_test_data.email.email is not None
            and load_test_data.email.email != "")
