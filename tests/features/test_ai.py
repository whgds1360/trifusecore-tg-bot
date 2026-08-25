from pytest import fixture
from features.ai_chat.ai_manager import AiManager
from asyncio import run


@fixture
def load_test_data() -> str:
    return "Привет"


def test_ai_manager(load_test_data) -> None:
    response = run(AiManager.get_response(content=load_test_data))

    assert (response is not None
            and response != ""
            and isinstance(response, str))
