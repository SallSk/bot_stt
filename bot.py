import telebot
from db import create_table, insert_row, is_stt_block_limit
from speechkit import speech_to_text

bot = telebot.TeleBot('token')

@bot.message_handler(commands=['stt'])
def stt_handler(message):
    message.chat.id = message.from_user.id
    bot.send_message(message.chat.id, 'Отправь голосовое сообщение, чтобы я его распознал!')
    bot.register_next_step_handler(message, stt)


def stt(message):
    if not message.voice:
        return

    stt_blocks = is_stt_block_limit(message, message.voice.duration)
    if stt_blocks is str:
        bot.send_message(message.chat.id, stt_blocks)
        return

    file_id = message.voice.file_id
    file_info = bot.get_file(file_id)
    file = bot.download_file(file_info.file_path)

    status, text = speech_to_text(file)

    if status:
        insert_row(message.chat.id, text, 'stt_blocks', stt_blocks)
        bot.send_message(message.chat.id, text, reply_to_message_id=message.id)
    else:
        bot.send_message(message.chat.id, text)


if __name__ == '__main__':
    create_table()
    bot.polling()
