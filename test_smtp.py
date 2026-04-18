"""Quick test of all SMTP configurations for info@aoeua.com"""
import smtplib, ssl

configs = [
    ('smtp.gmail.com', 587, 'STARTTLS'),
    ('smtp-relay.gmail.com', 587, 'STARTTLS'),
    ('smtp.gmail.com', 465, 'SSL'),
]

for host, port, method in configs:
    try:
        print(f'Trying {host}:{port} ({method})...')
        if method == 'SSL':
            ctx = ssl.create_default_context()
            server = smtplib.SMTP_SSL(host, port, context=ctx, timeout=10)
        else:
            server = smtplib.SMTP(host, port, timeout=10)
            server.ehlo()
            if method == 'STARTTLS':
                ctx = ssl.create_default_context()
                server.starttls(context=ctx)
                server.ehlo()
        
        server.login('info@aoeua.com', '320990567!')
        print(f'  >>> SUCCESS on {host}:{port}! <<<')
        server.quit()
        break
    except smtplib.SMTPAuthenticationError as e:
        print(f'  Auth failed: {e.smtp_code}')
    except Exception as e:
        print(f'  Error: {e}')
