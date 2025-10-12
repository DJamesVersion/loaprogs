import time
from datetime import datetime

# Time structure
MONTHS, WEEKS, DAYS = 14, 6, 5
HOURS, MINUTES, SECONDS, WHIKS = 9, 5, 4, 999

WHIKS_PER_SECOND = WHIKS
WHIKS_PER_MINUTE = SECONDS * WHIKS
WHIKS_PER_HOUR = MINUTES * WHIKS_PER_MINUTE
WHIKS_PER_DAY = HOURS * WHIKS_PER_HOUR
WHIKS_PER_YEAR = MONTHS * WEEKS * DAYS * WHIKS_PER_DAY

# Anchor date: Oct 14, 2025
ANCHOR = datetime(2025, 10, 14)

# Phonology mapping
phonology = {
    'a': "ariatnah", 'b': "batobwatchaeh", 'c': "c'illiatnah", 'd': "diadowatchaeh",
    'e': "eecheechuwah", 'f': "f'illianarre", 'g': "gagoikenne", 'h': "h'uilliatachaeh",
    'i': "illianarre", 'j': "ampejinne", 'k': "kajoinkenne", 'l': "lenemketobontette",
    'm': "momaw", 'n': "nona/nano", 'o': "oichenne", 'p': "perfuvium", 'q': "quaristenne",
    'r': "roykenne", 's': "stihuu/siataeh", 't': "tetnobautte/tahkmahnelle",
    'u': "uilliatachaeh", 'v': "vraelvrae", 'w': "weetus", 'x': "xiangxong",
    'y': "y'uilliatachaeh", 'z': "zazoykenne"
}

month_names = [phonology[c] for c in 'abcdefghijklmn']
week_names = [phonology[c] for c in 'opqrst']
day_names = [phonology[c] for c in 'uvwxy']

# Rituals at specific hours
rituals = {
    0: "✨ Lenemketobontette Dawn",
    2: "✨ Stihuu Day",
    4: "✨ Vraelvrae Day",
    6: "✨ Tahkmahnelle Gathering",
    7: "✨ Tetnobautte Tree Day"
}

# Seasonal markers every 8h cycle
seasons = ["🌗 Ariatnah Siataeh", "🌗 Ariatnah Stihuu", "🌗 Vraelvrae Siataeh", "🌗 Vraelvrae Stihuu"]
last_trigger = {"ritual": None, "season": None}

def get_ritual_time():
    now = datetime.utcnow()
    elapsed = (now - ANCHOR).total_seconds()
    whiks = int(elapsed * WHIKS_PER_SECOND)

    year = whiks // WHIKS_PER_YEAR
    rem = whiks % WHIKS_PER_YEAR

    month = rem // (WEEKS * DAYS * WHIKS_PER_DAY)
    rem %= WEEKS * DAYS * WHIKS_PER_DAY

    week = rem // (DAYS * WHIKS_PER_DAY)
    rem %= DAYS * WHIKS_PER_DAY

    day = rem // WHIKS_PER_DAY
    rem %= WHIKS_PER_DAY

    hour = rem // WHIKS_PER_HOUR
    rem %= WHIKS_PER_HOUR

    minute = rem // WHIKS_PER_MINUTE
    rem %= WHIKS_PER_MINUTE

    second = rem // WHIKS_PER_SECOND
    whik = rem % WHIKS_PER_SECOND

    cycle = ((datetime.utcnow() - ANCHOR).total_seconds()) // (HOURS * MINUTES * SECONDS)
    season = seasons[int(cycle) % 4]

    return {
        "year": year + 1,
        "month": month_names[month],
        "week": week_names[week],
        "day": day_names[day],
        "hour": hour,
        "minute": minute,
        "second": second,
        "whik": whik,
        "season": season
    }

# Display loop
while True:
    t = get_ritual_time()
    line = (f"\rYear {t['year']} | Month: {t['month']} | Week: {t['week']} | Day: {t['day']} | "
            f"{t['hour']:02}:{t['minute']:02}:{t['second']:02}:{t['whik']:03}")
    print(line, end="")

    # Ritual trigger
    if t['minute'] == 0 and t['second'] == 0 and t['whik'] < 10:
        if t['hour'] in rituals and last_trigger["ritual"] != t['hour']:
            print(f"\n{rituals[t['hour']]} begins.")
            last_trigger["ritual"] = t['hour']

    # Season trigger
    if t['hour'] == 0 and t['minute'] == 0 and t['second'] == 0 and t['whik'] < 10:
        if last_trigger["season"] != t['season']:
            print(f"\n{t['season']} begins.")
            last_trigger["season"] = t['season']

    time.sleep(0.05)# Logging function
def log_event(message):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    with open("ritual_log.txt", "a") as f:
        f.write(f"[{timestamp}] {message}\n")

# Display loop with logging
while True:
    t = get_ritual_time()
    line = (f"\rYear {t['year']} | Month: {t['month']} | Week: {t['week']} | Day: {t['day']} | "
            f"{t['hour']:02}:{t['minute']:02}:{t['second']:02}:{t['whik']:03}")
    print(line, end="")

    # Ritual trigger
    if t['minute'] == 0 and t['second'] == 0 and t['whik'] < 10:
        if t['hour'] in rituals and last_trigger["ritual"] != t['hour']:
            msg = f"{rituals[t['hour']]} begins."
            print(f"\n{msg}")
            log_event(msg)
            last_trigger["ritual"] = t['hour']

    # Season trigger
    if t['hour'] == 0 and t['minute'] == 0 and t['second'] == 0 and t['whik'] < 10:
        if last_trigger["season"] != t['season']:
            msg = f"{t['season']} begins."
            print(f"\n{msg}")
            log_event(msg)
            last_trigger["season"] = t['season']

    time.sleep(0.05)
