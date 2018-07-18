import smtplib as smtp
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from imbox import Imbox


class Mailer:
    def __init__(self, login: string, password: string, contact_address: string = None):
        """
        :param login: account login, like example@gmail.com
        :param password: password to the account
        :param contact_address: email where the director sends messages (example+dir@gmail.com)
        """
        self.login = login
        self.password = password
        self.contact_address = contact_address or login


    def send_email(self, to: string, body: string = '', subject: string = ''):
        """
        :param to: destination email address
        :param body: content of the message
        :param subject: subject of the message
        """
        msg = MIMEMultipart('alternative')

        # login+commentary in "From" is legal
        msg['Sender'] = self.contact_address
        msg['From'] = f'Игорь Стребежев <{self.contact_address}>'
        msg['Subject'] = subject
        msg['To'] = to

        # html = """<html><head></head><body>%s</body></html>""" % body
        # part = MIMEText(html.encode('utf-8'), 'html', 'utf-8')
        part = MIMEText(body.encode('utf-8'), 'plain', 'utf-8')
        msg.attach(part)

        yandex = smtp.SMTP_SSL('smtp.yandex.com')
        # yandex.set_debuglevel(1)
        yandex.ehlo(self.login)
        yandex.login(self.login, self.password)
        yandex.auth_plain()
        yandex.sendmail(self.login, to, msg.as_string())
        yandex.quit()


    def fetch(self):
        # with suppress(BaseException):
        with Imbox('imap.yandex.ru', self.login, self.password, port=993) as ya:
            # app folder already contains letters sent to the contact_address
            for uid, msg in ya.messages(unread=True, folder='app'):
                yield msg
                ya.mark_seen(uid)
