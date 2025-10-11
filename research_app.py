import json
import textwrap

# --- Knowledge Base Data ---
# This dictionary contains the synthesized research data for the specified organizations.
RESEARCH_DATABASE = {
    "Planetary Society": {
        "focus": "Space advocacy, planetary science, and exploration.",
        "mission": "Empowering the world's citizens to advance space science and exploration, particularly through the core enterprises of Explore Worlds, Find Life, and Defend Earth.",
        "key_activities": [
            "Advocacy for robust NASA funding and space policies (e.g., Day of Action).",
            "Innovative technology projects, such as the LightSail solar sailing spacecraft.",
            "Public outreach via The Planetary Report magazine and educational events."
        ],
        "domain": "Space Exploration & Advocacy"
    },
    "National Space Society": {
        "focus": "Promoting the creation of a spacefaring civilization and space settlement.",
        "mission": "To promote social, economic, technological, and political change in order to expand civilization beyond Earth.",
        "key_activities": [
            "Hosting the International Space Development Conference (ISDC).",
            "Publishing the space interest magazine Ad Astra.",
            "Running educational competitions like the Gerard K. O'Neill Space Settlement Contest."
        ],
        "domain": "Space Advocacy & Settlement"
    },
    "Smithsonian National Air and Space Museum": {
        "focus": "Collecting, preserving, and exhibiting historic aircraft and spacecraft.",
        "mission": "To explore and present the history, science, technology, and social impact of aeronautics and spaceflight.",
        "key_activities": [
            "Maintaining the world's largest collection of aviation and space artifacts (nearly 70,000 objects).",
            "Conducting research through the Center for Earth and Planetary Studies.",
            "Operating two landmark facilities in Washington, D.C., and Chantilly, VA (Udvar-Hazy Center)."
        ],
        "domain": "Aeronautics & Space History"
    },
    "American Air Museum in Britain": {
        "focus": "Anglo-American air power and collaboration in 20th and 21st-century conflicts.",
        "mission": "To tell the personal stories of those whose lives shaped or were shaped by American air power operating from British soil, particularly during WWII.",
        "key_activities": [
            "Exhibiting historic aircraft (e.g., B-29 Superfortress, SR-71 Blackbird).",
            "Serving as a memorial to the US airmen and women killed while serving from Great Britain during WWII.",
            "Located at the Imperial War Museum (IWM) Duxford."
        ],
        "domain": "Military Aviation History"
    },
    "Paleontological Society": {
        "focus": "Advancing knowledge and understanding of the evolution of life through fossils.",
        "mission": "To advance knowledge of paleontology and understanding of the evolution of life through research, education and advocacy.",
        "key_activities": [
            "Publishing leading scientific journals, including the Journal of Paleontology and Paleobiology.",
            "Hosting annual meetings and the North American Paleontological Convention.",
            "Providing research grants and internships to students and early career paleontologists."
        ],
        "domain": "Earth Science & Paleontology"
    },
    "BOINC": {
        "focus": "Open-source middleware for volunteer (distributed) computing.",
        "mission": "To enable researchers to utilize the massive processing resources of personal computers and devices volunteered by the public globally.",
        "key_activities": [
            "Providing the platform for major scientific projects (e.g., SETI@home, Einstein@Home, LHC@home).",
            "Using idle CPU and GPU cycles from devices to perform complex scientific calculations.",
            "The name stands for 'Berkeley Open Infrastructure for Network Computing'."
        ],
        "domain": "Distributed Computing"
    },
    "ITU": {
        "focus": "The leading specialized United Nations agency for information and communication technologies (ICTs).",
        "mission": "To promote, facilitate and foster affordable and universal access to telecommunication/ICT networks and services for sustainable development.",
        "key_activities": [
            "Allocating global radio-frequency spectrum and satellite orbits (Radiocommunication Sector).",
            "Developing international standards for ICTs (Standardization Sector).",
            "Assisting developing countries in telecommunication deployment and policy (Development Sector)."
        ],
        "domain": "Global Telecommunications & Policy"
    }
}

class ResearchApp:
    """
    A class to manage and retrieve information from the research database.
    """
    def __init__(self, database):
        self.database = database
        self.org_names = list(database.keys())

    def format_info(self, name, data):
        """Formats the organization data into a readable string."""
        title = f"--- Research Summary: {name} ---"
        separator = "-" * len(title)
        
        output = [
            separator,
            f"Focus: {data['focus']}",
            f"Mission: {data['mission']}",
            f"Domain: {data['domain']}",
            "\nKey Activities:",
            textwrap.indent("\n".join(f"- {act}" for act in data['key_activities']), '  ')
        ]
        return "\n".join(output)

    def search_organization(self, query):
        """
        Searches the database for a matching organization name, prioritizing exact matches.
        Returns the formatted information or an error message.
        """
        # Clean query for comparison
        clean_query = query.strip().lower()

        # 1. Exact or near-exact match
        for name, data in self.database.items():
            if name.lower() == clean_query or clean_query in [alias.lower() for alias in name.split()]:
                return self.format_info(name, data)

        # 2. Contains query (e.g., searching "space" finds multiple)
        matches = {name: data for name, data in self.database.items() 
                   if clean_query in name.lower() or clean_query in data['domain'].lower()}

        if matches:
            if len(matches) == 1:
                name, data = list(matches.items())[0]
                return self.format_info(name, data)
            else:
                return f"\nFound multiple matches for '{query}'. Please be more specific or choose from the list:\n- " + "\n- ".join(matches.keys())

        return f"\nError: No information found for '{query}'. Please try a different query or list all organizations using 'list'."

    def display_all_organizations(self):
        """Displays a numbered list of all organizations in the database."""
        output = ["\n--- Available Organizations ---"]
        for i, name in enumerate(self.org_names, 1):
            output.append(f"{i}. {name} (Domain: {self.database[name]['domain']})")
        output.append("\nEnter the full name or a key term to search (e.g., 'Paleontological' or 'Space Society').\n")
        return "\n".join(output)

def main():
    """The main function for the command-line interface."""
    app = ResearchApp(RESEARCH_DATABASE)
    print("\n--- Scientific & Technical Organizations Knowledge Base ---")
    print("Welcome! Type 'list' to see all organizations, or enter a name to search.")
    print("Type 'quit' or 'exit' to close the application.")

    app.display_all_organizations()

    while True:
        try:
            user_input = input("\nEnter query (or 'list' / 'quit'): ").strip()

            if user_input.lower() in ['quit', 'exit']:
                print("\nThank you for using the Research Knowledge Base. Goodbye!")
                break

            if not user_input:
                continue

            if user_input.lower() == 'list':
                print(app.display_all_organizations())
                continue

            result = app.search_organization(user_input)
            print(result)

        except Exception as e:
            print(f"An unexpected error occurred: {e}. Please try again.")

if __name__ == "__main__":
    main()

