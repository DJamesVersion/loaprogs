import time
from datetime import datetime

# Time units
SECONDS_PER_MINUTE = 80
MINUTES_PER_HOUR = 12
HOURS_PER_DAY = 24
WHIKS_PER_SECOND = 999

# Calendar structure
DAYS_PER_WEEK = 7
WEEKS_PER_MONTH = 6
MONTHS_PER_YEAR = 8
DAYS_PER_MONTH = DAYS_PER_WEEK * WEEKS_PER_MONTH
DAYS_PER_YEAR = DAYS_PER_MONTH * MONTHS_PER_YEAR

# New Year anchor
NEW_YEAR_MONTH = 10
NEW_YEAR_DAY = 14
LORE_YEAR_AT_2025 = 222110

# Seasonal markers
SEASONAL_DAYS = {
    0: "🌑 New Year",
    84: "🌸 Equinox I",
    168: "☀️ Solstice",
    252: "🍂 Equinox II"
}

# Lore events
LORE_EVENTS = {
    13: "🕯️ Day of Whik Resonance",
    222: "🌀 Festival of Stihuu",
    335: "🔥 Last Day of the Cycle"
}

# Ritual triggers
def ritual_trigger(day_index, whik):
    rituals = []
    if whik == 999:
        rituals.append("✨ Whik Alignment: Portal shimmer detected")
    if day_index in SEASONAL_DAYS:
        rituals.append("🔔 Seasonal Rite: Prepare offerings")
    if day_index == 0 and whik < 10:
        rituals.append("🌟 Genesis Pulse: Begin the new cycle")
    if day_index == 222 and whik == 222:
        rituals.append("🌀 Stihuu Spiral: Time folds inward")
    return rituals

# Names
MONTH_NAMES = [
    "ariatnah", "batobwatchaeh", "c'illiatnah", "diadowatchaeh",
    "eecheechuwah", "f'illianarre", "gagoikenne", "h'uilliatachaeh"
]
WEEK_NAMES = [
    "tetnobautte", "tahkmahnelle", "quaristenne",
    "roykenne", "vraelvrae", "weetus"
]
DAY_NAMES = [
    "stihuu", "siataeh", "uilliatachaeh",
    "y'uilliatachaeh", "kajoinkenne", "lenemketobontette", "perfuvium"
]

def get_lore_year(now):
    current = datetime(now.year, NEW_YEAR_MONTH, NEW_YEAR_DAY)
    if now < current:
        return LORE_YEAR_AT_2025 + (now.year - 2025 - 1)
    else:
        return LORE_YEAR_AT_2025 + (now.year - 2025)

def get_day_index(now):
    year = now.year
    new_year = datetime(year, NEW_YEAR_MONTH, NEW_YEAR_DAY)
    if now < new_year:
        new_year = datetime(year - 1, NEW_YEAR_MONTH, NEW_YEAR_DAY)
    return (now - new_year).days % DAYS_PER_YEAR

def get_calendar_position(day_index):
    month = day_index // DAYS_PER_MONTH
    week = (day_index % DAYS_PER_MONTH) // DAYS_PER_WEEK
    day = day_index % DAYS_PER_WEEK
    return MONTH_NAMES[month], WEEK_NAMES[week], DAY_NAMES[day]

def get_custom_time(now):
    seconds = now.hour * 3600 + now.minute * 60 + now.second + now.microsecond / 1e6
    hour = int(seconds // 3600)
    rem = seconds % 3600
    minute = int((rem / 3600) * MINUTES_PER_HOUR)
    second = int(((rem / 3600) * MINUTES_PER_HOUR - minute) * SECONDS_PER_MINUTE)
    whik = int((((rem / 3600) * MINUTES_PER_HOUR - minute) * SECONDS_PER_MINUTE - second) * WHIKS_PER_SECOND)
    return hour, minute, second, whik

def log_to_scroll(text):
    with open("vraelvrae_scroll.txt", "a", encoding="utf-8") as f:
        f.write(text + "\n")

def display_clock():
    pulse = ["", "•", "◦", "∙", "✶", ""]  # Whik shimmer cycle
    pulse_index = 0
    while True:
        now = datetime.now()
        lore_year = get_lore_year(now)
        day_index = get_day_index(now)
        month, week, day = get_calendar_position(day_index)
        hour, minute, second, whik = get_custom_time(now)

        season = SEASONAL_DAYS.get(day_index, "")
        event = LORE_EVENTS.get(day_index, "")
        rituals = ritual_trigger(day_index, whik)

        # Build display
        print("\033c", end="")  # Clear screen
        print(f"🌌 VraelvraeStihuu Year: {lore_year}")
        print(f"📅 Date: Month {month}, Week {week}, Day {day}")
        if season:
            print(f"{season}")
        if event:
            print(f"{event}")
        print(f"🕰️ Time: {hour:02d}:{minute:02d}:{second:02d}.{whik:03d}")
        print(f"(24h • 12m/h • 80s/m • 999 whiks/s)")
        print(f"💫 Whik Pulse: {pulse[pulse_index % len(pulse)]}")
        if rituals:
            print("🔮 Rituals:")
            for r in rituals:
                print(f"   {r}")

        # Log to scroll
        log_entry = f"{now.isoformat()} | Year {lore_year} | {month}/{week}/{day} | {hour}:{minute}:{second}.{whik} | Rituals: {', '.join(rituals) if rituals else '—'}"
        log_to_scroll(log_entry)

        pulse_index += 1
        time.sleep(0.5)

if __name__ == "__main__":
    display_clock()
