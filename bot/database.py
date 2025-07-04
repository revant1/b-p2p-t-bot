import sqlite3
from bot.alerts import Alert

class Database:
    def __init__(self, db_name):
        self.db_name = db_name

    def init_db(self):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS alerts (
                            alert_id INTEGER PRIMARY KEY,
                            user_id INTEGER,
                            asset TEXT,
                            fiat TEXT,
                            trade_type TEXT,
                            threshold_price REAL,
                            payment_method TEXT,
                            active INTEGER,
                            last_triggered TEXT
                        )''')
            conn.commit()

    def insert_alert(self, alert: Alert):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute('''INSERT INTO alerts (alert_id, user_id, asset, fiat, trade_type, threshold_price, payment_method, active, last_triggered)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                      (alert.alert_id, alert.user_id, alert.asset, alert.fiat, alert.trade_type, alert.threshold_price, alert.payment_method, int(alert.active), alert.last_triggered))
            conn.commit()

    def load_alerts(self):
        alerts = {}
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            for row in c.execute('SELECT * FROM alerts'):
                alert_id, user_id, asset, fiat, trade_type, threshold_price, payment_method, active, last_triggered = row
                alert = Alert(alert_id, user_id, asset, fiat, trade_type, threshold_price, payment_method)
                alert.active = bool(active)
                if last_triggered:
                    from datetime import datetime
                    alert.last_triggered = datetime.fromisoformat(last_triggered)
                alerts[alert_id] = alert
        return alerts
