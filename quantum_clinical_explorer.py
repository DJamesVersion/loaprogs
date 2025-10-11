import sys

# --- Assimilated Data Definition (Fusing Clinical/Quantum Paradoxes) ---
# Data structures are now structured as a series of complex clinical assessments.
EXPLORER_DATA = {
    "bunnies and rainbows": {
        "anomaly": "Genetic Anomaly: Chromosome 7 Frenulum Abnormality (FAM20C disruption). Diagnosed as a hyper-chromatic contagion (Bipolar I Equivalent).",
        "syndromic_correlate": "Triple Comorbidity Profile: High-risk alleles in DISC1 and CACNA1C interact with DMN hyperactivity, manifesting as spontaneous hopping and optical distortion.",
        "mitigation_protocol": "Pharmacogenomics-Guided Treatment: Bimodal rTMS (left DLPFC) synchronized with Vonoprazan (20mg/day) and nightly melatonin (6mg) to stabilize esophageal-temporal sync.",
        "quantum_entropy": "Induces counter-harmonic feedback loops in the Abstract Expressionist lattice. **5-Year Stability Projection: 92%** (vs. 60% in non-stabilized groups).",
    },
    "youth in asia": {
        "anomaly": "Triple Comorbidity (Manic $\leftrightarrow$ GERD $\leftrightarrow$ Schizoaffective, Bipolar Type). Symptom: Spatio-temporal dislocation toward grumpy garden gnomes.",
        "syndromic_correlate": "Prognostic Factor: Treatment Resistance (Failed trials of lithium/valproate). Linked to altered dopamine receptor expression (Molecular Psychiatry 2021 study).",
        "mitigation_protocol": "Antipsychotic Switch Protocol: Clozapine (150mg/day) + custom Nanodrugs (Dopamine D2 Partial Agonist Nanoparticles) targeting allele-specific DRD2 rs6277.",
        "quantum_entropy": "Freezes rhythmic complexity (tachyons) in music scores. Validated by **AFM force-displacement curves** showing sharp drop-off at $F_{ad} < 10 \text{ nN}$ in musical phase adherence.",
    },
    "blisterfist": {
        "anomaly": "Condition where overzealous conviction (Schizoaffective Psychosis) solidifies into high-impact metacarpals. Refractory to PPIs (omeprazole 40mg BID).",
        "syndromic_correlate": "Negative Indicator: Functional Decline anticipated at 5 years due to chronic psychosis and GERD-induced hypoxia. **Projected Mortality Risk: $\uparrow 40\%$**.",
        "mitigation_protocol": "Surveillance Protocol: Immersion in lukewarm tea while implementing Clozapine titration. Requires Annual endoscopy + 24-hour pH impedance monitoring.",
        "quantum_entropy": "Generates resonant frequencies causing terracotta sculptures to debate sonatas. The energy transfer adheres to **Tear Viscosity Rheometry ($\eta$ increases 300\% under cortisol exposure)**.",
    },
    "blue hero": {
        "anomaly": "Emotional state of benign, quiet melancholy (Mixed Depressive-Psychotic State). Subject believes they are protagonist of a low-budget Polish sci-fi film.",
        "syndromic_correlate": "Neurocircuitry Dysfunction: Hypoactive dorsolateral prefrontal cortex (dlPFC) combined with Amygdala-striatal circuit overactivation.",
        "mitigation_protocol": "Therapeutic Modality: Transcranial Photobiomodulation (Near-infrared laser stimulation of dlPFC) paired with a meal of burnt toast and milk.",
        "quantum_entropy": "Creates 'acoustic mirroring' where emotional state dictates key signature. EEG-fMRI correlates show a **15% reduction in amygdala BOLD signal** during musical exposure.",
    },
    "grass blues": {
        "anomaly": "Photosynthetic depression (Epigenetic Modification: BDNF promoter methylation) resulting from insufficient atmospheric oxygen exchange with flora's emotional centers.",
        "syndromic_correlate": "Cognitive Integrity: MMSE score 28/30 retained capacity for psychoeducation despite $\theta$-wave desynchronization and working memory deficits.",
        "mitigation_protocol": "Epigenetic Reprogramming: CRISPR-dCas9 demethylation of BDNF promoter in hippocampal neurons, combined with writing 100 thank-you notes to moss species.",
        "quantum_entropy": "Allows quantum entanglement between viewer's eye movements and brushstrokes to be perceived as a drone, reflecting **$\Psi_{risk}$ integral stability**.",
    },
    "od duck": {
        "anomaly": "The Defect of the Ordinary: Defective Unadhereance/Steady Tears in the Lacrimal-Cerebral Axis. Communicates only via 18th-century naval logs.",
        "syndromic_correlate": "Pathological Nexus: Vagus nerve irritation from chronic GIRD shows bidirectional modulation of affective episodes via gut-brain axis signaling.",
        "mitigation_protocol": "Gut Microbiome Intervention: Fecal microbiota transplantation combined with the completion of a composite jigsaw puzzle (mixed pieces) for cognitive resilience.",
        "quantum_entropy": "Enables 'Symbiotic Entropy' to be stabilized temporarily. Quantified via phenomenological assessment: **Sartre-Binswanger Index = $0.47 \pm 0.08$**.",
    },
    "your favorite vegetable": {
        "anomaly": "A philosophical quandary (Atman Projection Neutrality) where the preferred root/leaf/fruit becomes a psychological anchor, granting minor vegetable telekinesis.",
        "syndromic_correlate": "Existential Parameter: Universe Designation 'Unknown'. Linked to parietal cortex meta-cognition networks and chronic GERD $\rightarrow$ sleep disruption $\rightarrow$ episode triggers.",
        "mitigation_protocol": "Psychiatric Surveillance: Monthly Brief Psychiatric Rating Scale (BPRS) and YMRS, paired with the ritualistic, perfect peeling of an orange without consumption.",
        "quantum_entropy": "The sound of a single, perfectly timed raindrop becomes the master conductor, synchronizing the decay of analog sound and digital video via **Dopaminergic reward pathway activation**.",
    },
    "giraffe in the jug full of jelly": {
        "anomaly": "Cognitive Instability: Over-reliance on paradoxical metaphors leading to excessive grape preserves consumption and grammatical failure (Inability to use prepositions).",
        "syndromic_correlate": "Critical Window: Outlook is **Guarded Long-Term**. Intervention needed within $\leq 6$ months to prevent irreversible functional decline (due to Chronic GERD-induced hypoxia).",
        "mitigation_protocol": "Ethical Safeguards (4050 AD): Neural data encrypted via quantum blockchain, coupled with constructing a tiny scale model of the giraffe/jug using only lint and regret.",
        "quantum_entropy": "Warps musical tempo based on the artist's perceived altitude. This system exemplifies the Second Law: **Entropy Production ($\Delta S > 0$)** from defective bonding (Unadhereance).",
    },
}

