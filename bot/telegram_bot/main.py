import os
import asyncio
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters
from bot.telegram_bot import add_alert, prices
from bot.alerts.alert_manager import AlertManager
from bot.telegram_bot.quick_add_alert import quick_add_alert
from bot.telegram_bot.common import cancel, error
from bot.telegram_bot.show_alerts import show_alerts
from bot.telegram_bot.remove_alert import remove_alert
from bot.telegram_bot.inactivate_alert import inactivate_alert
from bot.telegram_bot.activate_alert import activate_alert
from dotenv import load_dotenv


load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Define conversation states
(CRYPTO, FIAT, ORDER_TYPE, PRICE, REMOVE_ALERT) = range(5)

async def on_startup(application):
    alert_manager = AlertManager()
    asyncio.create_task(alert_manager.start_checking())

def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_error_handler(error)

    # Prices conversation
    prices_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('prices', prices.start_prices)],
        states={
            prices.GET_CRYPTO: [MessageHandler(filters.TEXT & ~filters.COMMAND, prices.get_crypto)],
            prices.GET_FIAT: [MessageHandler(filters.TEXT & ~filters.COMMAND, prices.get_fiat)],
            prices.GET_ORDER_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, prices.get_order_type)],
            prices.GET_PAYMENT_METHOD: [MessageHandler(filters.TEXT & ~filters.COMMAND, prices.get_payment_method)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    application.add_handler(prices_conv_handler)

    # Add alert conversation
    add_alert_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('add_alert', add_alert.start_add_alert)],
        states={
            add_alert.GET_CRYPTO: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_alert.get_crypto)],
            add_alert.GET_FIAT: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_alert.get_fiat)],
            add_alert.GET_ORDER_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_alert.get_order_type)],
            add_alert.GET_PAYMENT_METHOD: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_alert.get_payment_method)],
            add_alert.GET_THRESHOLD: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_alert.get_threshold)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    application.add_handler(add_alert_conv_handler)

    # Quick add alert
    quick_add_alert_handler = CommandHandler('quick_add_alert', quick_add_alert)
    application.add_handler(quick_add_alert_handler)

    # Other handlers
    application.add_handler(CommandHandler('show_alerts', show_alerts))
    application.add_handler(CommandHandler('remove_alert', remove_alert))
    application.add_handler(CommandHandler('inactivate_alert', inactivate_alert))
    application.add_handler(CommandHandler('activate_alert', activate_alert))

    # Startup tasks
    application.post_init = on_startup

    print("🚀 Bot running with alert monitoring...")
    application.run_polling()

if __name__ == '__main__':
    main()