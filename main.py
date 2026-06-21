import os
import time
import requests

BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

KEYWORDS = [
    'ищу таргетолога', 'нужен таргетолог', 'требуется таргетолог',
    'вакансия таргетолог', 'таргетолог нужен', 'ищем таргетолога',
    'специалист по таргету', 'настройка рекламы вк', 'таргет вк',
    'таргетолог фриланс', 'ищу специалиста по рекламе',
    'нужен специалист по рекламе', 'таргетированная реклама',
    'настройка таргета', 'таргетолог мебель', 'таргетолог фитнес',
]

BASE_URL = f'https://api.telegram.org/bot{BOT_TOKEN}'

def send_message(chat_id, text):
    requests.post(f'{BASE_URL}/sendMessage', json={'chat_id': chat_id, 'text': text})

def get_updates(offset=None):
    params = {'timeout': 30, 'allowed_updates': ['message']}
    if offset:
        params['offset'] = offset
    try:
        r = requests.get(f'{BASE_URL}/getUpdates', params=params, timeout=35)
        return r.json()
    except Exception as e:
        print(f'Ошибка getUpdates: {e}')
        return {'ok': False, 'result': []}

def main():
    print('Бот запущен!')
    offset = None
    while True:
        data = get_updates(offset)
        if not data.get('ok'):
            time.sleep(5)
            continue
        for update in data.get('result', []):
            offset = update['update_id'] + 1
            msg = update.get('message')
            if not msg or not msg.get('text'):
                continue
            text = msg['text'].lower()
            if any(kw in text for kw in KEYWORDS):
                chat = msg.get('chat', {})
                chat_name = chat.get('title') or chat.get('username') or 'Неизвестно'
                msg_id = msg.get('message_id', '')
                username = chat.get('username', '')
                link = f'https://t.me/{username}/{msg_id}' if username else ''
                forward_text = (
                    f'🎯 ЗАПРОС НА ТАРГЕТОЛОГА\n'
                    f'━━━━━━━━━━━━━━━━━━━━\n'
                    f'📌 Источник: {chat_name}\n'
                    f'🔗 Ссылка: {link}\n'
                    f'━━━━━━━━━━━━━━━━━━━━\n'
                    f'{msg["text"][:1000]}'
                )
                if CHAT_ID:
                    send_message(CHAT_ID, forward_text)
                    print(f'Отправлено уведомление из {chat_name}')

if __name__ == '__main__':
    main()
