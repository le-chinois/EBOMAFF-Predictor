import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bienvenue sur EBOMAFF Predictor !\n\n"
        "🎮 Sélectionne ton jeu et lance une prédiction.\n"
        "⚠️ Les résultats générés sont indicatifs et ne garantissent aucun gain."
    )

def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN n'est pas configuré.")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    print("🤖 EBOMAFF Predictor démarré...")
    app.run_polling()

if __name__ == "__main__":
    main()
