#!/bin/bash

# This script requires Bash 4.0+ for associative arrays.

# --- Terminal Colors ---
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# --- Data Assimilation: Fusing Clinical and Quantum Paradoxes ---
# We use parallel associative arrays to map the eight concepts to their four data fields.
declare -A CONCEPTS
declare -A ANOMALY
declare -A SYNDROMIC_CORRELATE
declare -A MITIGATION_PROTOCOL
declare -A QUANTUM_ENTROPY

# Define Concept Keys (for iteration)
CONCEPTS[1]="bunnies and rainbows"
CONCEPTS[2]="youth in asia"
CONCEPTS[3]="blisterfist"
CONCEPTS[4]="blue hero"
CONCEPTS[5]="grass blues"
CONCEPTS[6]="od duck"
CONCEPTS[7]="your favorite vegetable"
CONCEPTS[8]="giraffe in the jug full of jelly"

# --- ANOMALY Data ---
ANOMALY["bunnies and rainbows"]="Genetic Anomaly: Chromosome 7 Frenulum Abnormality (FAM20C disruption). Diagnosed as a hyper-chromatic contagion (Bipolar I Equivalent)."
ANOMALY["youth in asia"]="Triple Comorbidity (Manic $\leftrightarrow$ GERD $\leftrightarrow$ Schizoaffective, Bipolar Type). Symptom: Spatio-temporal dislocation toward grumpy garden gnomes."
ANOMALY["blisterfist"]="Condition where overzealous conviction (Schizoaffective Psychosis) solidifies into high-impact metacarpals. Refractory to PPIs (omeprazole 40mg BID)."
ANOMALY["blue hero"]="Emotional state of benign, quiet melancholy (Mixed Depressive-Psychotic State). Subject believes they are protagonist of a low-budget Polish sci-fi film."
ANOMALY["grass blues"]="Photosynthetic depression (Epigenetic Modification: BDNF promoter methylation) resulting from insufficient atmospheric oxygen exchange with flora's emotional centers."
ANOMALY["od duck"]="The Defect of the Ordinary: Defective Unadhereance/Steady Tears in the Lacrimal-Cerebral Axis. Communicates only via 18th-century naval logs."
ANOMALY["your favorite vegetable"]="A philosophical quandary (Atman Projection Neutrality) where the preferred root/leaf/fruit becomes a psychological anchor, granting minor vegetable telekinesis."
ANOMALY["giraffe in the jug full of jelly"]="Cognitive Instability: Over-reliance on paradoxical metaphors leading to excessive grape preserves consumption and grammatical failure (Inability to use prepositions)."

# --- SYNDROMIC_CORRELATE Data ---
SYNDROMIC_CORRELATE["bunnies and rainbows"]="Triple Comorbidity Profile: High-risk alleles in DISC1 and CACNA1C interact with DMN hyperactivity, manifesting as spontaneous hopping and optical distortion."
SYNDROMIC_CORRELATE["youth in asia"]="Prognostic Factor: Treatment Resistance (Failed trials of lithium/valproate). Linked to altered dopamine receptor expression (Molecular Psychiatry 2021 study)."
SYNDROMIC_CORRELATE["blisterfist"]="Negative Indicator: Functional Decline anticipated at 5 years due to chronic psychosis and GERD-induced hypoxia. ${RED}Projected Mortality Risk: \uparrow 40\%{NC}$."
SYNDROMIC_CORRELATE["blue hero"]="Neurocircuitry Dysfunction: Hypoactive dorsolateral prefrontal cortex (dlPFC) combined with Amygdala-striatal circuit overactivation."
SYNDROMIC_CORRELATE["grass blues"]="Cognitive Integrity: MMSE score 28/30 retained capacity for psychoeducation despite $\theta$-wave desynchronization and working memory deficits."
SYNDROMIC_CORRELATE["od duck"]="Pathological Nexus: Vagus nerve irritation from chronic GIRD shows bidirectional modulation of affective episodes via gut-brain axis signaling."
SYNDROMIC_CORRELATE["your favorite vegetable"]="Existential Parameter: Universe Designation 'Unknown'. Linked to parietal cortex meta-cognition networks and chronic GERD $\rightarrow$ sleep disruption $\rightarrow$ episode triggers."
SYNDROMIC_CORRELATE["giraffe in the jug full of jelly"]="Critical Window: Outlook is ${RED}Guarded Long-Term${NC}$. Intervention needed within $\leq 6$ months to prevent irreversible functional decline (due to Chronic GERD-induced hypoxia)."

