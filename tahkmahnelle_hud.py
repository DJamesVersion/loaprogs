import time
import random
import sys
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.table import Table
from rich.text import Text
from rich.style import Style
from rich.progress_bar import ProgressBar
from rich.bar import Bar

# --- Setup and Global Constants ---
console = Console()
REFRESH_RATE = 1.0  # Seconds between screen updates
LORE_UPDATES = [
    "LOG: Deep Regolith Scan complete. Temple of Mars location confirmed, 98% probability.",
    "ALERT: Subterranean pressure spike detected near Lebus Lineage root section (Section C).",
    "STATUS: Elara Wilson's original Navigational Path integrity report validated (100%).",
    "REPORT: Crystal Moss harvest efficiency boosted by 15% following Sora Lebus algorithm update.",
    "NOTICE: External system broadcast detected from Jupiter Quadrant. Analysis pending...",
    "DATA: Tahkmahnelle-Tree Biometric Health Index: Optimum (99.98%).",
]

# Style definitions for the Sci-Fi aesthetic
STYLE_TITLE = Style(color="bright_cyan", bold=True, frame=True)
STYLE_HEADER = Style(color="yellow", bold=True, italic=True)
STYLE_SECTION = Style(color="green", bold=True)
STYLE_SUCCESS = Style(color="green", bold=True)
STYLE_ALERT = Style(color="red", bold=True)
STYLE_NORMAL = Style(color="white")
STYLE_DIM = Style(color="grey50", italic=True)

# --- Fictional Data Generation Functions ---

def get_random_finance_data():
    """Generates simulated financial data for stocks and credits."""
    return {
        "TechStocks_Wilson": round(random.uniform(95.0, 105.0), 2),
        "BioCredits_Lebus": round(random.uniform(1.2, 2.5), 2),
        "Science_R&D_Credit": random.randint(500, 950),
        "Total_Commonwealth_Treasury": random.randint(1_000_000, 5_000_000),
    }

def get_random_weather_data():
    """Generates simulated weather and environmental data for Tahkmahnelle45."""
    weather_states = ["Clear, Low Dust", "Regolith Storm Advisory", "Icy Micro-Meteor Shower", "Stable Atmosphere", "Thermal Anomaly Detected"]
    temp = random.randint(-180, -100)
    humidity = random.randint(5, 15)
    wind = random.randint(0, 50)
    
    return {
        "Atmosphere": random.choice(weather_states),
        "Temperature": f"{temp}°C (Stable)",
        "Ionosphere Wind Speed": f"{wind} km/h",
        "Humidity": f"{humidity}%",
    }

def get_random_tech_data():
    """Generates simulated technological attributes and advances."""
    return {
        "Tractor Beam Efficiency": random.randint(85, 100),
        "Arboreal Network Latency": round(random.uniform(0.01, 0.09), 3),
        "AI Co-Processor Load": random.randint(10, 70),
        "Life Extension Rate": round(random.uniform(0.8, 1.1), 2), # Fictional metric
    }

# --- Layout Components ---

def make_layout() -> Layout:
    """Define the basic structure of the HUD using Rich Layout."""
    layout = Layout(name="root")
    
    layout.split(
        Layout(name="header", size=3),
        Layout(name="main_body", ratio=3)
    )
    
    layout["main_body"].split_row(
        Layout(name="left_panel", ratio=2),
        Layout(name="center_panel", ratio=3),
        Layout(name="right_panel", ratio=2)
    )
    return layout

def get_header(current_time):
    """Generates the header panel."""
    current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
    header_text = Text.assemble(
        (f" Royal Tahkmahnelle Commonwealth Terminal  //  ", STYLE_TITLE),
        (f"System Time: {current_time_str}  //  ", STYLE_HEADER),
        (f"Tahkmahnelle45 Status: OPERATIONAL", STYLE_SUCCESS),
    )
    return Panel(header_text, style="bold blue on black", border_style="blue")

def get_weather_tech_panel(weather_data, tech_data):
    """Generates the weather patterns and technological attributes panel."""
    
    # 1. Weather Table
    weather_table = Table(title="Environmental Scan", title_style=STYLE_SECTION, show_header=False, expand=True, box=None)
    weather_table.add_column("Metric", style="yellow")
    weather_table.add_column("Value", style="white")
    
    for key, value in weather_data.items():
        weather_table.add_row(key, value)

    # 2. Tech Attributes Table
    tech_table = Table(title="Technological Attributes", title_style=STYLE_SECTION, show_header=False, expand=True, box=None)
    tech_table.add_column("Attribute", style="yellow")
    tech_table.add_column("Rating", style="white")

    for key, value in tech_data.items():
        rating_style = STYLE_SUCCESS if value > 90 else STYLE_NORMAL
        tech_table.add_row(key, Text(f"{value}%" if "Efficiency" in key or "Load" in key else str(value), style=rating_style))
        
    return Panel(
        weather_table.__rich__().append("\n").append(tech_table.__rich__()),
        title="[bold green]Planetar & Advancements[/bold green]",
        border_style="green"
    )

