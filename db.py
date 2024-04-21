import sqlite3
import math
from config import MAX_VOICE_DURATION, MAX_USER_STT_BLOCKS


def create_table(db_name="speech_kit.db"):
    try:
        # Создаём подключение к базе данных
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                message TEXT,
                stt_blocks INTEGER)
            ''')
            conn.commit()
    except Exception as e:(
        print(f"Error: {e}"))


def insert_row(user_id, message, cell, value, db_name="speech_kit.db"):
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(f'''INSERT INTO messages (user_id, message, {cell}) VALUES (?, ?, ?)''',
                           (user_id, message, value))
            # Сохраняем изменения
            conn.commit()
    except Exception as e:
        print(f"Error: {e}")


def count_all_blocks(user_id, db_name="speech_kit.db"):
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT SUM(stt_blocks) FROM messages WHERE user_id=?''', (user_id,))
            data = cursor.fetchone()
            if data and data[0]:
                return data[0]
            else:
                return 0
    except Exception as e:
        print(f"Error: {e}")


def is_stt_block_limit(user_id, duration):
    audio_blocks = math.ceil(duration / 15)
    all_blocks = count_all_blocks(user_id) + audio_blocks

    if duration >= MAX_VOICE_DURATION:
        msg = "SpeechKit STT работает с голосовыми сообщениями меньше 30 секунд"
        return msg

    if all_blocks >= MAX_USER_STT_BLOCKS:
        msg = f"Превышен общий лимит SpeechKit STT {MAX_USER_STT_BLOCKS}. Использовано {all_blocks} блоков. Доступно: {MAX_USER_STT_BLOCKS - all_blocks}"
        return msg

    return audio_blocks


