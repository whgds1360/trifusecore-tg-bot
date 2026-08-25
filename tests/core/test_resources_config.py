from pytest import fixture
from pathlib import Path
from core.resources_manager import ResourcesManager


@fixture
def load_test_data() -> Path:
    return Path(__file__).parent.parent.joinpath("configs_for_tests", "config.env")


def test_resource_manager(load_test_data) -> None:
    ResourcesManager.load_config(env_path=load_test_data)

    assert (ResourcesManager.AI_API_KEY is not None
            and ResourcesManager.AI_API_KEY != "")

    assert (ResourcesManager.DB_URL is not None
            and ResourcesManager.DB_URL != "")

    assert (ResourcesManager.TG_TOKEN is not None
            and ResourcesManager.TG_TOKEN != "")
