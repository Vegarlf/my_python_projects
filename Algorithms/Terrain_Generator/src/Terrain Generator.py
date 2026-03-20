import time

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# --- CONFIGURATION ---
# np.random.seed(42)
STARTTIME = time.time()
GRIDSIZE = 500
SMOOTHNESSA = 250
SMOOTHNESSB = 25

# --- CONTROLS ---
# 1. SEA_LEVEL (0.0 to 1.0):
#    Where the ocean stops. Higher = Less Land, but mountains stay tall.
SEA_LEVEL = 0.35

# 2. ROUGHNESS (0.0 to 1.0):
#    How much "jagged" noise to add on top of the smooth continents.
ROUGHNESS_STRENGTH = 0.3

# 3. MOUNTAIN_MULTIPLIER (1.0 to 3.0):
#    Stretches the mountains up HIGHER without affecting the coast.
MOUNTAIN_MULTIPLIER = 1.2


def gettime(starttime):
    timefinish = time.time() - starttime
    string = f"Calc Done in {timefinish:.3f} seconds."
    return string


# --- HELPER FUNCTION: Make a Map Layer ---
def generate_layer(smooth_steps):
    # 1. Start with noise
    layer = np.random.uniform(0, 1, (GRIDSIZE, GRIDSIZE))

    # 2. Smooth it (Vectorized Neighbor Averaging)
    for i in range(smooth_steps):
        up = np.roll(layer, -1, axis=0)
        down = np.roll(layer, 1, axis=0)
        left = np.roll(layer, -1, axis=1)
        right = np.roll(layer, 1, axis=1)
        layer = (layer + up + down + left + right) / 5

    # 3. Normalize immediately so this layer is predictable (0.0 to 1.0)
    layer = (layer - np.min(layer)) / (np.max(layer) - np.min(layer))
    return layer


currentseed = int(time.time())

np.random.seed(currentseed)

# currentseed = None

print(f"Generating World With Seed: {currentseed}")

# --- PART 1: GENERATE LAYERS (The "Octaves") ---

# Layer A: "Continents" (Very smooth, defines shape)
base_layer = generate_layer(smooth_steps=SMOOTHNESSA)

# Layer B: "Details" (Not smooth, adds the variation you wanted)
detail_layer = generate_layer(smooth_steps=SMOOTHNESSB)

# --- PART 2: COMBINE LAYERS ---
# We mix them based on the user's ROUGHNESS setting.
# A smooth base with a sprinkle of detail on top.
worldmap = (base_layer * (1 - ROUGHNESS_STRENGTH)) + (detail_layer * ROUGHNESS_STRENGTH)

# Re-normalize the combined map to 0.0-1.0
worldmap = (worldmap - np.min(worldmap)) / (np.max(worldmap) - np.min(worldmap))


# --- PART 3: APPLY CONTROLS (Smart Terraforming) ---

# A. Apply Sea Level
# Instead of subtracting (which shrinks mountains), we just "clip" the bottom.
# But for the visual heatmap, we want water to be 0.
# So we shift everything, but we stretch the remaining land so it still hits 1.0.

# 1. Mask out the water (Anything below sea level becomes 0)
# We make a copy to work on
final_map = worldmap.copy()

# 2. "Zero out" the ocean (make it flat)
final_map[final_map < SEA_LEVEL] = SEA_LEVEL

# 3. Shift down so the shoreline starts at 0.0
final_map = final_map - SEA_LEVEL

# 4. Stretch the Mountains (Recover the height)
final_map = final_map * MOUNTAIN_MULTIPLIER

# Currently, max height is (1.0 - SEA_LEVEL). We want it back at 1.0 * Multiplier.
max_current = np.max(final_map)
if max_current > 0:  # Avoid division by zero if world is empty
    final_map = final_map / max_current  # Now 0.0 to 1.0
# ... (After your terrain generation code) ...

# --- PART 4: PHYSICS (CALCULATING SLOPE) ---

# np.gradient returns a list of arrays [gradient_y, gradient_x]
grads = np.gradient(final_map)
grad_y = grads[0]
grad_x = grads[1]

# Calculate Magnitude (Total Steepness)
slope_map = np.hypot(grad_x, grad_y)

# Normalize Slope Map for better viewing (0.0 to 1.0)
slope_map = (slope_map - np.min(slope_map)) / (np.max(slope_map) - np.min(slope_map))


print(gettime(starttime=STARTTIME))
print(
    f"Sea Level: {SEA_LEVEL}, Roughness: {ROUGHNESS_STRENGTH}, Mountain Multiplier: {MOUNTAIN_MULTIPLIER}\nGridsize: {GRIDSIZE},  Smoothed: A: {SMOOTHNESSA},   B:{SMOOTHNESSB} "
)

# --- PART 4: VISUALIZATION ---
plt.figure(figsize=(14, 7))

# We use vmin=0 to lock Sea Level.
# We set vmax to MOUNTAIN_MULTIPLIER so the color scale fits our new tall peaks.
plt.subplot(1, 2, 1)
sns.heatmap(
    final_map,
    cmap="terrain",
    vmin=0,
    vmax=1.0,
    cbar=True,
    xticklabels=False,
    yticklabels=False,
)
plt.title("Multi-Layer Terrain")

plt.subplot(1, 2, 2)
# 'magma' is great for intensity (Black = Flat, Bright Orange = Cliff)
sns.heatmap(slope_map, cmap="magma", cbar=True, xticklabels=False, yticklabels=False)
plt.title("Slope/Cliff Map")
plt.tight_layout()
plt.show()
