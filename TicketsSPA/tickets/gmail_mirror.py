import imapclient
import email
import re
from email.header import decode_header
from .models import Email, Ticket

EMAIL = "prometonaoescam@gmail.com"
PASSWORD = "wmmcblxzxvcocuyz"


def get_emails():
    with imapclient.IMAPClient("imap.gmail.com", ssl=True) as client:
        client.login(EMAIL, PASSWORD)
        client.select_folder("INBOX")

        messages = []
        # Search for all messages from a specific sender (noreply.escoladigital@min-educ.pt)
        sender = "noreply.escoladigital@min-educ.pt"
        message_ids = client.search(['FROM', sender])
        for message_id in message_ids:
            msg_data = client.fetch([message_id], ["RFC822"])[message_id]
            msg = email.message_from_bytes(msg_data[b"RFC822"])
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8")
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True)
                        break
            else:
                body = msg.get_payload(decode=True)

            messages.append(
                # Decodifica o corpo do email para uma string
                {"subject": subject, "body": body.decode()}
            )

        return messages


def create_ticket_instances(emails):
    for email_data in emails:
        subject = email_data['subject']
        body = email_data['body']

        # Extract the code from the subject using regular expressions
        code_regex = r"\[(.*?)\]"
        match = re.search(code_regex, subject)
        if match:
            code = match.group(1)
        else:
            code = ""

        # Check if a ticket with the same subject already exists
        existing_ticket = Ticket.objects.filter(title=subject).first()

        if existing_ticket:
            # If a ticket with the same subject exists, update its details
            existing_ticket.subject_from_email = body
            existing_ticket.save()
            ticket_instance = existing_ticket
        else:
            # Create a new ticket instance
            ticket_instance = Ticket.objects.create(
                title=subject,
                subject_from_email=body,
                code=code
            )

        # Create an instance of the Email model
        email_instance = Email.objects.create(
            assunto=subject,
            corpo=body,
            ticket=ticket_instance
        )

        # Check if the subject contains "fechado/resolvido"
        if "fechado/resolvido" in subject.lower():
            ticket_instance.status = 'F'  # Update status to "Fechado"
            ticket_instance.save()

