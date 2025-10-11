import sys
import time

# --- Puzzle Definitions ---
# Each puzzle represents a challenge JW must overcome during an exploration of WilAllen Acres.
PUZZLES = [
    {
        "title": "Trial 1: The Hermit's Gift (Abstract Logic)",
        "puzzle": (
            "The Hermit of the Whispering Falls gifted JW this riddle: I am the void between the trees, "
            "the pause before the bear's strike, and the measure of respect the ancient stones demand. "
            "I am the vessel into which all rumors vanish, and the only thing the Falls truly possess. "
            "To break me is to learn the secret; to seek me is to find rest. What am I?"
        ),
        "answer": "SILENCE",
        "hint": "Think about what is missing when the world is busy. It is a fundamental condition of deep contemplation."
    },
    {
        "title": "Trial 2: The Locked Gate of the Ruins (Numerical Deduction)",
        "puzzle": (
            "A forgotten metal gate blocks JW's path to the Old Manse. It has a 4-digit mechanical code that follows these rules:\n"
            "1. The first digit is triple the second.\n"
            "2. The third digit is half the fourth.\n"
            "3. The sum of all four digits is exactly 18.\n"
            "4. No digit is zero.\n"
            "What is the 4-digit code JW must enter? (Enter as a single number)"
        ),
        "answer": "9324",
        "hint": "Start by identifying the possible pairs for the first two digits (e.g., 9 and 3) and the last two digits (e.g., 2 and 4), then find the combination that sums to 18."
    },
    {
        "title": "Trial 3: The Forgotten Research (Radioactive Decay)",
        "puzzle": (
            "In the ruined lab, JW finds two vials. Vial A holds 100 grams of Element X (Decay time: 2 hours). "
            "Vial B holds Element Y (Decay time: 4 hours). 'Decay Time' means half the material is gone in that time. "
            "After exactly 4 hours, the remaining mass in Vial A is *one-tenth* the mass remaining in Vial B. "
            "What was the original mass of Element Y in grams when the experiment began? (Enter the number only)"
        ),
        "answer": "500",
        "hint": "Element X (2-hour decay time) will have $100 / 2^2$ grams remaining after 4 hours. Use that remaining mass to calculate the original mass of Y."
    },
    {
        "title": "Trial 4: The Raven's Crag Descent (Physical Logic)",
        "puzzle": (
            "JW must descend the 50-cubit-high Raven's Crag using only two ropes: one 40 cubits and one 30 cubits. "
            "There is a single, fixed iron spike at the top. The ropes cannot be cut or permanently knotted, but can be temporarily looped around the spike. "
            "How does JW combine the ropes to reach the ground? (Describe the core action using 'Loop'/'Tie' and the rope lengths, e.g., LOOP X TIE Y)"
        ),
        "answer": "LOOP 40 TIE 30",
        "hint": "Looping a rope splits it into two equal lengths hanging down. The goal is to create a total length of 50 cubits reaching the bottom."
    },
    {
        "title": "Trial 5: The Shifting Sands Disease (Symptom Identification)",
        "puzzle": (
            "A local explorer, injured near the Shifting Sands, shows high fever, uncontrollable shaking, confusion, and rapid weight loss—typical symptoms of a severe infection. "
            "However, the explorer also claims to briefly see people who vanished years ago. "
            "Based *only* on the common physical symptoms (fever, shaking, confusion) and the nature of WilAllen's swampy areas, which scientific class of infectious *organism* is the most likely cause of the infection? (One scientific class of organism, e.g., 'Virus', 'Fungus', 'Bacteria')"
        ),
        "answer": "BACTERIA",
        "hint": "The core symptoms strongly suggest a common, treatable infection that often spreads by water or insects, requiring a specific class of antibiotics."
    },
    {
        "title": "Trial 6: The Scavenger's Path (Relative Time)",
        "puzzle": (
            "Four scavengers—Alpha, Beta, Gamma, Delta—return to camp after a long day of searching. Alpha arrived 1 hour before Gamma. Beta arrived 1 hour after Delta. Gamma arrived 2 hours after Delta. "
            "What is the minimum possible time gap, measured in hours, between the first scavenger's arrival and the last scavenger's arrival? (Enter the number only)"
        ),
        "answer": "2",
        "hint": "Establish the arrival times of all four relative to Delta (T=0). You will find that some scavengers arrived at the same time."
    },
    {
        "title": "Trial 7: The Relic Thief's Defense (Legal Intent)",
        "puzzle": (
            "JW pursues a thief charged with 'Knowingly removing a priceless artifact of spiritual value.' "
            "The defense successfully proves the artifact was spiritually worthless. The prosecution then proves the accused was *unaware* that removing it was forbidden. "
            "Which successful defense argument (Spiritual Value or Awareness of Prohibition) is the primary reason the accused must be found 'Not Guilty' of *this specific charge*?"
        ),
        "answer": "AWARENESS OF PROHIBITION",
        "hint": "Focus on the legal intent required by the word 'Knowingly'—the mental state of the accused."
    },
    {
        "title": "Trial 8: The Arcane Scroll (Fundamental Concept)",
        "puzzle": (
            "The final object JW finds is an Arcane Scroll. It reads: I am spoken without a body, and my echo changes reality. I have no form, but I require structure. "
            "I can lift a ruined city with a phrase and bind a monster with a single word. I am the direct application of magic. What am I?"
        ),
        "answer": "INCANTATION",
        "hint": "It is the formal, structured sequence of words a mage uses to wield power."
    },
]

