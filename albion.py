import imaplib, email

user = 'albioncompany18@gmail.com'
password = 'Albion2018'
imap_url = 'imap.gmail.com'

def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None, True)

def search(key, value, conn):
    result, data = conn.search(None, key, '"()"'.format(value))
    return data

conn = imaplib.IMAP4_SSL(imap_url)

conn.login(user, password)

conn.select('INBOX')

result, data = conn.fetch(b'1', '(RFC822)')
raw = email.message_from_bytes(data[0][1])


msgs = []
result, data = conn.uid('search', None, "ALL")
if result == 'OK':
    for num in data[0].split():
        result, data = conn.uid('fetch', num, '(RFC822)')
        if result == 'OK':
            email_message = email.message_from_bytes(data[0][1])
            msgs.append(get_body(email_message))

for msg in msgs:
    print(msg)