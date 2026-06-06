import os
import requests
from datetime import datetime
import pytz

class TrainTrackerSkill:
    def init(self):
        self.api_key = os.getenv("YANDEX_API_KEY")
        self.url = "https://api.rasp.yandex.net/v3.0/search/"
        self.station_from = 's9601666'
        self.station_to = 's9602028'
        self.tz_moscow = pytz.timezone('Europe/Moscow')

    def execute(self) -> str:
        if not self.api_key:
            return "Ошибка: Не найден YANDEX_API_KEY."

        now_moscow = datetime.now(self.tz_moscow)
        params = {
            "apikey": self.api_key,
            "format": "json",
            "from": self.station_from,
            "to": self.station_to,
            "lang": "ru_RU",
            "system": "yandex",
            "transport_types": "suburban",
            "date": now_moscow.strftime("%Y-%m-%d")
        }
        
        try:
            response = requests.get(self.url, params=params)
            response.raise_for_status()
            data = response.json()
            
            now_iso = now_moscow.isoformat()
            upcoming = [s for s in data.get('segments', []) if s['departure'] > now_iso][:3]
            
            if not upcoming:
                return "🤷‍♂️ На ближайшее время электричек больше нет."
                
            msg = "🚉 Ближайшие электрички: Булатниково ➔ Москва-Товарная\n"
            for t in upcoming:
                dept = t['departure'].split('T')[1][:5]
                arr = t['arrival'].split('T')[1][:5]
                title = t['thread']['short_title']
                msg += f"🕒 {dept} - {arr} | {title}\n"
                
            return msg
            
        except Exception as e:
            return f"Ошибка при запросе к Яндексу: {str(e)}"

# ВОТ ЭТОТ БЛОК ЗАСТАВЛЯЕТ КОД РАБОТАТЬ
if __name__ == "__main__":
    skill = TrainTrackerSkill()
    print(skill.execute())
