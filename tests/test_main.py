def test_main_imports() -> None:
    from core.resources_manager import ResourcesManager
    from core.text_config_manager import TextConfigManager
    from core.сore import Core

    assert ResourcesManager is not None
    assert TextConfigManager is not None
    assert Core is not None
