import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.tree import Tree
from rich.style import Style
from rich.table import Table

# --- Setup and Data ---

# Initialize the rich console
console = Console()

# Defined styles for the "graphically advanced" presentation
STYLE_TITLE = Style(color="bright_cyan", bold=True, frame=True)
STYLE_FAMILY_NAME = Style(color="yellow", bold=True)
STYLE_MEMBER_NAME = Style(color="green", bold=True)
STYLE_LORE = Style(color="light_steel_blue")
STYLE_OBJECTIVE = Style(color="red", bold=True, italic=True)
STYLE_SYSTEM = Style(color="grey50")

# Core data for the Wilson and Lebus families and the Tahkmahnelle lore
FAMILY_TREE_DATA = {
    "The Great Tahkmahnelle-Tree (Tahkmahnelle45 Core)": {
        "color": "bright_green",
        "description": "The ancient, biomechanically-augmented Oak at the heart of the dwarf planet. Its roots form the primary network connecting the Wilson and Lebus dynasties.",
        "children": {
            "The Wilson Lineage (Navigators & Metallurgists)": {
                "color": "deep_sky_blue1",
                "description": "Known for their mastery of space travel and the creation of advanced regolith-processing alloys.",
                "members": {
                    "Elara Wilson (The Founder)": "Chief Navigator. Specialized in biometallurgy and laid the path to the 'Lands of Ages'.",
                    "Kael Wilson (Current Matriarch)": "Root Node Guardian. Oversees the integration of all system data and celestial alignments.",
                    "Jax Wilson": "Regolith Explorer. Currently charting the deepest caverns toward the Temple's subterranean entrance."
                }
            },
            "The Lebus Lineage (Engineers & Archivists)": {
                "color": "magenta",
                "description": "Keepers of the Arboreal Memory System and maintainers of the Great Oak's complex life support.",
                "members": {
                    "Roric Lebus (The First Archivist)": "Designer of the Tree's digital memory core and historical lexicon.",
                    "Sora Lebus": "Lead Biometrician. Studies the rare crystal moss required for regolith journey survival.",
                    "Zane Lebus": "Core System Engineer. Ensures the energy flow is sufficient for the long transit to the Temple of Mars."
                }
            }
        }
    }
}

# --- Functions ---

def display_welcome_screen():
    """Displays the initial, colorful title screen and lore introduction."""
    console.print(Panel(
        Text("TAHKMAHNELLE-TREE: FAMILY LORE SYSTEM", justify="center", style=STYLE_TITLE),
        title="[bold yellow]Access Terminal: Dwarf Planet Tahkmahnelle45[/bold yellow]",
        border_style="green",
        style="on black"
    ))
    console.print()
    console.print(Text.assemble(
        (f"Welcome, Initiate. You are viewing the core data system of ", STYLE_LORE),
        ("Tahkmahnelle45", STYLE_FAMILY_NAME),
        (", the celestial body where the ", STYLE_LORE),
        ("Great Oak Tahkmahnelle-Tree", STYLE_FAMILY_NAME),
        (" grows. This tree is the unified archive of the ", STYLE_LORE),
        ("Wilson", Style(color="deep_sky_blue1", bold=True)),
        (" and ", STYLE_LORE),
        ("Lebus", Style(color="magenta", bold=True)),
        (" families, central to the mission to the Lands of Ages.", STYLE_LORE),
        (f"\n\nObjective: ", STYLE_OBJECTIVE),
        ("Traverse the Regolith to the Temple of Mars.", STYLE_OBJECTIVE)
    ), justify="center")
    console.print("-" * console.width, style=STYLE_SYSTEM)
    console.print()


def create_family_tree_visualization():
    """Generates the Rich Tree visualization of the family data."""
    root_key = list(FAMILY_TREE_DATA.keys())[0]
    root_data = FAMILY_TREE_DATA[root_key]

    # Create the main root node (The Great Tree)
    tree = Tree(
        f"[{root_data['color']} bold]{root_key}[/{root_data['color']} bold]\n" +
        f"[grey50 italic]{root_data['description']}[/grey50 italic]",
        guide_style=Style(color="dim green")
    )

    # Add the main lineages (Wilson and Lebus)
    for lineage_key, lineage_data in root_data["children"].items():
        lineage_node = tree.add(
            f"[{lineage_data['color']} bold]{lineage_key}[/{lineage_data['color']} bold]\n" +
            f"[grey70]{lineage_data['description']}[/grey70]",
            guide_style=Style(color=lineage_data['color'])
        )

        # Add individual family members
        for member_name, details in lineage_data["members"].items():
            lineage_node.add(
                f"[white]{member_name}[/white]\n" +
                f"[italic]{details}[/italic]",
                Style(color="dark_khaki", bold=False)
            )

    return tree

