import pprint

# Pretty printer instance for readable output
pp = pprint.PrettyPrinter(indent=4)

# --- I. COMMAND AND CONTROL HIERARCHY ---
COMMAND_HIERARCHY = [
    {
        "Level": "Highest Authority",
        "Title": "The Sovereign's Grand Edict",
        "Function": "Ultimate command; strategic doctrine and declaration of war."
    },
    {
        "Level": "Operational Command",
        "Title": "Royal High Council of War",
        "Function": "Joint Chiefs of Staff; resource allocation and inter-service coordination (Quaternary Synchronization)."
    },
    {
        "Level": "Ground Operations",
        "Title": "Marshal of the Phalanx",
        "Function": "Commander of the Royal Ground Phalanx (RGP)."
    },
    {
        "Level": "Void Operations",
        "Title": "Grand Admiral of Star Command",
        "Function": "Commander of all space-faring assets (RSC)."
    }
]

# --- II. UNIFIED RANKS STRUCTURE (The Quaternary Hierarchy) ---
UNIFIED_RANKS = {
    "COMMAND_TIER": {
        "Marshal/Admiral": {
            "RGP": "Grand Marshal of the Phalanx",
            "RSC": "Grand Admiral of Star Command",
            "ROF": "Grand Admiral of the Flotilla",
            "RAD": "High Marshal of the Aerium"
        },
        "General/Admiral": {
            "RGP": "Marshal-General",
            "RSC": "Star Admiral",
            "ROF": "Sector Admiral",
            "RAD": "Air General"
        }
    },
    "OFFICER_TIER": {
        "Field Grade": {
            "RGP": "Phalanx Colonel (PC)",
            "RSC": "Command Captain (CC)",
            "ROF": "Flotilla Captain (FC)",
            "RAD": "Aerium Wing Commander (AWC)"
        },
        "Company Grade": {
            "RGP": "Phalanx Captain (PA)",
            "RSC": "Star Lieutenant (SL)",
            "ROF": "Flotilla Lieutenant (FL)",
            "RAD": "Aerium Flight Leader (AFL)"
        }
    },
    "SUPPORT_TIER": {
        "Sub-Commissioned": {
            "RGP": "Chief Warrant Officer",
            "RSC": "Void Engineer Specialist",
            "ROF": "Master Hydro-Pilot",
            "RAD": "Tactical Sensor Chief"
        },
        "Enlisted Senior": {
            "RGP": "Master Sergeant",
            "RSC": "Stellar Chief",
            "ROF": "Flotilla Master",
            "RAD": "Aerium Sergeant Major"
        },
        "Enlisted Junior": {
            "RGP": "Trooper",
            "RSC": "Crewman Second Class",
            "ROF": "Mariner",
            "RAD": "Airman"
        }
    }
}

# --- III. WEAPONS SYSTEMS AND ARMAMENTS ---
WEAPONS_SYSTEMS = {
    "RGP_ARMY": [
        {"Name": "TFP-8 'Inertia' Rifle", "Type": "Standard Energy Rifle", "Role": "Standard infantry issue utilizing Tachyon-Field Pulse (TFP) technology."},
        {"Name": "Magneto-Rail Cannon", "Type": "Heavy Anti-Armor", "Role": "Vehicle-mounted kinetic projectile system."},
        {"Name": "Phalanx Exosuits", "Type": "Powered Armor", "Role": "Provides enhanced strength and resilience in zero-G to high-G deployments."}
    ],
    "RSC_SPACE_FORCES": [
        {"Name": "Void Hammer Lance", "Type": "Capital Ship Weaponry", "Role": "High-yield, sustained energy beam for fleet combat."},
        {"Name": "Gravitic Torpedoes", "Type": "Ship-to-Ship Missile", "Role": "Bypasses conventional shielding using manipulated gravity fields."},
        {"Name": "Sentinel Drones", "Type": "Autonomous Fighters", "Role": "Un-manned swarm fighters for fleet defense and interception."}
    ],
    "ROF_NAVY": [
        {"Name": "Hydro-Pulse Cannon", "Type": "Standard Submersible Weapon", "Role": "Sonic/kinetic pulse optimized for dense water environments."},
        {"Name": "Deep-Vibe Sensor Nets", "Type": "Detection & Surveillance", "Role": "Passive listening systems for subterranean and deep-ocean threats."},
        {"Name": "Thermal Harpoons", "Type": "Anti-Submersible Weapon", "Role": "Penetrative weapons to breach reinforced submersible hulls."}
    ],
    "RAD_AIR_FORCE": [
        {"Name": "Skyspear Autocannons", "Type": "Fighter Weaponry", "Role": "High-rate-of-fire kinetic/energy hybrid for atmospheric superiority."},
        {"Name": "Atmospheric Inhibitor", "Type": "Electronic Warfare", "Role": "Disrupts enemy targeting and creates localized turbulence."},
        {"Name": "Dropship Shielding", "Type": "Defensive System", "Role": "Reinforced plasma shielding for RGP deployment vehicles."}
    ]
}

