import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage


def send_email(receiver_email, contest_name,web_address):
    sender_email = "laydenserver@gmail.com"
    smtp_password = 'meep hnev xblq nfki'
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Create the email message
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    del msg["Subject"]

    if not receiver_email[0:10].isdigit():  # if not a mms address
        msg['Subject'] = "Judging card results are in!"

    # include image
    with open("Results JC post process.png", "rb") as image_file:
        image_data = image_file.read()
        image = MIMEImage(image_data, name="Results JC post process.png")
        msg.attach(image)

    # body of the email
    msg.attach(MIMEText("Judging card has updated: \n", "plain"))
    msg.attach(MIMEText((contest_name +" "), "plain"))
    msg.attach(MIMEText(web_address, "plain"))

    # Establish a connection to the SMTP server
    try:
        mail_server = smtplib.SMTP(smtp_server, smtp_port)
        mail_server.starttls()
        mail_server.login(sender_email, smtp_password)
        mail_server.sendmail(sender_email, receiver_email, msg.as_string())
        print("notified: ", receiver_email)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        mail_server.quit()  
