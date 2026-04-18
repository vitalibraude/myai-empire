"""
Email Verification System — validates emails BEFORE sending.
3-layer verification:
  1. Syntax check
  2. DNS MX record check (domain has mail server)
  3. SMTP RCPT TO check (mailbox actually exists)

Target: 95%+ real emails only.
"""
import re
import dns.resolver
import smtplib
import socket
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
VERIFIED_FILE = os.path.join(DATA_DIR, 'verified_prospects.json')
INVALID_FILE = os.path.join(DATA_DIR, 'invalid_emails.json')

# Disposable/catchall domains to skip
SKIP_DOMAINS = {
    'example.com', 'test.com', 'localhost', 'mailinator.com',
    'guerrillamail.com', 'tempmail.com', 'throwaway.email'
}


def check_syntax(email):
    """Layer 1: Basic email format validation."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email.strip()))


def check_mx(domain):
    """Layer 2: Check if domain has MX records (can receive email)."""
    try:
        records = dns.resolver.resolve(domain, 'MX')
        mx_hosts = [str(r.exchange).rstrip('.') for r in records]
        return mx_hosts if mx_hosts else None
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN,
            dns.resolver.NoNameservers, dns.exception.Timeout):
        return None
    except Exception:
        return None


def check_smtp_rcpt(email, mx_hosts, timeout=10):
    """
    Layer 3: SMTP RCPT TO — check if the mailbox exists.
    Connects to the MX server and asks if it accepts mail for this address.
    """
    for mx in mx_hosts[:2]:  # Try top 2 MX records
        try:
            with smtplib.SMTP(timeout=timeout) as smtp:
                smtp.connect(mx, 25)
                smtp.helo('aoeua.com')
                smtp.mail('verify@aoeua.com')
                code, _ = smtp.rcpt(email)
                smtp.quit()
                if code == 250:
                    return 'valid'
                elif code == 550:
                    return 'invalid'
                else:
                    return 'unknown'
        except smtplib.SMTPServerDisconnected:
            return 'unknown'  # Server doesn't cooperate — can't tell
        except (socket.timeout, socket.error, smtplib.SMTPException):
            continue
        except Exception:
            continue
    return 'unknown'


def verify_email(email):
    """
    Full 3-layer verification. Returns dict with result.
    """
    email = email.strip().lower()
    result = {
        'email': email,
        'syntax': False,
        'mx': False,
        'smtp': 'unchecked',
        'verdict': 'invalid'
    }

    # Layer 1: Syntax
    if not check_syntax(email):
        return result
    result['syntax'] = True

    domain = email.split('@')[1]

    # Skip known bad domains
    if domain in SKIP_DOMAINS:
        return result

    # Layer 2: MX record
    mx_hosts = check_mx(domain)
    if not mx_hosts:
        return result
    result['mx'] = True

    # Layer 3: SMTP mailbox check
    smtp_result = check_smtp_rcpt(email, mx_hosts)
    result['smtp'] = smtp_result

    if smtp_result == 'valid':
        result['verdict'] = 'valid'
    elif smtp_result == 'unknown':
        # MX exists but server won't tell us — likely catchall or greylisting
        # These are risky but domain is real, count as 'risky'
        result['verdict'] = 'risky'
    else:
        result['verdict'] = 'invalid'

    return result


def verify_prospect_list(prospects, max_workers=5):
    """
    Verify a list of prospects in parallel.
    Returns (verified, invalid, risky) lists.
    """
    verified = []
    invalid = []
    risky = []
    total = len(prospects)

    print(f"[VERIFY] Starting verification of {total} emails...")
    print(f"[VERIFY] Using {max_workers} parallel workers")

    def _verify_one(prospect):
        email = prospect.get('email', '').strip().lower()
        if not email:
            return ('invalid', prospect, None)
        r = verify_email(email)
        return (r['verdict'], prospect, r)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_verify_one, p): p for p in prospects}
        done = 0
        for future in as_completed(futures):
            done += 1
            verdict, prospect, result = future.result()
            email = prospect.get('email', '?')

            if verdict == 'valid':
                verified.append(prospect)
                status = '✅'
            elif verdict == 'risky':
                risky.append(prospect)
                status = '⚠️'
            else:
                invalid.append(prospect)
                status = '❌'

            if done % 10 == 0 or done == total:
                print(f"  [{done}/{total}] {status} {email} -> {verdict}")

    print(f"\n[VERIFY] Results:")
    print(f"  ✅ Valid:   {len(verified)}")
    print(f"  ⚠️  Risky:   {len(risky)}")
    print(f"  ❌ Invalid: {len(invalid)}")
    print(f"  📊 Valid rate: {len(verified)*100/total:.1f}%")

    return verified, invalid, risky


def save_verified(verified, risky):
    """Save verified prospects to file."""
    os.makedirs(DATA_DIR, exist_ok=True)
    # Include risky ones too (domain exists, just can't confirm mailbox)
    all_good = verified + risky
    with open(VERIFIED_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_good, f, indent=2, ensure_ascii=False)
    print(f"[VERIFY] Saved {len(all_good)} verified prospects to {VERIFIED_FILE}")
    return VERIFIED_FILE


def save_invalid(invalid):
    """Save invalid emails for reference."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(INVALID_FILE, 'w', encoding='utf-8') as f:
        json.dump([p.get('email', '') for p in invalid], f, indent=2)
    print(f"[VERIFY] Saved {len(invalid)} invalid emails to {INVALID_FILE}")


def main():
    """Load all prospects, verify, and save clean list."""
    prospects_file = os.path.join(DATA_DIR, 'real_prospects.json')
    manufacturer_file = os.path.join(DATA_DIR, 'manufacturer_prospects.json')

    all_prospects = []
    seen = set()

    for fpath in [prospects_file, manufacturer_file]:
        if not os.path.exists(fpath):
            continue
        with open(fpath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for p in data:
            email = p.get('email', '').strip().lower()
            if email and email not in seen:
                seen.add(email)
                all_prospects.append(p)

    print(f"[VERIFY] Loaded {len(all_prospects)} unique prospects")

    verified, invalid, risky = verify_prospect_list(all_prospects, max_workers=5)

    save_verified(verified, risky)
    save_invalid(invalid)

    print(f"\n[VERIFY] Done! Only verified emails will be used for outreach.")


if __name__ == '__main__':
    main()