# --- MITIGATION_PROTOCOL Data ---
MITIGATION_PROTOCOL["bunnies and rainbows"]="Pharmacogenomics-Guided Treatment: Bimodal rTMS (left DLPFC) synchronized with Vonoprazan (20mg/day) and nightly melatonin (6mg) to stabilize esophageal-temporal sync."
MITIGATION_PROTOCOL["youth in asia"]="Antipsychotic Switch Protocol: Clozapine (150mg/day) + custom Nanodrugs (Dopamine D2 Partial Agonist Nanoparticles) targeting allele-specific DRD2 rs6277."
MITIGATION_PROTOCOL["blisterfist"]="Surveillance Protocol: Immersion in lukewarm tea while implementing Clozapine titration. Requires Annual endoscopy + 24-hour pH impedance monitoring."
MITIGATION_PROTOCOL["blue hero"]="Therapeutic Modality: Transcranial Photobiomodulation (Near-infrared laser stimulation of dlPFC) paired with a meal of burnt toast and milk."
MITIGATION_PROTOCOL["grass blues"]="Epigenetic Reprogramming: CRISPR-dCas9 demethylation of BDNF promoter in hippocampal neurons, combined with writing 100 thank-you notes to moss species."
MITIGATION_PROTOCOL["od duck"]="Gut Microbiome Intervention: Fecal microbiota transplantation combined with the completion of a composite jigsaw puzzle (mixed pieces) for cognitive resilience."
MITIGATION_PROTOCOL["your favorite vegetable"]="Psychiatric Surveillance: Monthly Brief Psychiatric Rating Scale (BPRS) and YMRS, paired with the ritualistic, perfect peeling of an orange without consumption."
MITIGATION_PROTOCOL["giraffe in the jug full of jelly"]="Ethical Safeguards (4050 AD): Neural data encrypted via quantum blockchain, coupled with constructing a tiny scale model of the giraffe/jug using only lint and regret."

# --- QUANTUM_ENTROPY Data ---
QUANTUM_ENTROPY["bunnies and rainbows"]="Induces counter-harmonic feedback loops in the Abstract Expressionist lattice. ${GREEN}5-Year Stability Projection: 92\%\text{ (vs. 60\% in non-stabilized groups)}{NC}$."
QUANTUM_ENTROPY["youth in asia"]="Freezes rhythmic complexity (tachyons) in music scores. Validated by AFM force-displacement curves showing sharp drop-off at $F_{ad} < 10 \text{ nN}$ in musical phase adherence."
QUANTUM_ENTROPY["blisterfist"]="Generates resonant frequencies causing terracotta sculptures to debate sonatas. The energy transfer adheres to Tear Viscosity Rheometry ($\eta$ increases 300\% under cortisol exposure)."
QUANTUM_ENTROPY["blue hero"]="Creates 'acoustic mirroring' where emotional state dictates key signature. EEG-fMRI correlates show a ${BLUE}15\% \text{ reduction in amygdala BOLD signal}$ during musical exposure."
QUANTUM_ENTROPY["grass blues"]="Allows quantum entanglement between viewer's eye movements and brushstrokes to be perceived as a drone, reflecting $\Psi_{risk}$ integral stability."
QUANTUM_ENTROPY["od duck"]="Enables 'Symbiotic Entropy' to be stabilized temporarily. Quantified via phenomenological assessment: Sartre-Binswanger Index $= 0.47 \pm 0.08$."
QUANTUM_ENTROPY["your favorite vegetable"]="The sound of a single, perfectly timed raindrop becomes the master conductor, synchronizing the decay of analog sound and digital video via Dopaminergic reward pathway activation."
QUANTUM_ENTROPY["giraffe in the jug full of jelly"]="Warps musical tempo based on the artist's perceived altitude. This system exemplifies the Second Law: Entropy Production ($\Delta S > 0$) from defective bonding (Unadhereance)."