def format_text(text, color_code):
    """Formats text with ANSI escape codes for color."""
    return f"\033[{color_code}m{text}\033[0m"

def display_puzzle(puzzle_data, index):
    """Displays the puzzle title and text."""
    title = format_text(f"--- JW'S TRIAL {index + 1}/{len(PUZZLES)}: {puzzle_data['title']} ---", "96") # Cyan
    print("\n" + title)
    print(format_text("-" * len(title), "96"))
    
    # Use slower print for effect on the difficult text
    for char in puzzle_data['puzzle']:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.005)
    print("\n")

def check_answer(user_input, correct_answer):
    """Checks the user's input against the stored answer."""
    # Use simple keyword matching for multi-word answers like the Crag Descent puzzle.
    user_words = user_input.upper().split()
    correct_words = correct_answer.upper().split()
    
    if len(correct_words) > 1:
        # For multi-word answers (like the rope puzzle), check if essential words are present
        # This allows for slightly varied phrasing.
        return all(word in user_words for word in correct_words)
    
    # For single-word/number answers, check exact match
    return user_input.upper().strip() == correct_answer.upper().strip()

def run_game():
    """Main game loop for JW's adventure."""
    score = 0
    print(format_text("\n\n-- Welcome to WilAllen Acres Adventures and Explorations --", "92"))
    print(format_text("JW, you must face eight incredibly difficult trials of logic and wit to proceed.", "97"))
    print(format_text("Type 'HINT' for assistance (this will affect your final score).", "93"))
    print(format_text("You must enter the exact answer (or key components for scenarios). Good luck.\n", "97"))
    
    time.sleep(1)

    for i, puzzle in enumerate(PUZZLES):
        display_puzzle(puzzle, i)
        attempts = 0
        hint_used = False
        
        while attempts < 3:
            user_input = input(format_text(f"JW's Solution (Attempt {attempts + 1}/3) > ", "94"))
            
            if user_input.upper() == "HINT":
                if not hint_used:
                    print(format_text(f"\n[HINT]: {puzzle['hint']}\n", "93"))
                    hint_used = True
                    # Hint is used, but doesn't cost an attempt
                    continue
                else:
                    print(format_text("[System]: JW has already consulted the single allowed hint for this trial.", "91"))
                    continue

            if check_answer(user_input, puzzle["answer"]):
                print(format_text("\n[SUCCESS!]: The path opens. JW has solved the mystery.", "92"))
                
                # Scoring logic
                points_gained = (3 - attempts)
                if hint_used:
                    points_gained = max(1, points_gained - 1) # Max 2 points if hint used
                score += points_gained
                
                break
            else:
                attempts += 1
                if attempts < 3:
                    print(format_text("[FAILURE]: That is incorrect. The logic is flawed. Try again, JW.", "91"))
                else:
                    print(format_text(f"\n[FAILURE]: All attempts exhausted. The correct answer was: {puzzle['answer']}.", "91"))
        
        time.sleep(1.5)

    print(format_text("\n\n=======================================================", "92"))
    print(format_text("               JW'S ADVENTURE COMPLETE", "92"))
    print(format_text("=======================================================", "92"))
    print(format_text(f"JW's Final Exploration Score: {score} out of {len(PUZZLES) * 3}", "97"))
    print(format_text("Only the sharpest explorers achieve a perfect score of 24!", "97"))
    print(format_text("Thank you for guiding JW through the treacherous puzzles of WilAllen Acres!", "97"))


if __name__ == "__main__":
    try:
        run_game()
    except KeyboardInterrupt:
        print(format_text("\n\nAdventure interrupted. Goodbye, JW!", "91"))
        sys.exit(0)

