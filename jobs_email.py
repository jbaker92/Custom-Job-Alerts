import keyring
import smtplib
import ssl
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_job_email(jobs):
    """Email automated jobs alert"""
    # Get email settings from config file
    email_settings = parse_conf()
    # Connect to SMTP server
    server = smtp_connect(email_settings)
    # Construct email and send, quit smtp server
    msg = MIMEMultipart()
    msg['From'] = email_settings['From']
    msg['To'] = email_settings['To']
    msg['Subject'] = email_settings['Subject']
    msg.attach(MIMEText(jobs, 'html', _charset = 'utf-8'))
    server.sendmail(email_settings['From'], email_settings['To'], msg.as_string()) 
    server.quit()


def smtp_connect(settings):
    """Connect to smtp server for mail.com"""
    # Create a secure SSL context
    smtp = smtplib.SMTP(settings['Hostname'], int(settings['Port']))
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(settings['From'], keyring.get_password(settings['Hostname'], settings['From']))
    return smtp


def parse_conf():
    """Parse email config file to get email details"""
    with open("email.conf") as emailconf:
        settings = {line.split(":")[0] : line.split(":")[1] for line in emailconf.readlines()}
    # Remove any extra whitespace/newlines
    settings = {key.strip(): value.strip() for key, value in settings.iteritems()}
    return settings
