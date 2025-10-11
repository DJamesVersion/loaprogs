# laondsofages_jhg.py
import time

def pause():
    time.sleep(1.5)

def intro():
    print("🌌 Welcome to Laonds of Ages: JHG 🌌")
    print("In the ancient caverns of Stihuu, beneath the land of Vraelvrae,")
    print("the royal family of Tahkmahnelle faces trials that will shape their destiny.")
    print("You will guide Jocelyn, Henrietta, Gabriella, and their father JPW7 through 8 epic adventures.\n")
    pause()

def chapter(title, description, choices):
    print(f"\n📜 {title} 📜")
    print(description)
    for i, choice in enumerate(choices, 1):
        print(f"{i}. {choice['text']}")
    while True:
        try:
            selection = int(input("Choose an option: "))
            if 1 <= selection <= len(choices):
                print(choices[selection - 1]['outcome'])
                pause()
                break
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a number.")

def main():
    intro()

    chapter("Chapter 1: The Whispering Walls",
        "Jocelyn hears voices echoing from the obsidian walls of the royal chamber. They speak of a forgotten gate.",
        [
            {"text": "Investigate the whispers alone", "outcome": "Jocelyn uncovers a hidden glyph glowing with ancient power."},
            {"text": "Tell her sisters", "outcome": "Together, they decipher the glyph and awaken a dormant guardian."}
        ])

    chapter("Chapter 2: The Ember Trial",
        "Henrietta must pass the Trial of Embers to prove her right to wield the Flame Scepter.",
        [
            {"text": "Face the trial with courage", "outcome": "Henrietta walks through fire unscathed, earning the scepter's trust."},
            {"text": "Ask JPW7 for help", "outcome": "JPW7 reveals a secret chant that calms the flames."}
        ])

    chapter("Chapter 3: Gabriella's Vision",
        "Gabriella dreams of a silver serpent coiled around the throne. Is it prophecy or warning?",
        [
            {"text": "Seek the Oracle of Ash", "outcome": "The Oracle warns of betrayal from within."},
            {"text": "Ignore the dream", "outcome": "The serpent appears in waking life, slithering through the court."}
        ])

    chapter("Chapter 4: The Hollow Feast",
        "A banquet is held for the visiting dwarves of Kurn, but something in the food is cursed.",
        [
            {"text": "Taste the food first", "outcome": "JPW7 falls ill, but saves the guests."},
            {"text": "Let the dwarves eat first", "outcome": "The dwarves fall into a trance, whispering secrets of the deep."}
        ])

    chapter("Chapter 5: The Mirror of Vraelvrae",
        "A mirror shows each royal their darkest fear. Only one may look at a time.",
        [
            {"text": "Jocelyn looks", "outcome": "She sees herself ruling alone, her sisters gone."},
            {"text": "Gabriella looks", "outcome": "She sees the throne shattered, her father turned to stone."}
        ])

    chapter("Chapter 6: The Siege of Shadows",
        "Darklings rise from the lower caverns, threatening the kingdom.",
        [
            {"text": "Lead the army into battle", "outcome": "Henrietta's fire scorches the enemy, but the cost is high."},
            {"text": "Seal the cavern gates", "outcome": "The kingdom is safe, but the shadows whisper vengeance."}
        ])

    chapter("Chapter 7: The Pact of Stihuu",
        "A mysterious envoy offers peace in exchange for a royal sacrifice.",
        [
            {"text": "Accept the pact", "outcome": "JPW7 offers himself, vanishing into the mist."},
            {"text": "Refuse the pact", "outcome": "The envoy vanishes, but the caverns tremble with fury."}
        ])

    chapter("Chapter 8: The Crown of Echoes",
        "The sisters must choose a new ruler. The crown calls to each of them.",
        [
            {"text": "Jocelyn takes the crown", "outcome": "She becomes Queen, but the echoes of the past haunt her."},
            {"text": "They rule together", "outcome": "A new era begins—three voices, one throne, united in purpose."}
        ])

    print("\n🏰 The saga of Tahkmahnelle continues... Thank you for playing Laonds of Ages: JHG!")

if __name__ == "__main__":
    main()
