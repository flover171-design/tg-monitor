import os
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

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

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text.lower()

    if any(kw in text for kw in KEYWORDS):
        chat = update.message.chat
        chat_name = chat.title or chat.username or 'Неизвестно'
        msg_id = update.message.message_id

        link = ''
        if chat.username:
            link = f'https://t.me/{chat.username}/{msg_id}'

        forward_text = (
            f'🎯 ЗАПРОС НА ТАРГЕТОЛОГА\n'
            f'━━━━━━━━━━━━━━━━━━━━\n'
            f'📌 Источник: {chat_name}\n'
            f'🔗 Ссылка: {link}\n'
            f'━━━━━━━━━━━━━━━━━━━━\n'
            f'{update.message.text[:1000]}'
        )

        if CHAT_ID:
            await context.bot.send_message(chat_id=CHAT_ID, text=forward_text)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text(
        f'✅ Монитор запущен!\n'
        f'Твой Chat ID: {chat_id}\n\n'
        f'Скопируй этот ID и добавь его в переменную CHAT_ID на Railway.'
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    from telegram.ext import CommandHandler
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print('Бот запущен!')
    app.run_polling()

if __name__ == '__main__':
    main()
