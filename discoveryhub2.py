# /DiscoveryHub_v2/
# │
# ├── main.py                     # Main script to launch the app
# │
# ├── data/
# │   ├── organizations.json        # Base info, tags, and RSS feed URLs
# │   └── user_data.db              # SQLite DB for 'My Log' and user settings
# │
# ├── assets/
# │   ├── icons/
# │   └── images/
# │
# ├── core/
# │   ├── data_handler.py           # Manages fetching/saving data from JSON/DB
# │   ├── news_fetcher.py           # Module for parsing RSS feeds
# │   └── event_scraper.py          # Module for scraping event info
# │
# └── ui/
#     ├── main_window.py            # Main window, now includes event calendar logic
#     ├── home_screen.py            # Home screen with new tag filtering
#     ├── org_profile_widget.py     # Template with tabs for About, News, etc.
#     ├── log_screen.py
#     └── settings_screen.py        # New widget for app settings