def display_menu():
    """Displays the main menu of the assimilated medical explorer."""
    print("\n" + "#"*70)
    print("  QUANTUM PARALLELS / CLINICAL-PSYCHIATRIC FUSION EXPLORER (4050 AD)")
    print("  Assessment of Symbiotic Entropy Groups using Patient 1-2-3 Data")
    print("#"*70)
    
    concepts = list(EXPLORER_DATA.keys())
    
    # Use a professional, indexed list format
    for i, concept in enumerate(concepts):
        display_name = concept.title()
        print(f"  [{i + 1}] {display_name} - Status: Guarded Long-Term Outlook")
    
    print("\n  [Q] Exit Terminal (Risk: Catastrophic Decompensation)")
    print("-" * 70)

def display_concept_info(concept_key):
    """Displays the complex, assimilated analysis for a chosen concept."""
    data = EXPLORER_DATA[concept_key]
    
    print("\n" + "="*80)
    print(f"  PROGNOSTIC ASSESSMENT: {concept_key.upper()} (CASE FILE ID: {concept_key.split()[0].upper()}-A46X)")
    print("="*80)
    
    # Genetic/Phenotypic Anomaly
    print("\n--- I. Genetic/Phenotypic Anomaly ---")
    print(f"  Pathological Core: {data['anomaly']}")
    
    # Syndromic Correlate
    print("\n--- II. Clinical-Syndromic Correlate (Comorbidity Nexus) ---")
    print(f"  Negative Indicator $\leftrightarrow$ Bipolar/GERD Interplay: {data['syndromic_correlate']}")
    
    # Mitigation Protocol
    print("\n--- III. Evidence-Based Mitigation Strategy (Antidote/Stasis) ---")
    print(f"  Intervention Protocol: {data['mitigation_protocol']}")
    
    # Quantum Effect
    print("\n--- IV. Symbiotic Entropy Correlate (Quantum Realm) ---")
    print(f"  Theoretical Entanglement: {data['quantum_entropy']}")
    
    print("\n" + "="*80 + "\n")

def medical_explorer_app():
    """The main interactive loop for the terminal application."""
    while True:
        display_menu()
        
        user_input = input("Enter assessment selection [1-8 or Q to Exit]: ").strip().lower()
        
        # Handle Quit
        if user_input == 'q':
            print("\nExiting the Quantum-Clinical Fusion Explorer. All patient data is now encrypted via quantum blockchain.")
            sys.exit(0)
            
        # Handle Numeric Selection
        try:
            selection = int(user_input)
            concepts = list(EXPLORER_DATA.keys())
            
            if 1 <= selection <= len(concepts):
                concept_key = concepts[selection - 1]
                display_concept_info(concept_key)
                
                # Wait for user to continue before returning to menu
                input("Press Enter to continue analysis and prevent irreversible functional decline...")
            else:
                print(f"Error: Selection '{user_input}' is out of range. Must choose a number between 1 and {len(concepts)}.")
                
        except ValueError:
            # Handle non-numeric and invalid input
            if user_input != 'q':
                 print(f"Error: Invalid input '{user_input}'. Please enter a valid option number or 'Q'.")

if __name__ == "__main__":
    medical_explorer_app()

