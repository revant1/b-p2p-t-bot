from datetime import datetime, timedelta
from bot.binance_api import get_offers, get_link
from bot.utils import send_telegram_message

class Alert:
    def __init__(self, alert_id, user_id, asset, fiat, trade_type, threshold_price, payment_method):
        self.alert_id = alert_id
        self.user_id = user_id
        self.asset = asset
        self.fiat = fiat
        self.trade_type = trade_type
        self.threshold_price = threshold_price
        self.payment_method = payment_method
        self.active = True
        self.last_triggered = None
        self.trigger_interval = 15  # minutes
        self.link = get_link(self.fiat, self.asset, self.payment_method, self.trade_type)

    async def check_alert(self):
        if self.active and (self.last_triggered is None or datetime.now() >= self.last_triggered + timedelta(minutes=self.trigger_interval)):
            offers = await get_offers(self.asset, self.fiat, self.trade_type, payment_method=self.payment_method)
            for offer in offers:
                price = float(offer['price'])
                if (self.trade_type == 'Sell' and price >= self.threshold_price) or \
                   (self.trade_type == 'Buy' and price <= self.threshold_price):
                    await self.trigger_alert(price, offer['min_amount'], offer['max_amount'])
                    break

    async def trigger_alert(self, price, min_amount, max_amount):
        message = (
            f"<b>🚨 Alert Triggered!</b>\n\n"
            f"<b>ID:</b> {self.alert_id}\n"
            f"<b>Pair:</b> {self.asset}/{self.fiat}\n"
            f"<b>Type:</b> {self.trade_type}\n"
            f"<b>Price:</b> {price}\n"
            f"<b>Min:</b> {min_amount}, <b>Max:</b> {max_amount}\n\n"
            f"<a href='{self.link}'>View Offers</a>"
        )
        await send_telegram_message(self.user_id, message, parse_mode='HTML')
        self.last_triggered = datetime.now()