def get_finance_graph_panel(finance_data):
    """Generates the monetary values and stocks vs credit in sciences panel."""
    
    # 1. Stocks vs Credit Bar Chart
    stock_bar = Panel(
        Text("Wilson TechStocks: $105.00 (Max Value)", style=STYLE_DIM) + "\n" +
        Bar(
            size=105.0,
            width=50,
            style=Style(color="deep_sky_blue1"),
            finished_style=Style(color="deep_sky_blue1"),
            begin=0,
            end=finance_data["TechStocks_Wilson"]
        ).__rich__() + "\n" +
        Text("Lebus BioCredits: 2.5 (Max Value)", style=STYLE_DIM) + "\n" +
        Bar(
            size=2.5,
            width=50,
            style=Style(color="magenta"),
            finished_style=Style(color="magenta"),
            begin=0,
            end=finance_data["BioCredits_Lebus"]
        ).__rich__(),
        title="[bold yellow]Market & Dynasty Valuations[/bold yellow]",
        border_style="yellow"
    )

    # 2. Science Funding Gauge
    science_gauge = Panel(
        Text("Science R&D Funding Level (Max 1000 Cr)", style=STYLE_DIM) + "\n" +
        ProgressBar(
            total=1000,
            completed=finance_data["Science_R&D_Credit"],
            width=60,
            style=Style(color="bright_green"),
            complete_style=Style(color="bright_green"),
            finished_style=Style(color="green")
        ).__rich__(),
        title="[bold bright_green]Investment in Sciences[/bold bright_green]",
        border_style="bright_green"
    )

    return Panel(
        stock_bar.__rich__().append("\n").append(science_gauge.__rich__()),
        title="[bold bright_cyan]Financial & Credit Flow[/bold bright_cyan]",
        border_style="bright_cyan"
    )

def get_lore_panel():
    """Generates the Tahkmahnelle-Tree data source status and lore updates."""
    
    # Simulate a rolling lore update
    update = random.choice(LORE_UPDATES)
    update_style = STYLE_ALERT if "ALERT" in update else STYLE_NORMAL

    tree_status = Table(title="Tahkmahnelle-Tree Core Status", title_style=STYLE_SECTION, show_header=False, expand=True, box=None)
    tree_status.add_column("Metric", style="yellow")
    tree_status.add_column("Value", style="white")
    tree_status.add_row("Root Integrity:", "[bold green]100.0%[/bold green]")
    tree_status.add_row("Data Flow:", "[bold white]Nominal[/bold white]")
    tree_status.add_row("Mission Target:", "[bold red]Temple of Mars[/bold red]")

    lore_feed = Panel(
        tree_status.__rich__().append("\n").append(
            Text.assemble(("[-- LORE FEED --]\n", STYLE_DIM), (update, update_style))
        ),
        title="[bold magenta]The Great Tree's Conduit[/bold magenta]",
        border_style="magenta"
    )

    return lore_feed

def update_layout(layout: Layout):
    """Updates the content of the entire HUD layout with new simulated data."""
    current_time = time.localtime()
    
    finance_data = get_random_finance_data()
    weather_data = get_random_weather_data()
    tech_data = get_random_tech_data()
    
    layout["header"].update(get_header(current_time))
    layout["left_panel"].update(get_weather_tech_panel(weather_data, tech_data))
    layout["center_panel"].update(get_finance_graph_panel(finance_data))
    layout["right_panel"].update(get_lore_panel())


# --- Main Application Loop ---

def run_hud():
    """Initializes the HUD and runs the update loop."""
    layout = make_layout()
    
    # Use console.live to continuously refresh the terminal output
    with console.live(layout, screen=True, refresh_per_second=4) as live:
        console.print(Text("Initializing Tahkmahnelle Data Streams...", style=STYLE_SYSTEM))
        time.sleep(2) # Initializing delay
        
        while True:
            try:
                update_layout(layout)
                time.sleep(REFRESH_RATE)
            except KeyboardInterrupt:
                break
            except Exception as e:
                console.print(f"[bold red]System Error: {e}[/bold red]")
                time.sleep(5)
                
    console.print("\n[bold red]Tahkmahnelle HUD Offline. System Terminated.[/bold red]")


if __name__ == "__main__":
    try:
        run_hud()
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure 'rich' is installed: pip install rich")

