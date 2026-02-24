import os
import asyncio
import sqlite3
from datetime import datetime
from telegram import (
    Update,
    BotCommand,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler
)

# ==============================
# CONFIGURACIÓN
# ==============================

TOKEN = os.getenv("TOKEN")
ADMIN_ID = 123456789  # 🔴 PON TU ID REAL AQUÍ

# ==============================
# BASE DE DATOS
# ==============================

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()

def register_user(user):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO users (id, username, first_name, created_at)
    VALUES (?, ?, ?, ?)
    """, (user.id, user.username, user.first_name, datetime.now()))

    conn.commit()
    conn.close()

# ==============================
# COMANDOS
# ==============================

async def set_commands(app):
    commands = [
        BotCommand("start", "Iniciar"),
        BotCommand("menu", "Ver catálogo"),
        BotCommand("id", "Ver mi ID")
    ]
    await app.bot.set_my_commands(commands)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    register_user(update.effective_user)
    await update.message.reply_text(
        f"Hola 👋\nTu ID es: {update.effective_user.id}\n\nUsa /menu para ver catálogo."
    )

async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🆔 Tu ID es: {update.effective_user.id}"
    )

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Ejemplo Producto - $10", callback_data="buy_test")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Selecciona una opción:",
        reply_markup=reply_markup
    )

# ==============================
# BOTONES
# ==============================

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "buy_test":
        await query.edit_message_text(
            "Producto seleccionado.\nEnvía comprobante de pago."
        )

# ==============================
# MAIN
# ==============================

async def main():
    init_db()

    app = ApplicationBuilder().token(TOKEN).build()

    # Registrar handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("id", get_id))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CallbackQueryHandler(button_handler))

    # Registrar comandos oficiales
    await set_commands(app)

    print("🚀 Bot activo correctamente...")

    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