# --- IV. ROYAL STAR COMMAND (RSC) FLEET DESIGNATIONS ---
RSC_FLEET_DESIGNATIONS = [
    {"Name": "The Illianarre (First Fleet)", "Role": "Carrier Command & Deep Strike", "Strategy": "Rapid, overwhelming force projection against major system threats."},
    {"Name": "The Vraelvrae (Second Fleet)", "Role": "System Defense & Destroyer Corps", "Strategy": "Perimeter defense and anti-piracy, guarding key jump points."},
    {"Name": "The Tetnobautte (Third Fleet)", "Role": "Logistics, Archival & Resupply", "Strategy": "Maintaining supply lines and resource harvesting."},
    {"Name": "The Stihuu (Sentinel Guard)", "Role": "Royal Escort & Home World Defense", "Strategy": "Permanent deployment around core Tahkmahnelle worlds."}
]

# --- V. AWARDS, MEDALS, AND RIBBONS ---
HONORS_AND_AWARDS = {
    "VALOR_AND_SACRIFICE": [
        {"Name": "The Sovereign's Star of Valor (SSV)", "Purpose": "Awarded for an act of singular, extreme heroism above and beyond the call of duty."},
        {"Name": "The Ruby Star of the Void", "Purpose": "Awarded posthumously for the ultimate sacrifice in deep space."}
    ],
    "DISTINGUISHED_SERVICE": [
        {"Name": "The Order of the Chronometer", "Purpose": "Awarded for maintaining the integrity and precision of the T-Time navigation network."},
        {"Name": "The Gagoikenne Cross", "Purpose": "Awarded for consistently superior command and tactical leadership in non-combat roles."},
        {"Name": "The Service Ribbon of C'illiatnah", "Purpose": "Awarded for distinguished service in multi-branch operations."}
    ],
    "SERVICE_AND_CAMPAIGN": [
        {"Name": "T-Month Service Ribbons", "Purpose": "Issued for completing extended tours during a full 45-day T-Month cycle in a high-risk zone."},
        {"Name": "Planetary Defense Medal", "Purpose": "Issued for participation in the defense of a core world."}
    ]
}

# --- VI. OPERATIONAL DOCTRINES AND TREATISES ---
OPERATIONAL_DOCTRINES = {
    "TREATY_OF_TETNOBAUTTE": {
        "Focus": "Strategic use of all four Royal Forces.",
        "Core_Principle": "Defense through Predictability, Attack through Synchronization. Mandates all military actions be scheduled and executed according to the T-Time meter (H.M.S) for absolute coordination across light-years."
    },
    "VRAELVRAE_PROTOCOL": {
        "Focus": "Rules of engagement (ROE) with non-Tahkmahnelle entities.",
        "Core_Principle": "Escalation is authorized only when the sanctity of the T-Month cycle or planetary stability is threatened. Defines three stages of force projection."
    },
    "LORE_OF_ILLIANARRE": {
        "Focus": "Military discipline, personal conduct, and cultural integration.",
        "Core_Principle": "The duty of the soldier is not merely to fight, but to preserve the cultural and chronological integrity of the Tahkmahnelle domain."
    }
}

