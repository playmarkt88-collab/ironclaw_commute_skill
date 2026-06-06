import os
import requests
from datetime import datetime

class TrainTrackerSkill:
    def init(self):
        # Агент будет брать ключ из своих скрытых настроек
        self.api_key = os.getenv("YANDEX_API_KEY")
        self.url = "https://api.rasp.yandex.net/v3.0/search/"
        # Коды станций: Булатниково -> Москва-Товарная
        self.station_from = 's9601666'
        self.station_to = 's9602028'

    def execute(self) -> str:
        if not self.api_key:
            return "Ошибка: Не найден YANDEX_API_KEY в настройках агента."

        params = {
            "apikey": self.api_key,
            "format": "json",
            "from": self.station_from,
            "to": self.station_to,
            "lang": "ru_RU",
            "system": "yandex",
            "transport_types": "suburban",
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        
        try:
            response = requests.get(self.url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Отбираем только те электрички, которые еще не ушли
            now = datetime.now().isoformat()
            upcoming = [s for s in data.get('segments', []) if s['departure'] > now][:3]
            
            if not upcoming:
                return "На сегодня электричек больше нет."
                
            msg = "🚉 Ближайшие электрички: Булатниково ➔ Москва-Товарная\n"
            for t in upcoming:
                dept = t['departure'].split('T')[1][:5] # Достаем только часы:минуты
                arr = t['arrival'].split('T')[1][:5]
                title = t['thread']['short_title']
                msg += f"🕒 {dept} - {arr} | {title}\n"
                
            return msg
            
        except Exception as e:
            return f"Ошибка при запросе к Яндексу: {str(e)}"

# Этот блок срабатывает, когда IronClaw дергает скрипт
if __name__ == "main":
    skill = TrainTrackerSkill()
    print(skill.execute())
