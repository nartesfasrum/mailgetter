import poplib, getpass
from email import parser


def mail_connection():
    
    pop_conn = poplib.POP3_SSL(input('Mail server: '))
    pop_conn.user = input('Mail user: ')
    pop_conn.pass_ = getpass.getpass('Mail password: ')

    return pop_conn

def mail_fetch(delete_after=False):
    pop_conn = mail_connection()

    messages = [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1]) + 1)]
    messages = ["\n".join(mssg[1]) for mssg in messages]
    messages = [parser.Parser().parsestr(mssg) for mssg in messages]

    if delete_after == True:
        delete_messages = [pop_conn.dele(i) for i in range(1, len(pop_conn.list()[1]) + 1)]
    
    pop_conn.quit()

    return messages

def get_attachments():
    messages = mail_fetch()
    attachments = []

    for msg in messages:
        for part in msg.walk():
            if part.gett_content_type() in allowed_mimetypes:
                name = part.get_filename()
                data = part.get_payload(decode=True)
                f = file(name, 'wb')
                f.write(data)
                f.close
                attachments.append(name)
                
    return attachments

get_attachments()
