print("TOKEN QUE USA EL BOT:")
print(TOKEN)
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ⚠️ TOKEN DIRECTO (NO recomendado en producción)
TOKEN = "8730267318:AAFZSmLhCv3qTrTRFfKZThuCKs7zZWHwohE"


# ==============================
# COMANDO START
# ==============================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔥 Contenido VIP", callback_data="vip")],
        [InlineKeyboardButton("💎 Contenido Premium", callback_data="premium")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Bienvenido 💋\n\nSelecciona una opción:",
        reply_markup=reply_markup
    )


# ==============================
# BOTONES
# ==============================

async def botones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "vip":
        await query.edit_message_text(
            "Contenido VIP 💋\n\nPrecio: $10\n\nEnvía comprobante al admin."
        )

    elif query.data == "premium":
        await query.edit_message_text(
            "Contenido Premium 🔥\n\nPrecio: $25\n\nEnvía comprobante al admin."
        )


# ==============================
# MAIN
# ==============================

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(botones))

    print("Bot iniciado correctamente 🚀")
    await app.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
