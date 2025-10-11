import sys

# --- Data Definition ---
# The core data structure containing the fictional medical/quantum information.
EXPLORER_DATA = {
    "bunnies and rainbows": {
        "description": "A hyper-chromatic contagion resulting from the over-saturation of joy in the limbic system, manifesting as spontaneous, gentle hopping and optical distortion.",
        "antidote_stasis": "The deliberate consumption of monochrome textures while listening to Gregorian chant.",
        "quantum_effect": "Induces counter-harmonic feedback loops, causing Abstract Expressionist paintings to hum the B-flat minor scale.",
    },
    "youth in asia": {
        "description": "A temporary spatio-temporal dislocation of youthful exuberance, causing individuals to suddenly prefer the company of wise, but grumpy, garden gnomes.",
        "antidote_stasis": "A 10-second blast of pure 1980s synth-pop played through a rusty tuba.",
        "quantum_effect": "Freezes rhythmic complexity (tachyons) in music scores, allowing composers to re-sequence Baroque concertos via interpretive dance.",
    },
    "blisterfist": {
        "description": "A condition where overzealous conviction solidifies into keratinized, high-impact metacarpals, ideal for emphatically pointing at things.",
        "antidote_stasis": "Immersion of the fist in lukewarm, slightly used tea while reciting the quadratic formula backwards.",
        "quantum_effect": "Generates resonant frequencies that cause terracotta sculptures to debate the proper use of negative space in sonatas.",
    },
    "blue hero": {
        "description": "An emotional state of benign, quiet melancholy where the subject believes they are the unsung protagonist of a low-budget 1970s Polish sci-fi film.",
        "antidote_stasis": "A meal consisting entirely of burnt toast and a glass of milk, served under a single spotlight.",
        "quantum_effect": "Creates 'acoustic mirroring' where a listener's emotional state dictates the key signature of the piece being played.",
    },
    "grass blues": {
        "description": "Photosynthetic depression resulting from insufficient atmospheric oxygen exchange with the emotional centers of terrestrial flora.",
        "antidote_stasis": "Writing 100 thank-you notes to various moss species on recycled paper.",
        "quantum_effect": "Allows the quantum entanglement between a viewer's eye movements and the brushstrokes of a Van Gogh to be perceived as a gentle, low-frequency drone.",
    },
    "od duck": {
        "description": "A mutation of the ordinary, leading to an irresistible urge to wear mismatched socks and only communicate using excerpts from 18th-century naval logs.",
        "antidote_stasis": "The successful completion of a jigsaw puzzle *after* realizing it contains pieces from three different sets.",
        "quantum_effect": "Enables 'Symbiotic Entropy' to be temporarily stabilized, resulting in a perfectly harmonious, yet rapidly deteriorating, 12-tone composition.",
    },
    "your favorite vegetable": {
        "description": "A philosophical quandary where the preferred root/leaf/fruit becomes a psychological anchor, granting minor telekinetic abilities related *only* to other vegetables.",
        "antidote_stasis": "The act of perfectly peeling an orange without breaking the skin, and then not eating it.",
        "quantum_effect": "The sound of a single, perfectly timed raindrop becomes the master conductor, synchronizing the decay of analog sound and digital video.",
    },
    "giraffe in the jug full of jelly": {
        "description": "A cognitive instability caused by over-reliance on paradoxical metaphors, leading to an excessive consumption of grape preserves and an inability to use prepositions correctly.",
        "antidote_stasis": "Constructing a tiny, accurate scale model of the jug, the jelly, and the giraffe, using only lint and regret.",
        "quantum_effect": "Warps musical tempo based on the artist's perceived altitude, causing slow, heavy music at 'sea level' and frantic jazz at 'mountain heights.'",
    },
}

def display_menu():
    """Displays the main menu of the medical explorer."""
    print("\n" + "="*50)
    print("  QUANTUM PARALLELS MEDICAL EXPLORER v1.0")
    print("  Analysis of Symbiotic Entropy Groups")
    print("="*50)
    
    concepts = list(EXPLORER_DATA.keys())
    
    for i, concept in enumerate(concepts):
        # Format the option number and capitalize the concept name for readability
        display_name = concept.title()
        print(f"  [{i + 1}] {display_name}")
    
    print("\n  [Q] Quit Explorer")
    print("-" * 50)

def display_concept_info(concept_key):
    """Displays the detailed analysis for a chosen concept."""
    data = EXPLORER_DATA[concept_key]
    
    print("\n" + "#"*60)
    print(f"  EXPLORER ANALYSIS: {concept_key.upper()}")
    print("#"*60)
    
    # Description
    print("\n[ Pathological Description (The Parallel) ]")
    print(f"  >> {data['description']}")
    
    # Antidote/Stasis
    print("\n[ Antidote / Stasis Protocol ]")
    print(f"  >> {data['antidote_stasis']}")
    
    # Quantum Effect
    print("\n[ Symbiotic Entropy in Quantum Realms of Music and Art ]")
    print(f"  >> {data['quantum_effect']}")
    
    print("\n" + "="*60 + "\n")

def medical_explorer_app():
    """The main interactive loop for the terminal application."""
    while True:
        display_menu()
        
        # Get user input
        user_input = input("Enter selection [1-8 or Q]: ").strip().lower()
        
        # Handle Quit
        if user_input == 'q':
            print("\nExiting the Quantum Parallels Medical Explorer. May your entropy remain stable.")
            sys.exit(0)
            
        # Handle Numeric Selection
        try:
            selection = int(user_input)
            concepts = list(EXPLORER_DATA.keys())
            
            if 1 <= selection <= len(concepts):
                concept_key = concepts[selection - 1]
                display_concept_info(concept_key)
                
                # Wait for user to continue before returning to menu
                input("Press Enter to return to the main menu...")
            else:
                print(f"Error: Selection '{user_input}' is out of range. Please choose a number between 1 and {len(concepts)}.")
                
        except ValueError:
            # Handle non-numeric and invalid input
            if user_input != 'q':
                 print(f"Error: Invalid input '{user_input}'. Please enter a valid option number or 'Q'.")

if __name__ == "__main__":
    medical_explorer_app()

