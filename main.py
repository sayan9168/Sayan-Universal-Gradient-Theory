import math

def calculate_sug_energy(r, e_nb, delta_t):
    """
    Simplified implementation of the Sayan Universal Gradient (SUG)
    Theta_S = sqrt(E_nb) / (Delta_T * log(r))
    """
    try:
        theta_s = math.sqrt(e_nb) / (delta_t * math.log10(r))
        return theta_s
    except ValueError:
        return "Invalid input: Distance must be > 1 and Temperature must be non-zero."

# Example Calculation
distance = 1000  # km
energy = 50      # Megatons
temp_diff = 273  # Kelvin
print(f"SUG Constant (Theta_S): {calculate_sug_energy(distance, energy, temp_diff)}")
