"""Quick test to parse Thomson Local and Made in Britain"""
import requests
from bs4 import BeautifulSoup
import collections

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

print("=== THOMSON LOCAL ===")
r = requests.get('https://www.thomsonlocal.com/search/manufacturer/london', headers=headers, timeout=10)
soup = BeautifulSoup(r.text, 'html.parser')

for h in soup.find_all(['h2','h3'])[:15]:
    txt = h.get_text(strip=True)
    if 3 < len(txt) < 80:
        link = h.find('a')
        href = link.get('href','') if link else ''
        print(f"  H: {txt} | {href}")

print("--- website links ---")
for a in soup.find_all('a', href=True):
    txt = a.get_text(strip=True).lower()
    href = a['href']
    if 'website' in txt or 'visit site' in txt:
        print(f"  Web: {txt} -> {href}")

print("--- classes ---")
classes = []
for div in soup.find_all('div', class_=True):
    for c in div.get('class', []):
        classes.append(c)
counter = collections.Counter(classes)
for c, n in counter.most_common(15):
    print(f"  {c}: {n}")

print("\n=== MADE IN BRITAIN ===")
r2 = requests.get('https://www.madeinbritain.org/members', headers=headers, timeout=10)
soup2 = BeautifulSoup(r2.text, 'html.parser')

for h in soup2.find_all(['h2','h3','h4'])[:15]:
    txt = h.get_text(strip=True)
    if 3 < len(txt) < 80:
        print(f"  H: {txt}")

print("--- member cards ---")
cards = soup2.find_all('div', class_=lambda c: c and ('member' in c.lower() or 'card' in c.lower()))
print(f"  Found {len(cards)} member cards")
for card in cards[:3]:
    print(f"  Card: {card.get_text(strip=True)[:100]}")

print("--- links ---")
for a in soup2.find_all('a', href=True)[:30]:
    href = a['href']
    txt = a.get_text(strip=True)
    if '/members/' in href and txt:
        print(f"  Member: {txt} -> {href}")
