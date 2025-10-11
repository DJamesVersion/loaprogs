import time
import random

def slow_print(text, delay=0.05):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

class Game:
    def __init__(self):
        self.character = "jpw7"
        self.treasures_found = []
        self.locations = ["Whispering Ridge", "Echo Peak", "Frostfang Summit"]
        self.treasures = {
            "Whispering Ridge": "Crystal Feather",
            "Echo Peak": "Golden Compass",
            "Frostfang Summit": "Ancient Rune"
        }

    def intro(self):
        slow_print(f"Welcome to Loa Tree, adventurer {self.character}!")
        slow_print("Your journey begins at the base of the towering mountains...")
        slow_print("Legends speak of a tree called Tetnobautte, hidden beyond the peaks.")

    def climb_mountain(self, location):
        slow_print(f"\nClimbing {location}...")
        time.sleep(1)
        event = random.choice(["storm", "clear skies", "rockslide", "eagle sighting"])
        slow_print(f"You encounter: {event}")
        if event == "rockslide":
            slow_print("You narrowly escape! But lose some supplies.")
        elif event == "storm":
            slow_print("You find shelter and wait it out.")
        else:
            slow_print("The path is challenging but beautiful.")

    def find_treasure(self, location):
        treasure = self.treasures.get(location)
        if treasure:
            slow_print(f"You discover a hidden treasure: {treasure}!")
            self.treasures_found.append(treasure)

    def reach_tetnobautte(self):
        slow_print("\nAfter conquering the final summit, a glowing path reveals itself...")
        slow_print("You follow it to a secluded grove where the Tetnobautte tree stands.")
        slow_print("Its bark shimmers with ancient light, and its leaves whisper secrets.")
        slow_print("You place your treasures at its roots, and the tree awakens...")
        slow_print("A voice echoes: 'jpw7, you have proven worthy. Loa Tree lives through you.'")
        slow_print("🌳 The End 🌳")

    def play(self):
        self.intro()
        for location in self.locations:
            self.climb_mountain(location)
            self.find_treasure(location)
        self.reach_tetnobautte()

if __name__ == "__main__":
    game = Game()
    game.play()
