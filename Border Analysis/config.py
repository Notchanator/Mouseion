NE_BASE = "https://naciscdn.org/naturalearth"

SOURCES = {
    "states": f"{NE_BASE}/10m/cultural/ne_10m_admin_1_states_provinces.zip",
    "ocean":  f"{NE_BASE}/10m/physical/ne_10m_ocean.zip",
    "rivers": f"{NE_BASE}/10m/physical/ne_10m_rivers_lake_centerlines.zip",
    "lakes":  f"{NE_BASE}/10m/physical/ne_10m_lakes.zip",
}

# Padding to use when clipping the layers to states.
PADDING = 1.0

# Padding around the state when plotting, as a fraction of the state's largest extent.
PLOT_PADDING = 0.05

# Preferred metric CRS per state for distance/buffer/area calculations.
STATE_CRS = {
    # --- Pacific Coast ---
    "California":       "EPSG:3310",    # CA Albers Equal Area (official statewide)
    "Oregon":           "EPSG:26910",   # UTM Zone 10N
    "Washington":       "EPSG:26910",   # UTM Zone 10N

    # --- Mountain West ---
    "Idaho":            "EPSG:26911",   # UTM Zone 11N
    "Nevada":           "EPSG:26911",   # UTM Zone 11N
    "Utah":             "EPSG:26912",   # UTM Zone 12N
    "Arizona":          "EPSG:26912",   # UTM Zone 12N
    "Colorado":         "EPSG:26913",   # UTM Zone 13N
    "New Mexico":       "EPSG:26913",   # UTM Zone 13N
    "Wyoming":          "EPSG:26913",   # UTM Zone 13N
    "Montana":          "EPSG:32100",   # MT State Plane (official statewide, meters)

    # --- Great Plains ---
    "North Dakota":     "EPSG:26914",   # UTM Zone 14N
    "South Dakota":     "EPSG:26914",   # UTM Zone 14N
    "Nebraska":         "EPSG:26914",   # UTM Zone 14N
    "Kansas":           "EPSG:26914",   # UTM Zone 14N
    "Oklahoma":         "EPSG:26914",   # UTM Zone 14N
    "Texas":            "EPSG:3083",    # TX Centric Albers Equal Area (spans 4 UTM zones)

    # --- Midwest ---
    "Minnesota":        "EPSG:26915",   # UTM Zone 15N
    "Iowa":             "EPSG:26915",   # UTM Zone 15N
    "Missouri":         "EPSG:26915",   # UTM Zone 15N
    "Arkansas":         "EPSG:26915",   # UTM Zone 15N
    "Wisconsin":        "EPSG:26916",   # UTM Zone 16N
    "Illinois":         "EPSG:26916",   # UTM Zone 16N
    "Indiana":          "EPSG:26916",   # UTM Zone 16N
    "Michigan":         "EPSG:3078",    # MI Oblique Mercator (covers UP + Lower Peninsula)
    "Ohio":             "EPSG:26917",   # UTM Zone 17N

    # --- Southeast ---
    "Louisiana":        "EPSG:26915",   # UTM Zone 15N
    "Mississippi":      "EPSG:26916",   # UTM Zone 16N
    "Alabama":          "EPSG:26916",   # UTM Zone 16N
    "Tennessee":        "EPSG:26916",   # UTM Zone 16N (state spans 15–17; 16 is central)
    "Kentucky":         "EPSG:3088",    # KY Single Zone (official statewide, meters)
    "West Virginia":    "EPSG:26917",   # UTM Zone 17N
    "Virginia":         "EPSG:26917",   # UTM Zone 17N
    "North Carolina":   "EPSG:26917",   # UTM Zone 17N
    "South Carolina":   "EPSG:26917",   # UTM Zone 17N
    "Georgia":          "EPSG:26917",   # UTM Zone 17N
    "Florida":          "EPSG:26917",   # UTM Zone 17N (spans 16–17; 17 covers most)

    # --- Mid-Atlantic ---
    "Pennsylvania":     "EPSG:26918",   # UTM Zone 18N
    "New York":         "EPSG:26918",   # UTM Zone 18N
    "New Jersey":       "EPSG:26918",   # UTM Zone 18N
    "Delaware":         "EPSG:26918",   # UTM Zone 18N
    "Maryland":         "EPSG:26918",   # UTM Zone 18N

    # --- New England ---
    "Connecticut":      "EPSG:26918",   # UTM Zone 18N
    "Vermont":          "EPSG:26918",   # UTM Zone 18N
    "Rhode Island":     "EPSG:26919",   # UTM Zone 19N
    "Massachusetts":    "EPSG:26919",   # UTM Zone 19N
    "New Hampshire":    "EPSG:26919",   # UTM Zone 19N
    "Maine":            "EPSG:26919",   # UTM Zone 19N

    # --- Non-contiguous ---
    "Alaska":           "EPSG:3338",    # AK Albers Equal Area (spans many UTM zones)
    "Hawaii":           "EPSG:26904",   # UTM Zone 4N (main islands; Big Island spans 4–5)
}