# --- VII. SUPPORTING CIVILIAN AGENCIES ---
SUPPORTING_AGENCIES = {
    "Bureau of Chronometric Integrity (BCI)": {
        "Mission": "Maintains and monitors the T-Time Chronometer network across all assets, ensuring absolute adherence to Quaternary Synchronization.",
        "Support": "Provides certified navigators and temporal technicians to RSC and RAD."
    },
    "Ministry of Applied Science (MAS)": {
        "Mission": "Focused on military R&D (TFP weapons, gravitic shielding, long-range propulsion).",
        "Support": "Operates classified research facilities and contracts R&D via the Oath of Innovation."
    },
    "Royal Logistics Guild (RLG)": {
        "Mission": "Manages the entire supply chain, from resource extraction to delivery of ordnance and rations to frontline units.",
        "Support": "Controls orbital dry docks and resource distribution hubs."
    }
}

# --- VIII. UNIFORMS AND CULTURAL RITUALS ---
CULTURAL_INTEGRATION = {
    "UNIFORMS": {
        "Formal Dress (Grand Edict Robe)": "Deep void-black fabric with Royal Violet trim. Features the Chronometer Sash, showing current T-Day/T-Week status.",
        "Service Duty (Aerium Standard)": "Charcoal-gray blend. Uses Cyan (Space/Air) or Khaki-Green (Ground/Oceanic) patches. Features Quaternary Meter Collar Pins.",
        "Combat Fatigue (Infiltrator Weave)": "Auto-camouflaging nanoweave, defaulting to Deep Nebula Blue. Features Thermal Signature Suppression and low-visibility rank insignia."
    },
    "RITUALS_AND_DOCTRINE": {
        "The Alignment Drill (A-Day)": "Compulsory simulation or live-fire exercise starting the 5-day cycle, focusing on rapid deployment.",
        "The Archive Edict (E-Day)": "Mandates reflection and knowledge review; personnel update personal logs and review mission histories.",
        "The Oath of Perpetual Service": "Commissioning oath taken on the T-Day of birth cycle, binding the member to the integrity of the domain.",
        "Retirement of the Sentinel": "Transition protocol for personnel completing nine full T-Months of active service, offering mentorship in the Gagoikenne Reserve."
    }
}

# --- IX. PRINTING FUNCTION ---

def display_database():
    """Prints the entire RTDC database structure."""
    
    print("\n=======================================================================")
    print("                 ROYAL TAHKMAHNELLE DEFENSE COMMAND DATABASE")
    print("=======================================================================\n")
    
    print("--- 1. COMMAND HIERARCHY ---")
    pp.pprint(COMMAND_HIERARCHY)
    print("\n" + "="*70 + "\n")
    
    print("--- 2. UNIFIED RANKS STRUCTURE (By Tier) ---")
    pp.pprint(UNIFIED_RANKS)
    print("\n" + "="*70 + "\n")
    
    print("--- 3. WEAPONS SYSTEMS (By Branch) ---")
    pp.pprint(WEAPONS_SYSTEMS)
    print("\n" + "="*70 + "\n")
    
    print("--- 4. RSC FLEET DESIGNATIONS ---")
    pp.pprint(RSC_FLEET_DESIGNATIONS)
    print("\n" + "="*70 + "\n")
    
    print("--- 5. HONORS AND AWARDS ---")
    pp.pprint(HONORS_AND_AWARDS)
    print("\n" + "="*70 + "\n")
    
    print("--- 6. OPERATIONAL DOCTRINES ---")
    pp.pprint(OPERATIONAL_DOCTRINES)
    print("\n" + "="*70 + "\n")
    
    print("--- 7. SUPPORTING CIVILIAN AGENCIES ---")
    pp.pprint(SUPPORTING_AGENCIES)
    print("\n" + "="*70 + "\n")
    
    print("--- 8. CULTURAL INTEGRATION (Uniforms & Rituals) ---")
    pp.pprint(CULTURAL_INTEGRATION)
    print("\n=======================================================================")

if __name__ == "__main__":
    display_database()

