import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email Configurations
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "fluffybirdgpt@gmail.com"
EMAIL_PASSWORD = "mzkm bsoi mclf woxy"

def send_email(medicine_name, subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = 'minethsasvin@gmail.com'  #Replace with recipient's email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))  #HTML Email Support

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, 'minethsasvin@gmail.com', msg.as_string())
            print(f"✅ Email sent successfully to minethsasvin@gmail.com")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

#Improved Email Body
def format_email_body(medicine_name, stock, pharmacy, is_low_stock=False):
    if is_low_stock:
        body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <h2 style="color: #ff4d4d;">⚠️ Low Stock Alert!</h2>
                <p>The stock for <b>{medicine_name}</b> at <b>{pharmacy}</b> is critically low at <b>{stock}</b> units.</p>
                <p style="color: #ff4d4d;"><b>Please restock immediately!</b></p>
                <hr>
                <p style="color: #888;">This is an automated notification from the Medicine Shortage Tracker.</p>
            </body>
        </html>
        """
    else:
        body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <h2 style="color: #2a9df4;">Medicine Stock Update</h2>
                <p>The stock for <b>{medicine_name}</b> at <b>{pharmacy}</b> has been updated to <b>{stock}</b> units.</p>
                <p>Please check the inventory for any further adjustments.</p>
                <hr>
                <p style="color: #888;">This is an automated notification from the Medicine Shortage Tracker.</p>
            </body>
        </html>
        """

    return body