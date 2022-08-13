#-*- coding:utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

smtp_server = "smtp.strato.de:465"
sender_email = "info@software-dieburg.de"
password = "info@software-dieburg.de@strato"


def send_mail(mail_to, subj="", msg=""):
    subject = "Ihre Anfrage an Software-Dieburg"
    tmp_message = "Vielen Dank für Ihre Nachricht an Software Dieburg!"
    message_end = '''<br><br><br>
        Mit freundlichen Grüßen <br><br>
        Tobias Cronauer<br>
        Software-Dieburg<br><br>
        http://www.software-dieburg.de    
    '''
    if subj != "":
        subject = subj
    if msg != "":
        tmp_message = msg

    message = MIMEMultipart("alternative")
    html_message = MIMEText(tmp_message + "\n\n\n" + message_end, "html")
    message["to"] = mail_to
    message["from"] = sender_email
    message["subject"] = subject
    message.attach(html_message)
    
    try:
        with smtplib.SMTP_SSL(smtp_server) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, mail_to, message.as_string())
            server.quit()
        return True
    except Exception as e:
        print(e)
        return False 


def send_html_mail(mail_to, subj="", msg=""):
    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = sender_email
    message["To"] = mail_to
    text = """\
Hi,
How are you?
Real Python has many great tutorials:
www.realpython.com"""
    html = """\
<html>
  <body>
    <p>Hi,<br>
       How are you?<br>
       <a href="http://www.realpython.com">Real Python</a> 
       has many great tutorials.
    </p>
  </body>
</html>
"""
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)

    try:
        with smtplib.SMTP_SSL(smtp_server) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, mail_to, message.as_string())
            server.quit()
        return True
    except:
        return False 
