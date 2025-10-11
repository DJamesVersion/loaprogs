import math
# Use math.pi for the core area and attenuation calculations
PI = math.pi

# --- NEW: System Hardware Parameters ---
FREQ_START_MHZ = 950
FREQ_END_MHZ = 2150
DC_VOLTAGE = 18.0

# --- 1. Radio Astronomy Signal Analysis (using PI) ---
def calculate_radio_signal_strength(telescope_diameter_m, distance_light_years, source_power_watts):
    """
    Calculates the received signal flux density at a radio telescope.

    The calculation uses PI for two main components:
    1. Telescope Effective Area (A) = PI * (D/2)^2
    2. Signal Attenuation (Inverse Square Law) = 4 * PI * R^2
    """
    
    # Constants
    M_PER_LY = 9.461e15  # Meters per Light Year
    distance_m = distance_light_years * M_PER_LY

    # 1. Calculate the effective area of the telescope using PI
    telescope_area_sq_m = PI * (telescope_diameter_m / 2)**2
    
    # 2. Calculate the total power spread over the shell at that distance (4*PI*R^2)
    shell_area_sq_m = 4 * PI * distance_m**2
    
    # Calculate Flux Density (Power per unit area at distance R)
    flux_density_w_per_sq_m = source_power_watts / shell_area_sq_m
    
    # Calculate Received Power (Watts)
    received_power_watts = flux_density_w_per_sq_m * telescope_area_sq_m
    
    # Convert to a more readable unit (e.g., Femto-watts, 1e-15 W)
    received_power_fW = received_power_watts * 1e15 
    
    print(f"--- Radio Astronomy Analysis (using PI for Area and Attenuation) ---")
    print(f"Telescope Effective Area: {telescope_area_sq_m:.2e} m²")
    print(f"Signal Flux Density at Planet: {flux_density_w_per_sq_m:.2e} W/m²")
    print(f"Received Power (P_sig): {received_power_fW:.4f} fW (FemtoWatts)")
    print("-" * 50)
    
    return received_power_watts, received_power_fW

# --- 2. System Performance and Noise Floor (using new parameters) ---
def analyze_system_performance(received_power_watts, freq_start, freq_end, dc_voltage):
    """
    Simulates system noise and detectability based on hardware specs.
    
    Noise Power (P_noise) is calculated using Boltzmann's constant (k) * System Temperature (T_sys) * Bandwidth (B).
    """
    
    # Constants
    BOLTZMANN_CONSTANT = 1.38e-23  # J/K (Used to determine noise power)

    # 1. Bandwidth Calculation
    bandwidth_hz = (freq_end - freq_start) * 1e6
    center_freq_mhz = (freq_start + freq_end) / 2
    
    # 2. System Noise Temperature (T_sys)
    # Hypothetical T_sys inversely related to DC_VOLTAGE (better power filtering/LNA performance at higher voltage)
    # The factor of 30 is purely illustrative for this simulation.
    hypothetical_t_sys_kelvin = 30 * (24.0 / dc_voltage) 

    # 3. Noise Power (P_noise)
    # P_noise = k * T_sys * B
    noise_power_watts = BOLTZMANN_CONSTANT * hypothetical_t_sys_kelvin * bandwidth_hz
    noise_power_fW = noise_power_watts * 1e15

    # 4. Signal-to-Noise Ratio (SNR)
    # SNR = P_sig / P_noise
    snr = received_power_watts / noise_power_watts
    snr_db = 10 * math.log10(snr) if snr > 0 else -99.9

    print(f"--- System Performance Analysis ({freq_start}-{freq_end} MHz at {dc_voltage}V DC) ---")
    print(f"Operational Bandwidth: {bandwidth_hz/1e6:.1f} MHz")
    print(f"Center Frequency: {center_freq_mhz:.1f} MHz")
    print(f"Hypothetical System Noise Temp (T_sys): {hypothetical_t_sys_kelvin:.2f} K")
    print(f"Noise Power (P_noise): {noise_power_fW:.4f} fW")
    
    # Detection Conclusion
    if snr_db > 10:
        conclusion = "SIGNAL DETECTABLE (High SNR)"
    elif snr_db > 3:
        conclusion = "SIGNAL MARGINAL (Needs integration)"
    else:
        conclusion = "SIGNAL UNDETECTABLE (Below noise floor)"
        
    print(f"Signal-to-Noise Ratio (SNR): {snr_db:.2f} dB -> {conclusion}")
    print("-" * 50)
    
    return snr_db

