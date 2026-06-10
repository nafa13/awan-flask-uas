class NotificationService:
    """
    Placeholder untuk layanan notifikasi (AWS SNS/SES).
    Akan diimplementasikan pada fase selanjutnya.
    """
    @staticmethod
    def send_email(to_address: str, subject: str, message: str):
        # Simulasi pengiriman email
        print(f"[NOTIFICATION] Sending email to {to_address} - Subject: {subject}")
        pass
        
    @staticmethod
    def send_sms(phone_number: str, message: str):
        print(f"[NOTIFICATION] Sending SMS to {phone_number}")
        pass
