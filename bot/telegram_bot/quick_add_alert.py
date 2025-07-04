from telegram import Update
from telegram.ext import CallbackContext
from bot.alerts import AlertManager

alert_manager = AlertManager()

async def quick_add_alert(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    asset = "USDT"
    fiat = "INR"
    payment_method = "BANK"
    threshold = 89
    order_type = "Buy"

    alert_id, link = await alert_manager.add_alert(
        user_id,
        asset,
        fiat,
        order_type,
        threshold,
        payment_method
    )

    await update.message.reply_text(
        f"✅ Quick alert created:\n\n"
        f"*Asset:* {asset}\n"
        f"*Fiat:* {fiat}\n"
        f"*Order Type:* {order_type}\n"
        f"*Payment Method:* {payment_method}\n"
        f"*Threshold:* {threshold}\n\n"
        f"[View Offers]({link})",
        parse_mode="Markdown",
        disable_web_page_preview=True
    )