# --- 3. Exobiology/Habitable Zone Analysis (using PI) ---
def calculate_exobiology_metrics(stellar_luminosity_solar_units, planet_radius_km):
    """
    Calculates the Habitable Zone (HZ) boundaries and planet surface area.
    Planet Surface Area (A) = 4 * PI * R^2
    """
    
    # Habitable Zone (HZ) reference distances (Astronomical Units, AU)
    INNER_HZ_REF = 0.95 
    OUTER_HZ_REF = 1.67 
    
    # HZ Distance (a) = Reference Distance * sqrt(Stellar Luminosity)
    sqrt_L = math.sqrt(stellar_luminosity_solar_units)
    
    inner_hz_au = INNER_HZ_REF * sqrt_L
    outer_hz_au = OUTER_HZ_REF * sqrt_L
    
    # Calculate the planet's total surface area using PI
    planet_radius_m = planet_radius_km * 1000
    planet_surface_area_sq_m = 4 * PI * planet_radius_m**2
    
    # Exobiology Index: A simple, hypothetical index related to PI and surface area
    # This factor uses PI to scale the result and make it relevant to the constant
    EXO_SCALING_FACTOR = 1 / PI 
    biomass_potential_index = planet_surface_area_sq_m * EXO_SCALING_FACTOR * 1e-12 
    
    print(f"--- Exobiology Analysis (using PI for Surface Area and HZ) ---")
    print(f"Stellar Luminosity: {stellar_luminosity_solar_units} L_sun")
    print(f"Habitable Zone Inner Edge: {inner_hz_au:.3f} AU")
    print(f"Habitable Zone Outer Edge: {outer_hz_au:.3f} AU")
    print(f"Exoplanet Surface Area: {planet_surface_area_sq_m:.2e} m²")
    print(f"Hypothetical Biomass Potential (Scaled by PI): {biomass_potential_index:.2f}")
    print("-" * 50)
    
    return inner_hz_au, outer_hz_au, planet_surface_area_sq_m


# --- Main Execution ---

# Parameters for the hypothetical star system and observatory
TELESCOPE_DIAMETER = 100.0   # Diameter of Radio Telescope (meters)
STAR_DISTANCE = 50.0        # Distance to star system (ly)
STELLAR_LUMINOSITY = 0.85   # Star's luminosity (L_sun)
SIGNAL_SOURCE_POWER = 1e12  # Hypothetical intelligent signal power (Watts)
PLANET_RADIUS = 6500.0      # Exoplanet radius (km)

# Execute the simulation components
print(f"--- Cosmic Pi Calculator Initiated (PI = {PI:.10f}) ---")
print()

# 1. Radio Astronomy Signal Strength
received_power_watts, received_power_fW = calculate_radio_signal_strength(
    telescope_diameter_m=TELESCOPE_DIAMETER,
    distance_light_years=STAR_DISTANCE,
    source_power_watts=SIGNAL_SOURCE_POWER
)

# 2. System Performance and Noise Floor Analysis
analyze_system_performance(
    received_power_watts=received_power_watts,
    freq_start=FREQ_START_MHZ,
    freq_end=FREQ_END_MHZ,
    dc_voltage=DC_VOLTAGE
)

# 3. Exobiology
calculate_exobiology_metrics(
    stellar_luminosity_solar_units=STELLAR_LUMINOSITY,
    planet_radius_km=PLANET_RADIUS
)

print("Analysis Complete.")

