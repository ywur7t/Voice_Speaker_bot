import telebot
import requests


def send_to_api(text: str) -> bytes:

    data = {"text": text}
    url = 'https://ttv.mckrei.ru/api/elevenlabs/text_to_speech'
    auth_header = {'Authorization': 'free'}
    response = requests.post(url, headers=auth_header, json=data)

    if response.status_code == 200:
        return response.content
    else:
        raise Exception("API connect error")

def save_audio_file(audio_content: bytes, filename: str = "voice_message.mp3"):
    with open(filename, 'wb') as f:
        f.write(audio_content)

def send_welcome_message(message, bot):
    bot.reply_to(message, "Text to voice")

def handle_user_text(message, bot):
    text = message.text
    try:
        waiting_message = bot.send_message(message.chat.id, "Recording...")

        audio_content = send_to_api(text)

        save_audio_file(audio_content)

        bot.delete_message(message.chat.id, waiting_message.message_id)

        with open("voice_message.mp3", 'rb') as voice:
            bot.send_voice(message.chat.id, voice)

    except Exception as e:

        bot.delete_message(message.chat.id, waiting_message.message_id)
        bot.send_message(message.chat.id, "Something goes wrong but i dont care")
        print(f"Error: {e}")




def main():
    API_TOKEN = "7476653740:AAEdOhZHRWrfjjtq66Ov-13VCzYs7z8LCB4"

    bot = telebot.TeleBot(API_TOKEN)

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        send_welcome_message(message, bot)

    @bot.message_handler(func=lambda message: True)
    def handle_text(message):
        handle_user_text(message, bot)

    bot.polling()

if __name__ == "__main__":
    main()