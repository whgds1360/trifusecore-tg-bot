from typing import Dict, final

@final
class UtilsManager:
    
    @staticmethod
    def parse_config_for_forward(config_text: str) -> Dict[str, str]:
        """
        Парсит строку конфига с разделителем &
        Пример: LIST_OF_LISTEN=1,2,3&VK_TOKEN=token&VK_COMMUNITY_TOKEN=123
        Возвращает словарь с параметрами
        """
        config_dict = {}

        pairs = config_text.split('&')

        for pair in pairs:
            if '=' in pair:
                key, value = pair.split('=', 1)
                config_dict[key.strip()] = value.strip()
            else:
                continue

        return config_dict