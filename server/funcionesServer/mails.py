import smtplib, ssl
from dotenv import load_dotenv
import os
import yagmail
import keyring

load_dotenv()



def checkMail(mailUser):

    state = True

    try:

        password = os.getenv('passwordMail')


        sender_mail = 'valenuser02@gmail.com'
        receiver_mail = mailUser
        server_domain = 'smtp.gmail.com'


        msg = ''' Subject: Confirmacion registro serverFTP



        Bienvenido, te has registrado con exito en el serverFTP!
        '''


        context  = ssl.create_default_context()


        with smtplib.SMTP_SSL(server_domain,465,context=context) as s:
                s.login(sender_mail,password)
                s.sendmail(sender_mail,receiver_mail,msg)

    except:
        state = False


    return state

