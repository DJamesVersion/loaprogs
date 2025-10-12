import time
from datetime import datetime

# Calendar structure
MONTHS, WEEKS, DAYS = 14, 6, 5
HOURS, MINUTES, SECONDS, WHIKS = 9, 5, 4, 999
WHIKS_PER_SECOND = WHIKS
WHIKS_PER_MINUTE = SECONDS * WHIKS
WHIKS_PER_HOUR = MINUTES * WHIKS_PER_MINUTE
WHIKS_PER_DAY = HOURS * WHIKS_PER_HOUR
WHIKS_PER_YEAR = MONTHS * WEEKS * DAYS * WHIKS_PER_DAY

# Anchor date: Oct 14, 2025 UTC
ANCHOR = datetime(2025, 10, 14, 0, 0, 0)
KNOWN_NEW_MOON = datetime(2024, 10, 2, 18, 49)

# Phonology
phonology = {
    'a': "ariatnah", 'b': "batobwatchaeh", 'c': "c'illiatnah", 'd': "diadowatchaeh",
    'e': "eecheechuwah", 'f': "f'illianarre", 'g': "gagoikenne", 'h': "h'uilliatachaeh",
    'i': "illianarre", 'j': "ampejinne", 'k': "kajoinkenne", 'l': "lenemketobontette",
    'm': "momaw", 'n': "nona/nano", 'o': "oichenne", 'p': "perfuvium", 'q': "quaristenne",
    'r': "roykenne", 's': "stihuu/siataeh", 't': "tetnobautte/tahkmahnelle",
    'u': "uilliatachaeh", 'v': "vraelvrae", 'w': "weetus", 'x': "xiangxong",
    'y': "y'uilliatachaeh", 'z': "zazoykenne"
}
months = [phonology[c] for c in 'abcdefghijklmn']
weeks = [phonology[c] for c in 'opqrst']
days = [phonology[c] for c in 'uvwxy']

def lunar_phase(now):
    age = ((now - KNOWN_NEW_MOON).total_seconds()) / 86400 % 29.53059
    if age < 1.5: return "🌑 New Moon"
    elif age < 7.4: return "🌒 Waxing Crescent"
    elif age < 8.9: return "🌓 First Quarter"
    elif age < 14.7: return "🌔 Waxing Gibbous"
    elif age < 16.3: return "🌕 Full Moon"
    elif age < 22.1: return "🌖 Waning Gibbous"
    elif age < 23.6: return "🌗 Last Quarter"
    else: return "🌘 Waning Crescent"

def get_time():
    now = datetime.utcnow()
    whiks = int((now - ANCHOR).total_seconds() * WHIKS_PER_SECOND)
    year = whiks // WHIKS_PER_YEAR
    rem = whiks % WHIKS_PER_YEAR
    m = rem // (WEEKS * DAYS * WHIKS_PER_DAY); rem %= WEEKS * DAYS * WHIKS_PER_DAY
    w = rem // (DAYS * WHIKS_PER_DAY); rem %= DAYS * WHIKS_PER_DAY
    d = rem // WHIKS_PER_DAY; rem %= WHIKS_PER_DAY
    h = rem // WHIKS_PER_HOUR; rem %= WHIKS_PER_HOUR
    mi = rem // WHIKS_PER_MINUTE; rem %= WHIKS_PER_MINUTE
    s = rem // WHIKS_PER_SECOND
    wk = rem % WHIKS_PER_SECOND
    return {
        "year": year + 1,
        "month": months[m],
        "week": weeks[w],
        "day": days[d],
        "hour": h, "minute": mi, "second": s, "whik": wk,
        "arc": solar_arc(h, mi, wk),
        "moon": lunar_phase(now)
    }

def solar_arc(hour, minute, whik):
    total = hour * WHIKS_PER_HOUR + minute * WHIKS_PER_MINUTE + whik
    position = int(total / WHIKS_PER_DAY * 30)
    return "☀" + "—" * position + "◉" + "—" * (30 - position)

while True:
    t = get_time()
    print(f"\r{t['arc']} | {t['moon']} | Year {t['year']} | Month: {t['month']} | Week: {t['week']} | Day: {t['day']} | "
          f"{t['hour']:02}:{t['minute']:02}:{t['second']:02}:{t['whik']:03}", end="")
    time.sleep(1)
