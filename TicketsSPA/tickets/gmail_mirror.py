import imapclient
import email
import re
from email.header import decode_header
from .models import Ticket

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

        # Check if a ticket with the same code already exists
        existing_tickets = Ticket.all_tickets.filter(code=code)

        # Check if the subject contains "fechado/resolvido"
        if "fechado/resolvido" in subject.lower():
            if existing_tickets.exists():
                # Update all tickets with the same code to "Fechado"
                existing_tickets.update(status='F')
        else:
            # If tickets with the same code exist, the parent ticket is the latest one.
            parent_ticket = existing_tickets.order_by('-created_at').first()

            # Check if a ticket with the same subject exists, if it does, update the existing one.
            ticket_instance = existing_tickets.filter(title=subject).first()
            if ticket_instance:
                ticket_instance.subject_from_email = body
                ticket_instance.save()
            else:
                # If no ticket with the same subject exists, create a new one.
                ticket_instance = Ticket.all_tickets.create(
                    title=subject,
                    subject_from_email=body,
                    code=code,
                    parent=parent_ticket
                )
