# laondsofages_jhg_echoes.py
import time

def pause():
    time.sleep(1.5)

def intro():
    print("👑 Laonds of Ages: JHG — Echoes of the Throne 👑")
    print("The sisters rule Tahkmahnelle, but the Echo stirs beneath the throne.")
    print("Dark truths, ancient allies, and forbidden paths await in the depths of Vraelvrae.\n")
    pause()

def chapter(title, description, choices):
    print(f"\n📖 {title} 📖")
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

    chapter("Chapter 1: The Echo Returns",
        "A voice from the throne room speaks in riddles. Jocelyn suspects it is the Echo, a forgotten entity.",
        [
            {"text": "Confront the Echo alone", "outcome": "Jocelyn is marked by the Echo, gaining insight into the Deep Realm."},
            {"text": "Call a council", "outcome": "The sisters learn the Echo was once a guardian of the throne."}
        ])

    chapter("Chapter 2: The Forgotten Vault",
        "Henrietta discovers a sealed vault beneath the Flame Temple. Its lock responds to bloodline magic.",
        [
            {"text": "Open the vault", "outcome": "Inside lies a map to the Deep Realm and a cursed crown."},
            {"text": "Leave it sealed", "outcome": "The vault hums with energy, whispering Henrietta’s name."}
        ])

    chapter("Chapter 3: Gabriella’s Bargain",
        "Gabriella meets a shadowy figure who offers her a pact: power in exchange for memory.",
        [
            {"text": "Accept the pact", "outcome": "Gabriella gains the Sight, but forgets her childhood."},
            {"text": "Refuse the pact", "outcome": "The figure vanishes, leaving behind a silver tear."}
        ])

    chapter("Chapter 4: The Deep Realm Beckons",
        "The sisters must descend into the Deep Realm to uncover the Echo’s origin.",
        [
            {"text": "Descend together", "outcome": "They face illusions, but their bond keeps them grounded."},
            {"text": "Send Jocelyn alone", "outcome": "Jocelyn finds the Echo’s heart, but is changed forever."}
        ])

    chapter("Chapter 5: The Trial of Echoes",
        "JPW7’s spirit appears, warning of a trial that tests loyalty, sacrifice, and truth.",
        [
            {"text": "Take the trial", "outcome": "The sisters relive their darkest choices and emerge wiser."},
            {"text": "Reject the trial", "outcome": "The Echo grows stronger, feeding on unresolved guilt."}
        ])

    chapter("Chapter 6: The Shattered Throne",
        "The throne cracks, revealing a hidden chamber with ancient runes.",
        [
            {"text": "Translate the runes", "outcome": "They reveal a prophecy: 'Three shall rule, one shall fall.'"},
            {"text": "Destroy the chamber", "outcome": "The prophecy is lost, but the Echo screams in fury."}
        ])

    chapter("Chapter 7: The Final Choice",
        "The Echo demands a sacrifice to restore balance. One sister must vanish into the Deep Realm.",
        [
            {"text": "Jocelyn volunteers", "outcome": "She becomes the new guardian, watching from the shadows."},
            {"text": "Refuse the sacrifice", "outcome": "The Echo consumes the throne, plunging Tahkmahnelle into chaos."}
        ])

    chapter("Chapter 8: The New Dawn",
        "Tahkmahnelle awakens to a new era. The throne is rebuilt, but echoes linger.",
        [
            {"text": "Rule with wisdom", "outcome": "The sisters forge a legacy of unity and resilience."},
            {"text": "Seek the Echo again", "outcome": "They descend once more, chasing whispers of forgotten power."}
        ])

    print("\n🌠 The saga continues... Echoes never truly fade. Thank you for playing Laonds of Ages: JHG — Echoes of the Throne!")

if __name__ == "__main__":
    main()