function display_menu() {
    clear
    echo -e "${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}"
    echo -e "  ${YELLOW}QUANTUM PARALLELS / CLINICAL-PSYCHIATRIC FUSION EXPLORER (SH v1.0)${NC}"
    echo -e "  ${BLUE}Assessment of Symbiotic Entropy Groups using Patient 1-2-3 Data${NC}"
    echo -e "${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}#${CYAN}#${NC}"
    
    for i in {1..8}; do
        KEY="${CONCEPTS[$i]}"
        # Capitalize first letter of each word for display
        DISPLAY_NAME=$(echo "$KEY" | sed -E 's/\b([a-z])/\U\1/g')
        echo -e "  [${GREEN}$i${NC}] ${DISPLAY_NAME} - ${RED}Status: Guarded Long-Term Outlook${NC}"
    done
    
    echo -e "\n  [${RED}Q${NC}] Exit Terminal (${RED}Risk: Catastrophic Decompensation${NC})"
    echo -e "${CYAN}----------------------------------------------------------------------${NC}"
}

function display_concept_info() {
    local key=$1
    local id=$(echo "$key" | awk '{print toupper(substr($1, 1, 1))}') # E.g., B for bunnies
    
    clear
    echo -e "${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}"
    echo -e "  ${RED}PROGNOSTIC ASSESSMENT: ${key^^} (CASE FILE ID: ${id}-A46X)${NC}"
    echo -e "${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}#${YELLOW}#${NC}"
    
    echo -e "\n${CYAN}--- I. Genetic/Phenotypic Anomaly ---${NC}"
    echo -e "  Pathological Core: ${ANOMALY[$key]}"
    
    echo -e "\n${CYAN}--- II. Clinical-Syndromic Correlate (Comorbidity Nexus) ---${NC}"
    echo -e "  Negative Indicator $\leftrightarrow$ Bipolar/GERD Interplay: ${SYNDROMIC_CORRELATE[$key]}"
    
    echo -e "\n${CYAN}--- III. Evidence-Based Mitigation Strategy (Antidote/Stasis) ---${NC}"
    echo -e "  Intervention Protocol: ${MITIGATION_PROTOCOL[$key]}"
    
    echo -e "\n${CYAN}--- IV. Symbiotic Entropy Correlate (Quantum Realm) ---${NC}"
    echo -e "  Theoretical Entanglement: ${QUANTUM_ENTROPY[$key]}"
    
    echo -e "\n${YELLOW}================================================================================${NC}\n"
}

# --- Main Application Loop ---
while true; do
    display_menu
    
    read -r -p "Enter assessment selection [1-8 or Q to Exit]: " USER_INPUT
    
    case "$USER_INPUT" in
        [1-8])
            CONCEPT_KEY="${CONCEPTS[$USER_INPUT]}"
            if [[ -n "$CONCEPT_KEY" ]]; then
                display_concept_info "$CONCEPT_KEY"
                read -r -p "Press Enter to continue analysis and prevent irreversible functional decline..."
            else
                echo -e "${RED}Error: Invalid index. Please select a number from 1 to 8.${NC}"
                sleep 2
            fi
            ;;
        [Qq]*)
            clear
            echo -e "\n${GREEN}Exiting the Quantum-Clinical Fusion Explorer. All patient data is now encrypted via quantum blockchain.${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}Error: Invalid input '$USER_INPUT'. Please enter a valid option number or 'Q'.${NC}"
            sleep 2
            ;;
    esac
done

