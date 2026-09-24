import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🚀 Lucky Jet", callback_data="luckyjet"),
         InlineKeyboardButton("✈️ Aviator", callback_data="aviator")],
        [InlineKeyboardButton("💥 Crash", callback_data="crash"),
         InlineKeyboardButton("👑 Rocket Queen", callback_data="rocketqueen")],
        [InlineKeyboardButton("💣 Mines Classic", callback_data="mines"),
         InlineKeyboardButton("📈 Limbo", callback_data="limbo")],
        [InlineKeyboardButton("⚽ Penalty", callback_data="penalty"),
         InlineKeyboardButton("🚀 Rocket X", callback_data="rocketx")],
        [InlineKeyboardButton("⚡ Speed & Cash", callback_data="speedcash"),
         InlineKeyboardButton("🐔 Chicken Train", callback_data="chickentrain")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🤖 Bienvenue sur EBOMAFF Predictor !\n\n"
        "🎮 Sélectionne ton jeu :\n"
        "⚠️ Les résultats générés sont indicatifs et ne garantissent aucun gain.",
        reply_markup=reply_markup
    )

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"EBOMAFF Predictor is running")

    def log_message(self, format, *args):
        pass


def run_server():
    port = int(os.getenv("PORT", "10000"))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()
def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN n'est pas configuré.")
    threading.Thread(target=run_server, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    print("🤖 EBOMAFF Predictor démarré...")
    app.run_polling()

if __name__ == "__main__":
    main()
