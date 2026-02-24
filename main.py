import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

# ==============================
# CARGAR TOKEN DESDE VARIABLES
# ==============================

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("No se encontró BOT_TOKEN en las variables de entorno")

# ==============================
# COMANDOS
# ==============================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔥 Contenido VIP", callback_data="vip")],
        [InlineKeyboardButton("💎 Contenido Premium", callback_data="premium")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Bienvenido 💋\n\nSelecciona una opción:",
        reply_markup=reply_markup
    )

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
# FUNCIÓN PRINCIPAL
# ==============================

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(botones))

    print("Bot iniciado correctamente 🚀")
    await app.run_polling()

# ==============================

if __name__ == "__main__":
    asyncio.run(main())
