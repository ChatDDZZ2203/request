import os
import asyncio

# External modules
import psycopg2
import requests
import telebot
from quart import Quart

bot = telebot.TeleBot(os.environ["TELEGRAM_BOT_TOKEN"])
app = Quart(__name__)
connection = psycopg2.connect(os.environ["DATABASE_URL"])
cur = connection.cursor()


@app.route('/', methods=["HEAD"])
async def index():
    asyncio.create_task(me())
    return 'OK'


async def me():
    cur.execute("""
                SELECT ident, url, password FROM request_data WHERE status = 'Ready'
                """)
    data = cur.fetchall()
    
    for i in range(15):
        final_string = ""
        for row in data:
            ident, url, passw = row
            try:
                r = requests.post(url, data={passw: ident}, timeout=4)
                final_string += f"Sent to\n{url}\n{passw}\n{r.text}\n\n"
            except requests.ReadTimeout:
                final_string += f"Read timeout on\n{url}\n{passw}\n\n"
            await asyncio.sleep(0.5)
        bot.send_message(chat_id=-1001968944787, message_thread_id=5279,
                         text=f"{final_string}\n\nSent {i + 1} Time")
        await asyncio.sleep(5)


app.run(host='0.0.0.0', port=int(os.getenv("PORT", 3000)))