def display_member_details():
    """Displays detailed biographies of all key family members in a table."""
    table = Table(title="Family Biometric Archive (Wilson & Lebus)", title_style=STYLE_FAMILY_NAME, show_header=True, header_style="bold blue")
    table.add_column("Lineage", style="yellow")
    table.add_column("Member", style="green")
    table.add_column("Role & Lore Detail", style="white")

    for root_key, root_data in FAMILY_TREE_DATA.items():
        for lineage_key, lineage_data in root_data["children"].items():
            lineage = "Wilson" if "Wilson" in lineage_key else "Lebus"
            for member_name, details in lineage_data["members"].items():
                table.add_row(lineage, member_name, details)

    console.print(table)
    console.print()
    console.input("[bold yellow]Press [Enter] to return to the main menu...[/bold yellow]")


def start_regolith_journey():
    """Starts the final narrative game objective."""
    console.clear()
    console.print(Panel(
        Text("REGOLITH TRAVERSAL INITIATED", justify="center", style=Style(color="red", bold=True, frame=True)),
        title="[bold red]Lands of Ages: Temple Approach[/bold red]",
        border_style="red"
    ))
    console.print(Text.assemble(
        ("The journey begins. You are at the base of the Tahkmahnelle-Tree, where the final, deepest root penetrates the planet's ", STYLE_LORE),
        ("regolith", Style(color="dim", italic=True)),
        (". The air is thick with ionized dust and the scent of ancient Martian soil.\n\n", STYLE_LORE),
        ("Your task, bestowed by the combined Wilson and Lebus knowledge, is to navigate the Labyrinth of Ages. You hold Jax Wilson's latest map and carry Sora Lebus's crystal moss preservation kit.\n\n", Style(color="white")),
        ("The path splits: \n", Style(color="yellow")),
        ("1. Take the [bold green]East Passage[/bold green] (The path of the Navigators, known for high winds).\n", Style(color="green")),
        ("2. Take the [bold magenta]West Descent[/bold magenta] (The path of the Archivists, known for stable but collapsing structures).", Style(color="magenta")),
        ("\n\n(Note: This is the end of the current lore simulation. The choice marks the beginning of your grand journey.)", STYLE_SYSTEM)
    ))
    choice = console.input("\n[bold]Enter your choice (1 or 2) to continue the story...[/bold]: ")

    if choice == '1':
        console.print("\n[bold green]You chose the East Passage.[/bold green] The winds buffet your suit, but the Wilson GPS system guides you true, closer to the Temple's signal beacon. The journey is harsh, but clear.")
    elif choice == '2':
        console.print("\n[bold magenta]You chose the West Descent.[/bold magenta] The ground trembles. You rely on the structural knowledge passed down by the Lebus lineage, carefully stepping over ancient, crumbling Martian infrastructure.")
    else:
        console.print("\n[bold yellow]Invalid choice.[/bold yellow] The system defaults to the safest route, following the established protocols of the Great Tree.")

    console.print("\n[bold red]MISSION ACCOMPLISHED: LORE SIMULATION ENDED.[/bold red]")


def main_menu():
    """Main application loop."""
    while True:
        console.clear()
        display_welcome_screen()

        menu = Panel(
            Text.assemble(
                ("1. Display the Colorful Tahkmahnelle-Tree Structure\n", Style(color="yellow")),
                ("2. View Detailed Family Member Biographies\n", Style(color="cyan")),
                ("3. [GAME START] Begin the Regolith Journey to the Temple of Mars\n", Style(color="red", bold=True)),
                ("4. Exit System\n", STYLE_SYSTEM)
            ),
            title="[bold white]Main Menu[/bold white]",
            border_style="blue"
        )
        console.print(menu)

        choice = console.input("\nEnter your selection (1-4): ")

        if choice == '1':
            console.clear()
            console.print(Panel(
                create_family_tree_visualization(),
                title="[bold bright_green]Tahkmahnelle-Tree Visualization[/bold bright_green]",
                border_style="green"
            ))
            console.input("\n[bold yellow]Press [Enter] to return to the main menu...[/bold yellow]")
        elif choice == '2':
            console.clear()
            display_member_details()
        elif choice == '3':
            start_regolith_journey()
            break  # Exit the main loop after starting the journey
        elif choice == '4':
            console.print("\n[bold red]Tahkmahnelle System Shutting Down. Farewell.[/bold red]")
            sys.exit()
        else:
            console.print("\n[bold red]Invalid option. Please choose 1, 2, 3, or 4.[/bold red]")
            console.input("[bold yellow]Press [Enter] to continue...[/bold yellow]")


if __name__ == "__main__":
    try:
        main_menu()
    except ImportError:
        # Fallback if rich is not installed, printing the key information
        print("ERROR: The 'rich' library is required for the colorful, graphically advanced display.")
        print("Please run: pip install rich")
        print("\n--- Displaying essential Family Tree data (Text-Only) ---")
        for lineage, data in {k: v for k in FAMILY_TREE_DATA for k,v in FAMILY_TREE_DATA.items()}[list(FAMILY_TREE_DATA.keys())[0]]['children'].items():
            print(f"\n[{lineage.upper()}] - {data['description']}")
            for member, role in data['members'].items():
                print(f"  - {member}: {role}")
        print("\nObjective: Traverse the Regolith to the Temple of Mars.")

