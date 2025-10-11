# laondsofages_jhg_throne_of_the_deep.py
import time

def pause():
    time.sleep(1.5)

def intro():
    print("👑 Laonds of Ages: JHG — Throne of the Deep 👑")
    print("Years have passed since the Echo was bound. But the Deep Realm stirs once more.")
    print("Jocelyn watches from the shadows. Henrietta and Gabriella rule. The Deep Crown awakens.\n")
    pause()

def chapter(title, description, choices):
    print(f"\n📘 {title} 📘")
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

    chapter("Chapter 1: The Crown Calls",
        "A pulse echoes through the throne room. The Deep Crown stirs beneath the stone.",
        [
            {"text": "Henrietta touches the crown", "outcome": "She sees visions of ancient kings and hears their demands."},
            {"text": "Gabriella seals the chamber", "outcome": "The crown’s whispers grow louder, seeping into dreams."}
        ])

    chapter("Chapter 2: Jocelyn’s Return",
        "Jocelyn emerges from the Deep Realm, changed and powerful.",
        [
            {"text": "Welcome her back", "outcome": "The sisters reunite, but Jocelyn’s eyes glow with Echo-fire."},
            {"text": "Challenge her authority", "outcome": "Jocelyn warns of a deeper threat rising beneath Vraelvrae."}
        ])

    chapter("Chapter 3: The Deep Kings",
        "Ghostly monarchs rise from the abyss, demanding tribute.",
        [
            {"text": "Offer the Flame Scepter", "outcome": "The kings accept, but Henrietta loses her fire."},
            {"text": "Refuse the tribute", "outcome": "The kings curse the land with eternal twilight."}
        ])

    chapter("Chapter 4: Gabriella’s Descent",
        "Gabriella descends alone to the Deep Crown’s chamber.",
        [
            {"text": "Claim the crown", "outcome": "She becomes Queen of Shadows, ruling both realms."},
            {"text": "Destroy the crown", "outcome": "The chamber collapses, sealing the Deep Realm forever."}
        ])

    chapter("Chapter 5: The Rift",
        "A rift opens between Tahkmahnelle and the Deep Realm. Creatures spill forth.",
        [
            {"text": "Unite the kingdoms", "outcome": "Jocelyn leads a pact of peace, binding both realms."},
            {"text": "Wage war", "outcome": "Henrietta’s army fights bravely, but the cost is immense."}
        ])

    chapter("Chapter 6: The Final Trial",
        "The sisters must face the Deep Crown together. Only one may wear it.",
        [
            {"text": "Jocelyn takes the crown", "outcome": "She becomes the Eternal Queen, watching over both worlds."},
            {"text": "They destroy it together", "outcome": "The Deep Realm fades, and peace returns to Vraelvrae."}
        ])

    chapter("Chapter 7: Legacy",
        "The throne is rebuilt. Songs are sung of the sisters’ courage.",
        [
            {"text": "Write the history", "outcome": "Their tale becomes legend, passed down through generations."},
            {"text": "Let it fade", "outcome": "The story is forgotten, but the peace endures."}
        ])

    chapter("Chapter 8: The Last Echo",
        "A final whisper reaches Jocelyn. The Echo is not gone—it waits.",
        [
            {"text": "Seek the Echo again", "outcome": "Jocelyn vanishes into the mist, chasing the last whisper."},
            {"text": "Seal the throne forever", "outcome": "The throne is locked, and the Echo sleeps once more."}
        ])

    print("\n🌌 The trilogy ends. But echoes never truly fade. Thank you for playing Laonds of Ages: JHG — Throne of the Deep!")

if __name__ == "__main__":
    main()
