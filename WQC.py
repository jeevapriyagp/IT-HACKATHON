import smtplib
from email.mime.text import MIMEText
from datetime import datetime

THRESHOLDS = {
    'pH': {'min': 6.5, 'max': 8.5},
    'turbidity': {'max': 5.0}, 
    'temperature': {'min': 0, 'max': 30}  
}

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_SENDER = 'your_email@gmail.com'
EMAIL_RECEIVER = 'admin@example.com'
EMAIL_PASSWORD = 'your_password'


def check_water_quality(data):
    alerts = []
    for param, value in data.items():
        if param in THRESHOLDS:
            thresholds = THRESHOLDS[param]
            if 'min' in thresholds and value < thresholds['min']:
                alerts.append(f"{param} is below acceptable minimum: {value}")
            if 'max' in thresholds and value > thresholds['max']:
                alerts.append(f"{param} is above acceptable maximum: {value}")
    return alerts


def send_email_alert(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")


def get_sensor_data():
    return {
        'pH': 6.0,       # Below minimum threshold
        'turbidity': 6.0, # Above maximum threshold
        'temperature': 35 # Above maximum threshold
    }

def main():
    
    data = get_sensor_data()
    print(f"Collected data: {data}")

    
    alerts = check_water_quality(data)
    
    if alerts:
        
        alert_message = "\n".join(alerts)
        alert_subject = f"Water Quality Alert - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        print(f"Sending alert: {alert_message}")
        
        
        send_email_alert(alert_subject, alert_message)
    else:
        print("Water quality is within acceptable parameters.")

if __name__ == "__main__":
    main()
