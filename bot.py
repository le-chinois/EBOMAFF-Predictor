import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🚀 Lucky Jet", callback_data="luckyjet"),
            InlineKeyboardButton("✈️ Aviator", callback_data="aviator"),
        ],
        [
            InlineKeyboardButton("💥 Crash", callback_data="crash"),
            InlineKeyboardButton("👑 Rocket Queen", callback_data="rocketqueen"),
        ],
        [
            InlineKeyboardButton("💣 Mines Classic", callback_data="mines"),
            InlineKeyboardButton("📈 Limbo", callback_data="limbo"),
        ],
        [
            InlineKeyboardButton("⚽ Penalty", callback_data="penalty"),
            InlineKeyboardButton("🚀 Rocket X", callback_data="rocketx"),
        ],
        [
            InlineKeyboardButton("⚡ Speed & Cash", callback_data="speedcash"),
            InlineKeyboardButton("🐔 Chicken Train", callback_data="chickentrain"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🤖 Bienvenue sur EBOMAFF Predictor !\n\n"
        "🎮 Sélectionne ton jeu :\n"
        "⚠️ Les résultats générés sont indicatifs et ne garantissent aucun gain.",
        reply_markup=reply_markup,
    )


async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    jeu = query.data

    if jeu == "luckyjet":
        await query.message.reply_text(
            "🚀 LUCKY JET\n\n"
            "🔎 Analyse du prochain tour en cours...\n"
            "⏳ Préparation du signal...\n\n"
            "📊 Envoie maintenant au moins 5 coefficients récents.\n"
            "Exemple : 1.24 2.15 1.08 3.42 1.67"
        )

        context.user_data["waiting_luckyjet"] = True
        return


async def analyse_luckyjet(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not context.user_data.get("waiting_luckyjet"):
        return

    texte = update.message.text.replace(",", ".")

    try:
        coefficients = [float(x) for x in texte.split()]
    except ValueError:
        await update.message.reply_text(
            "❌ Format incorrect.\n"
            "Exemple : 1.24 2.15 1.08 3.42 1.67"
        )
        return

    if len(coefficients) < 5:
        await update.message.reply_text(
            "⚠️ Envoie au moins 5 coefficients."
        )
        return

    recents = coefficients[-5:]

    moyenne = sum(recents) / len(recents)
    minimum = min(recents)
    maximum = max(recents)
    estimation = round(moyenne, 2)

    context.user_data["waiting_luckyjet"] = False

    await update.message.reply_text(
        "🚀 LUCKY JET - ANALYSE\n\n"
        f"📊 Tours analysés : {len(coefficients)}\n"
        f"🔎 5 derniers tours : {' '.join(f'{x:.2f}x' for x in recents)}\n"
        f"⬇️ Minimum récent : {minimum:.2f}x\n"
        f"⬆️ Maximum récent : {maximum:.2f}x\n"
        f"📈 Moyenne des 5 derniers : {moyenne:.2f}x\n"
        f"🎯 Estimation statistique : {estimation:.2f}x\n\n"
        "⚠️ Estimation calculée à partir des résultats fournis, "
        "pas le résultat garanti du prochain tour."
    )


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            with open("index.html", "rb") as file:
                content = file.read()

            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()

            self.wfile.write(content)

        except FileNotFoundError:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"index.html not found")

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
    app.add_handler(CallbackQueryHandler(button_click))
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            analyse_luckyjet,
        )
    )

    print("🤖 EBOMAFF Predictor démarré...")
    app.run_polling()


if __name__ == "__main__":
    main()
