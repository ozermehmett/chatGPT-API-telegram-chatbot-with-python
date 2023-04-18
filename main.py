import openai
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = "YOUR BOT TOKEN"
openai.api_key = "YOUR API TOKEN"
model_engine = "text-davinci-002"

def generate_text(prompt):
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=256,
        n=1,
        stop=None,
        temperature=0.4,
        )
    message = completions.choices[0].text.strip()
    return message

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Lütfen daha doğru cevaplar almak için ingilizce konuşun!")

def unknown(update, context):
    prompt = update.message.text
    response = generate_text(prompt)
    if "\n" in response:
        response = response[response.find("\n") + 1:]
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, unknown))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()