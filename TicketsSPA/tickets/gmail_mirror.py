import imapclient
import email
from email.header import decode_header

EMAIL = "prometonaoescam@gmail.com"
PASSWORD = "wmmcblxzxvcocuyz"


def get_emails():
    with imapclient.IMAPClient("imap.gmail.com", ssl=True) as client:
        client.login(EMAIL, PASSWORD)
        client.select_folder("INBOX")

        messages = []
        # Search for all unseen messages
        message_ids = client.search(["UNSEEN"])
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
                {"subject": subject, "body": body, })

        return messages
