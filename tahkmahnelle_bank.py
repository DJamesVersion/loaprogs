# -*- coding: utf-8 -*-
"""
This application models the fictional money system of Tahkmah'nelle
from the world of Lands of Ages. It handles conversions between
standard denominations, Royal Gems, and the credit-based stock system.
"""

class TahkmahnelleMoneySystem:
    """
    A class to manage the currency conversions for the Tahkmah'nelle money system.
    """

    def __init__(self):
        """
        Initializes the money system with all known conversion rates to the base
        unit, the 'kajoi'.
        """
        # Standard denominations, with values in kajoi
        self.denominations = {
            'kajoi': 1,
            'narres': 5,
            'illias': 10,
            'goikes': 50,
            'xias': 75,
            'zazois': 100
        }

        # Royal Gems. Values are assumed as they were not specified in the lore.
        # These can be adjusted as needed.
        self.royal_gems = {
            'royks': 250,
            'tetnos': 500,
            'ketobons': 1000
        }

        # Combine all physical currencies into one dictionary for easier lookup
        self.all_currencies = {**self.denominations, **self.royal_gems}

        # Stocks are in credit. The conversion is based on the rule that
        # 31% of a unit of credit is worth 5 kajoi.
        # So, 0.31 * 1 credit = 5 kajoi
        # 1 credit = 5 / 0.31 kajoi
        self.credit_to_kajoi_rate = 5 / 0.31

    def get_all_units(self):
        """Returns a list of all currency and credit units."""
        return list(self.all_currencies.keys()) + ['credit']

    def convert_to_kajoi(self, amount, unit):
        """
        Converts a given amount of a specific unit into its kajoi equivalent.

        Args:
            amount (float): The amount of the currency unit.
            unit (str): The name of the currency unit (e.g., 'goikes', 'credit').

        Returns:
            float: The equivalent value in kajoi, or None if the unit is invalid.
        """
        unit = unit.lower()
        if unit in self.all_currencies:
            return amount * self.all_currencies[unit]
        elif unit == 'credit':
            return amount * self.credit_to_kajoi_rate
        else:
            return None

    def convert_from_kajoi(self, kajoi_amount, target_unit):
        """
        Converts a given amount of kajoi into another currency unit.

        Args:
            kajoi_amount (float): The amount in kajoi.
            target_unit (str): The name of the target unit.

        Returns:
            float: The equivalent value in the target unit, or None if invalid.
        """
        target_unit = target_unit.lower()
        if target_unit in self.all_currencies:
            return kajoi_amount / self.all_currencies[target_unit]
        elif target_unit == 'credit':
            return kajoi_amount / self.credit_to_kajoi_rate
        else:
            return None

    def breakdown_kajoi(self, kajoi_amount):
        """
        Breaks down a total kajoi amount into the most efficient combination of
        physical currency denominations (largest units first).

        Args:
            kajoi_amount (float): The total amount in kajoi.

        Returns:
            dict: A dictionary with the amounts of each currency unit.
        """
        # Sort currencies by value in descending order for proper breakdown
        sorted_currencies = sorted(
            self.all_currencies.items(),
            key=lambda item: item[1],
            reverse=True
        )

        remaining_kajoi = kajoi_amount
        breakdown = {}

        for unit, value in sorted_currencies:
            if remaining_kajoi >= value:
                count = int(remaining_kajoi // value)
                breakdown[unit] = count
                remaining_kajoi %= value

        # The final remainder is in kajoi, but since 'kajoi' has a value of 1,
        # it might have been calculated already. We ensure the remainder is captured.
        if remaining_kajoi > 0:
            # We add the remainder to the 'kajoi' count if it exists,
            # otherwise we set it.
            breakdown['kajoi'] = breakdown.get('kajoi', 0) + remaining_kajoi
            # Since this might result in a float, we round to a sensible precision
            breakdown['kajoi'] = round(breakdown['kajoi'], 2)


        return breakdown

def display_menu():
    """Prints the main menu for the user."""
    print("\n" + "="*40)
    print("  Tahkmah'nelle Currency Converter")
    print("="*40)
    print("1. Convert from one currency to another")
    print("2. Breakdown a kajoi value into denominations")
    print("3. View currency exchange rates")
    print("4. Exit")
    print("="*40)

def display_exchange_rates(system):
    """Prints a table of all exchange rates relative to kajoi."""
    print("\n--- Exchange Rates (relative to 1 kajoi) ---")
    print(f"{'Unit':<15} {'Value in Kajoi':<20}")
    print("-"*40)
    # Sort all currencies by their value for a structured view
    sorted_currencies = sorted(
        system.all_currencies.items(),
        key=lambda item: item[1]
    )
    for unit, value in sorted_currencies:
        print(f"{unit.capitalize():<15} {value:<20.2f}")

    print("\n--- Stock System ---")
    print(f"{'Credit':<15} {system.credit_to_kajoi_rate:<20.2f}")
    print("-"*40)

def get_valid_amount():
    """Prompts the user for a valid numerical amount and handles errors."""
    while True:
        try:
            amount_str = input("Enter the amount: ")
            return float(amount_str)
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_valid_unit(system):
    """Prompts the user for a valid currency unit and handles errors."""
    valid_units = system.get_all_units()
    while True:
        unit = input(f"Enter the unit {valid_units}: ").lower()
        if unit in valid_units:
            return unit
        else:
            print("Invalid unit. Please choose from the list.")


def main():
    """The main function to run the command-line interface."""
    system = TahkmahnelleMoneySystem()

    while True:
        display_menu()
        choice = input("Choose an option (1-4): ")

        if choice == '1':
            # --- Conversion ---
            print("\n--- Convert Currency ---")
            print("Enter the source currency:")
            source_amount = get_valid_amount()
            source_unit = get_valid_unit(system)

            print("\nEnter the target currency:")
            target_unit = get_valid_unit(system)

            # First, convert source to the base unit (kajoi)
            kajoi_equivalent = system.convert_to_kajoi(source_amount, source_unit)

            if kajoi_equivalent is not None:
                # Then, convert from kajoi to the target unit
                final_amount = system.convert_from_kajoi(kajoi_equivalent, target_unit)
                if final_amount is not None:
                    print("\n--- Result ---")
                    print(f"{source_amount:.2f} {source_unit} is equal to {final_amount:.2f} {target_unit}")
                else:
                    print("Error during conversion.")
            else:
                print("Error during conversion.")

        elif choice == '2':
            # --- Breakdown ---
            print("\n--- Breakdown Kajoi Value ---")
            kajoi_total = get_valid_amount()
            result = system.breakdown_kajoi(kajoi_total)
            print("\n--- Result ---")
            print(f"The breakdown of {kajoi_total:.2f} kajoi is:")
            if not result:
                print("No denominations for this amount.")
            else:
                for unit, count in result.items():
                    print(f"- {count} {unit.capitalize()}")

        elif choice == '3':
            # --- View Rates ---
            display_exchange_rates(system)

        elif choice == '4':
            # --- Exit ---
            print("Exiting the Tahkmah'nelle Currency Converter. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 4.")


if __name__ == "__main__":
    main()

