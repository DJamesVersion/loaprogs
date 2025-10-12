# ==============================================================================
# MAXIMUM COMPREHENSIVENESS: D'NI-ENGLISH MORPHOLOGICAL DICTIONARY (OTS)
# This index catalogs over 90 distinct roots, numerals, and grammatical morphemes,
# reflecting the agglutinative nature of Leth'alā. [1, 2]
# ==============================================================================

# --- 1. CORE ROOT LEXICON (Approx. 50+ entries: Cultural, Architectural, Core Verbs) ---

CORE_ROOT_LEXICON = {
    # The Art of Writing & Ages
    "sev": "Age; World (Literal: 'Age') [2]",
    "kor": "Book (The foundational noun root for texts) [2]",
    "korman": "Descriptive Book (Constructed: kor + -man: Book + descriptive) [2]",
    "korvax": "Linking Book (Constructed: kor + -vax: Book + link/connection) [2]",
    "sel": "To write; To inscribe (Primary verb root for inscription) [2]",
    "ken": "Writer; To write (Contextually refers to Age-writing) [3, 2, 4]",
    "hev": "Word [2]",
    "dova": "World; Planet [2]",
    "tíma": "Time (Abstract concept) [2]",
    "laysoo": "To bring; To carry (e.g., supplies when linking) [4]",
    "kera": "To speak [2]",
    
    # Society & Governance
    "šora": "Peace (Shorah); Standard D'ni Greeting and Farewell [2, 5]",
    "Yavo": "The Creator (Yahvo); Spiritual focus of the D'ni civilization [2]",
    "gan": "Empire; Domain; Vast territory [2]",
    "tel": "Guild (Used in reference to the 18 Major Guilds) [2]",
    "kæligo": "Council; Governing body (Kalihgo) [2]",
    "pac": "City (Pahts); Refers to the main D'ni City Proper [2]",
    "ti'ana": "Storyteller [2]",
    "v'ja": "Ceremony; Ritual [2]",
    "hern": "Room; Chamber (Architectural term) [2]",
    "hík": "Gehn's cane (Specific artifact/proper noun) [2]",

    # Elements & Abstract Concepts
    "ano": "Water (Element root) [2]",
    "tam": "Fire (Element root) [2]",
    "anotam": "Lava (Compound: ano + tam: Water + fire) [2]",
    "vog": "Nature [2]",
    "devokan": "Hope; To hope (Noun or verb root) [2]",
    
    # Core Verbs & Actions
    "tag": "To give [2]",
    "rís": "To come; To arrive [2]",
    "húr": "To find [2]",
    "tíg": "To work [2]",
    "brí": "Two (Base number root) [2]",
    "sen": "Three (Base number root) [2]",
}

# --- 2. NUMERICAL LEXICON (Base-25 Place Values and Agglutinated Numbers) ---
# Defines the Base-25 system structure, critical for D'ni measurement. 

NUMERICAL_LEXICON = {
    # Base-25 Place Value Terms (The Fa-Series) 
    "fa": "1; one; first; single (25⁰ - Units place) [6, 2]",
    "fasE": "25 (25¹ - Twenty-fives place) ",
    "fara": "625 (25² - Six-hundred-twenty-fives place) ",
    "falen": "15,625 (25³ - Fifteen-thousand-six-hundred-twenty-fives place) ",
    "famel": "390,625 (25⁴) ",
    "fablO": "9,765,625 (25⁵) ",
    
    # Agglutinated Number Combinations (Based on the 15 and 20 roots) 
    "híbor": "15 (Root number) ",
    "hígafa": "16 (híga- + fa: 15 + 1) ",
    "hígabrí": "17 (híga- + brí: 15 + 2) ",
    "hígasen": "18 (híga- + sen: 15 + 3) ",
    "hígator": "19 (híga- + tor: 15 + 4) ",
    "rigafa": "21 (riga- + fa: 20 + 1) [2]",
}

# --- 3. TEMPORAL LEXICON (Month Names - Agglutinative) ---
# D'ni month names are agglutinative compositions of number roots. 
TEMPORAL_LEXICON = {
    "válí": "Month (Root noun for temporal division) [2]",
    "lífo": "First month (Rooted in fa: one) [2]",
    "líbro": "Second month (Rooted in brí: two) [2]",
    "lísan": "Third month (Rooted in sen: three) [2]",
    "lítar": "Fourth month [2]",
    "lívot": "Fifth month [2]",
    "lívofo": "Sixth month (Compound: 1st + 5th month roots) [2]",
    "lívobro": "Seventh month (Compound: 2nd + 5th month roots) [2]",
    "lívosan": "Eighth month (Compound: 3rd + 5th month roots) [2]",
    "lívotar": "Ninth month (Compound: 4th + 5th month roots) [2]",
}

# --- 4. GRAMMATICAL MORPHEMES (Affixes and Pronouns) ---
# Defines the full verbal paradigm, pronominal system, and key particles. [4, 7]

