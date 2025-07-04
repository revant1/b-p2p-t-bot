import asyncio
from itertools import count
from bot.alerts import Alert
from bot.database import Database

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class AlertManager(metaclass=Singleton):
    def __init__(self):
        self.lock = asyncio.Lock()
        self.db = Database('alerts.db')
        self.db.init_db()
        self.alerts = self.db.load_alerts()
        start_id = 1 + max([0] + [alert.alert_id for alert in self.alerts.values()])
        self._id_generator = count(start=start_id)

    async def add_alert(self, user_id, asset, fiat, trade_type, threshold_price, payment_method):
        async with self.lock:
            alert_id = next(self._id_generator)
            alert = Alert(alert_id, user_id, asset, fiat, trade_type, threshold_price, payment_method)
            self.db.insert_alert(alert)
            self.alerts[alert_id] = alert
            return alert_id, alert.link

    async def check_alerts(self):
        tasks = [alert.check_alert() for alert in self.alerts.values() if alert.active]
        await asyncio.gather(*tasks)

    async def start_checking(self, interval=60):
        while True:
            await self.check_alerts()
            await asyncio.sleep(interval)