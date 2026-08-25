from pytest import fixture
from pathlib import Path
from core.text_config_manager import TextConfigManager


@fixture
def load_test_data() -> Path:
    return Path(__file__).parent.joinpath("configs_for_tests", "config.json")


def test_resource_manager(load_test_data) -> None:
    TextConfigManager.load_config(path=load_test_data)

    config = TextConfigManager.get_config()

    assert (config["main_info"] is not None
            and config["forward_info"] != "")

    assert (config["ai_info"] is not None
            config["forward_info"] != "")

    assert (config["forward_info"] is not None
            and config["forward_info"] != "")

    assert (config["temp_mail_info"] is not None
            and config["temp_mail_info"] != "")