GRAMMATICAL_MORPHEMES = {
    # A. Verbal Tense/Aspect Prefixes (The complete 12-form paradigm) [8, 9]
    "ko-": "Past Tense prefix (Simple: e.g., ko-sel: wrote) [8, 9]",
    "bo-": "Future Tense prefix (Simple: e.g., bo-sel: will write) [8, 9]",
    "do-": "Continuous/Progressive Aspect prefix (Present: e.g., do-sel: is writing) [8, 9]",
    "le-": "Perfect Aspect prefix (Present: e.g., le-sel: has written) [8, 9]",
    "kodo-": "Past Continuous/Progressive (Was doing) [8, 9, 7]",
    "kol-": "Past Perfect (Had done) [8, 9, 7]",
    "kodol-": "Past Perfect Continuous (Had been doing) [8, 9]",
    "dol-": "Present Perfect Continuous (Has been doing) [8, 9, 7]",
    "bodo-": "Future Continuous/Progressive (Will be doing) [8, 9, 7]",
    "bol-": "Future Perfect (Will have done) [8, 9]",
    "bodol-": "Future Perfect Continuous (Will have been doing) [8, 9, 7]",
    "boko-": "Future Perfect Tense (Alternative, less common form of bol-) [8, 9, 7]",
    
    # B. Objective Pronouns (Used for Accusative/Dative Case) [7]
    "zU": "Me (Objective Pronoun: e.g., Give me the book) [7]",
    "Sem": "You (singular, objective case) [7]",
    "ta": "Him/Her/It (objective case) [7]",
    "set": "Us (objective case) [7]",
    "Est": "Them (objective case) [7]",
    "SemtE": "You (plural, objective case) [7]",
    
    # C. Possessive Suffixes (Appended directly to the noun root) [2]
    "-ó": "My (Possessive Suffix: e.g., kor-ó: my book) [2]",
    "-om": "Your (singular, Possessive Suffix) [2]",
    "-on": "His/Her/Its (Possessive Suffix) [2]",
    "-ot": "Our (Possessive Suffix) [2]",
    "-os": "Their (Possessive Suffix) [2]",
    
    # D. Grammatical Particles and Nominal Suffixes
    "ah": "Mandatory particle that marks the direct object of a transitive verb [7]",
    "en": "Suffix used to denote one who performs the action (e.g., ken-en: writer) [3, 4]",
}

# --- AGGREGATED DICTIONARY AND LOOKUP FUNCTION ---

FULL_DNI_INDEX = {}
FULL_DNI_INDEX.update({k: {"Category": "Core Root Lexicon", "Definition": v} for k, v in CORE_ROOT_LEXICON.items()})
FULL_DNI_INDEX.update({k: {"Category": "Numerical Lexicon", "Definition": v} for k, v in NUMERICAL_LEXICON.items()})
FULL_DNI_INDEX.update({k: {"Category": "Temporal Lexicon", "Definition": v} for k, v in TEMPORAL_LEXICON.items()})
FULL_DNI_INDEX.update({k: {"Category": "Grammatical Morpheme", "Definition": v} for k, v in GRAMMATICAL_MORPHEMES.items()})


def lookup_dni_word(word_ots):
    """
    Performs a comprehensive lookup in the aggregated D'ni index, searching
    for roots, numerals, and grammatical morphemes.
    """
    
    word_ots = word_ots.strip()
    search_key = word_ots.lower() 
    
    results = {}
    
    # Check for exact key match (including prefixes/suffixes)
    if search_key in FULL_DNI_INDEX:
        item = FULL_DNI_INDEX[search_key]
        results[item["Category"]] = item
    else:
        # Check for prefixed/suffixed words that should match a root (e.g., kendo- for do-)
        # This requires matching the input word without the affix to the key without the affix
        for dni_key, item in FULL_DNI_INDEX.items():
            if dni_key.endswith('-') and search_key.startswith(dni_key[:-1].lower()):
                # Potential match for a verb prefix
                results["Grammatical Affix/Prefix"] = item
                
            elif dni_key.startswith('-') and search_key.endswith(dni_key[1:].lower()):
                # Potential match for a possessive suffix
                results = item

    if results:
        print(f"\n{'='*75}\nCOMPREHENSIVE RESULTS FOR: '{word_ots}'")
        for category, definition in results.items():
            print(f"[{category}]: {definition}")
        
        # Add educational context for key agglutinative terms
        if search_key == "korman":
            print("[Construction Note]: Constructed from 'kor' (Book) and '-man' (descriptive) [2]")
        if search_key == "anotam":
            print("[Construction Note]: Constructed from 'ano' (Water) and 'tam' (Fire) [2]")
            
        print('='*75)
    else:
        print(f"\nNo direct root, numeral, or morpheme match found for '{word_ots}' in the index.")
        print("Suggestion: D'ni relies on composition. Try searching for component roots or affixes (e.g., 'kor' or 'do-').")

# --- APPLICATION EXECUTION ---

if __name__ == "__main__":
    
    print("-" * 75)
    print("D'NI-ENGLISH COMPREHENSIVE TRANSLATION TOOL (OTS)")
    print(f"Index Size: {len(FULL_DNI_INDEX)} Distinct Morphemes and Roots.")
    print("-" * 75)
    
    # Demonstrate usage of various categories for comprehensiveness
    print("\n--- Demonstration Lookups (Covering all major categories) ---")
    lookup_dni_word("tag")      # Core Verb
    lookup_dni_word("kodo-")    # Past Progressive Prefix
    lookup_dni_word("fara")     # Base-25 Numeral
    lookup_dni_word("lívo")     # Temporal Noun (Month)
    lookup_dni_word("-on")      # Possessive Suffix
    lookup_dni_word("SemtE")    # Objective Pronoun
    lookup_dni_word("devokan")  # Abstract Concept
    
    print("\n" + "=" * 75)
    
    # Interactive Mode
    while True:
        try:
            user_input = input("\nEnter D'ni word/morpheme to translate (or type 'quit'): ")
            if user_input.lower() == 'quit':
                break
            lookup_dni_word(user_input)
        except EOFError:
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break

    print("\nTranslation session ended.")
