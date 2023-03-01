import os
import smtplib
import ssl
import imaplib
import poplib


class EmailWrapper:
    def __init__(self, email, login, password, smtp_server, smtp_port, pop_server, pop_port, imap_server, imap_port):
        self.email = email
        self.login = login
        self.password = password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.pop_server = pop_server
        self.pop_port = pop_port
        self.imap_server = imap_server
        self.imap_port = imap_port

    def send_email(self, recipient, message):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
            server.login(self.login, self.password)
            server.sendmail(self.email, recipient, message)

    def get_emails(self, massages_nums, protocol='imap'):
        if protocol == 'pop3':
            return self.get_pop3(massages_nums)
        elif protocol == 'imap':
            return self.get_imap(massages_nums)
        else:
            raise ValueError ('Unknown protocol')

    def get_pop3(self, massages):
        M = poplib.POP3_SSL(self.pop_server)
        M.port = self.pop_port
        M.user(self.login)
        M.pass_(self.password)
        result = []
        for msg_num in massages:
            msg_num =  M.retr(msg_num)[1]
            result.append(str(msg_num))
        M.quit()
        return result

    def get_imap(self, massages):
        M = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
        M.login(self.login, self.password)
        M.select()
        result = []
        for msg_num in massages:
            typ, data = M.fetch(msg_num, '(RFC822)')
            result.append(str(data[0][1]))
        M.close()
        M.logout()
        return result






