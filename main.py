#!/usr/bin/env python3
import io
from html import escape

from telegram import Bot, ParseMode, TelegramError

from cleaner import remove_unallowed_tags, unicode_unescape
from config import env
from mailer import Mailer

bot, chat_id = Bot(env['TM_TOKEN']), env['GROUP']
mail = Mailer(env['EMAIL_LOGIN'], env['EMAIL_PASS'], env['INBOX'])

for msg in mail.fetch():
    is_plain = any('text/plain' in h['Value'] for h in msg.headers)
    source = ''.join(msg.body['plain'] or msg.body['html'])
    to_html = escape if is_plain else remove_unallowed_tags

    text = unicode_unescape(to_html(source)).strip()
    subject = msg.subject.lstrip('Re: ')
    author = ''  # + ', '.join(box['name'] for box in msg.sent_from)

    nl = '\n' if len(text.split('\n')) > 2 else ''
    post = f'<b>{subject}</b>{nl}\n{text}\n<i>{author}</i>'

    try:
        bot.sendMessage(chat_id, post, parse_mode=ParseMode.HTML)

        for at in msg.attachments:
            file = io.BufferedReader(at['content'])
            group, _ = at['content-type'].split('/')

            if group == 'image':
                bot.sendPhoto(chat_id, file)
            else:
                bot.sendDocument(chat_id, file, at['filename'])

        status = 'Новость успешно опубликована.\nЭто сообщение автоматическое, отвечать на него не нужно.'
        mail.send_email(msg.sent_from[0]['email'], status, 'Статус отправки')

    except TelegramError as e:
        del msg.raw_email
        err = f'Сообщение не доставлено.\n\n{e.message}\n\n{str(msg)}'
        mail.send_email(to=mail.login, body=err, subject='au-apartment-bot')
        break
