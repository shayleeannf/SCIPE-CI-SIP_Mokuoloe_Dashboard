import streamlit as st
import pandas as pd
import plotly.express as px

# CHANGE TEXT TO TIMES NEW ROMAN (LEAVING BACKGROUND AT DEFAULT)
st.markdown(
    """
    <style>
    /* target headers, paragraphs, lists, and bold text elements */
    h1, h2, h3, h4, h5, h6, p, li, strong, em {
        font-family: 'Times New Roman', Times, Baskerville, Georgia, serif !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Set up page styling
st.set_page_config(page_title="Mokuoloe Climate Risk", layout="wide")
st.title("🌊 The Vulnerability of Mokuoloe (Coconut Island)")

# --- THE PROJECT SCOPE: MOKUOLOE MAP ---
st.markdown("---")
st.header("🏝️ Where are we looking?")
st.markdown("""
Our specific focus is **Mokuoloe**, commonly known as Coconut Island, which sits within 
the large natural lagoon of Kāne’ohe Bay on the windward (eastern) coast of O'ahu. 
""")

# 1. Provide the specific location data for Mokuoloe
map_data = pd.DataFrame({
    'Island Name': ['Mokuoloe (Coconut Island)'],
    'lat': [21.4337],  # Latitude for Mokuoloe
    'lon': [-157.7885]  # Longitude for Mokuoloe
})

# 2. Build the map chart using Plotly's scatter_mapbox function
fig_map = px.scatter_map(
    map_data,
    lat='lat',
    lon='lon',
    hover_name='Island Name', # When you hover, it shows the name
    zoom=11.5, # This level of zoom shows all of Oahu
    height=450
)

# 3. Add styling to the marker and the base map
fig_map.update_traces(
    marker=dict(
        size=15,          # Make the marker big enough to see
        color='#D9383A'   # Use a strong color (Crimson Red) for high contrast
    )
)

# 4. Use a clear, standard terrain background (so you can see land vs. water)
fig_map.update_layout(
    map="open-street-map", # Use a standard, clear map base
    margin={"r":0,"t":0,"l":0,"b":0} # Remove all white margins
)

# 5. Display the final map in your Streamlit dashboard
st.plotly_chart(fig_map, use_container_width=True)

# --- CHAPTER 1: THE HOOK ---
st.markdown("""
### Why this matters right now:
Mokuoloe isn't just a beautiful island in Kāneʻohe Bay; it is a vital hub for marine biology research. 
Because it sits at sea level, even a few centimeters of rising ocean waters drastically change how often 
the island floods, threatening facilities, coral research, and coastal ecosystems. 
""")

st.write("---") # Visual divider line

# --- CHAPTER 2: THE CAUSE (SLR Projections) ---
st.header("1. The Driving Force: Sea Level Rise Projections")

# Your narrative explanation excerpt
st.markdown("""
### 📊 Understanding the "Climate Scenarios"
When you look at these models, each scenario represents a different global future based on human greenhouse gas emissions. 
But there is a twist: these models are built using **Global Mean Sea Level (GMSL)** targets. 

For example, when a model simulates a **1.0-meter scenario**, it is asking: 
> *"If the global average ocean height rises by 1.0 meter, what actually happens locally right here on the shores of Mokuoloe?"*

Because of local factors like changing ocean currents, regional water temperatures, and whether the land in Hawaii is rising or sinking (**Vertical Land Motion**), the local sea level rise at Mokuoloe might be higher or lower than the global average. The line chart below tracks that specific, localized future for our island.
""")

# Load the Sea Level Rise Data
slr_df = pd.read_csv("mokuoloe_slr_projections_clean.csv")

# The dropdown and chart follow right below it...
selected_scenario = st.selectbox(
    "Choose a Sea Level Rise Scenario to visualize:",
    options=slr_df['Scenario'].unique()
)

# # 2. FIXED: Filter using capital 'Scenario'
filtered_slr = slr_df[slr_df['Scenario'] == selected_scenario]

# # 3. FIXED: Sort the data by year so the line connects smoothly from left to right
filtered_slr = filtered_slr.sort_values(by='RSL_Scenario_Year')

# Make an official copy so we can cleanly modify the data and labels without warnings
filtered_slr = filtered_slr.copy()

# CLEAN THE LABELS: Strip out "RSL" and " (cm)" from the year column
filtered_slr['RSL_Scenario_Year'] = filtered_slr['RSL_Scenario_Year'].astype(str).str.replace('RSL', '').str.replace(' (cm)', '', regex=False)

# CONVERT TO METERS: Divide the centimeter column by 100 to create a new meters column
filtered_slr['RSL_Value_m'] = filtered_slr['RSL_Value_cm'] / 100

# # 4. FIXED: Map the X axis to Year and the Y axis to the new Meters column
fig_slr = px.line(
    filtered_slr,
    x='RSL_Scenario_Year',
    y='RSL_Value_m',  # Swapped to the new meters column
    title=f"Projected Rise Over Time (meters) – Scenario: {selected_scenario}",
    labels={'RSL_Scenario_Year': 'Year(RSL)', 'RSL_Value_m': 'Rise (meters)'}  # Updated label to meters
)

# Style it with a high-visibility red line
fig_slr.update_traces(line_color='#D9383A', line_width=4)

# Force the x-axis to treat the cleaned numbers as text categories so they space nicely
fig_slr.update_layout(
    xaxis=dict(type='category')
)

st.plotly_chart(fig_slr, use_container_width=True)

# --- CHAPTER 3: THE EFFECT (Extreme Water Levels) ---
st.header("2. The Immediate Threat: Tipping Points & Flooding")

st.markdown("""
### 📊 Understanding "Return Levels" (yrRL)
When looking at the flood thresholds below, you will see metrics labeled with **yrRL**, which stands for **Year Return Level**. 

This is a way scientists measure how rare and severe an extreme water level event is:
* **1yrRL:** An extreme high water level that happens roughly **once every year**.
* **10yrRL:** A severe flooding event that happens roughly **once every 10 years**.
* **100yrRL:** A catastrophic extreme water level event that historically only happens **once every 100 years** (a 1% chance each year).

Sea level rise acts as an amplifier. As the baseline ocean height rises, what used to be a rare '100-year flood' will begin happening every few years, and eventually, every single month.
""")

# Load and display your original bar chart data
ewl_df = pd.read_csv("mokuoloe_ewl_clean_.csv")

# Make an official copy so we can cleanly modify the labels without warnings
ewl_df_clean = ewl_df.copy()

# CLEAN THE LABELS: Strip out both variations of the meter text
ewl_df_clean['flood_metric'] = ewl_df_clean['flood_metric'].astype(str).str.replace(' (meters)', '', regex=False).str.replace('(m)', '', regex=False)

# FIXED: Updated the data source to the clean dataframe and simplified the x-axis label
fig_ewl = px.bar(
    ewl_df_clean, 
    x='flood_metric', 
    y='water_level_value',
    title="Historical Extreme Water Level Thresholds for Oahu Stations",
    labels={'flood_metric': 'Flooding Metric', 'water_level_value': 'Water Level (meters)'}
)

fig_ewl.update_traces(marker_color='#5A86AD')

# Force the x-axis to treat the numbers as distinct text categories so they look clean
fig_ewl.update_layout(
    xaxis=dict(type='category')
)

st.plotly_chart(fig_ewl, use_container_width=True)

# --- CHAPTER 4: THE FUTURE FORECAST (COMBINED IMPACT) ---
st.write("---")
st.header("🔮 The Grand Finale: Predicting Future Storm Crests")
st.markdown("""
### See the Combined Power of Both Datasets:
Now, let's look into the future. By combining the permanent baseline sea level rise with a temporary 
historical extreme storm event, we can see exactly how high future floods will crest on Mokuoloe. 

> **What does "Crest Height" mean?** The crest height is the absolute highest peak or maximum elevation that the water surface reaches during a flood event. 
> Think of it as the ultimate high-water mark on land. If the crest height is higher than the island's docks or foundations, 
> those areas will be completely submerged.

**Select a flood event below** to see how its threat increases over time under your chosen climate scenario.
""")

# (The rest of your code for the dropdown, math, and chart stays exactly the same!)

# 1. Dropdown for the user to choose an extreme water level metric
selected_metric = st.selectbox(
    "Select an Extreme Flood Event (Return Level):",
    options=ewl_df['flood_metric'].unique(),
    index=list(ewl_df['flood_metric'].unique()).index('100yrRL(m)') # Default to the 100-year flood
)

# 2. Extract the exact meter value for that selected storm event from your bar graph data
storm_spike_m = ewl_df[ewl_df['flood_metric'] == selected_metric]['water_level_value'].values[0]

# # 3. Create a copy of the filtered timeline data to do the predictive math
forecast_df = filtered_slr.copy()

# CLEAN THE LABELS: Strip out "RSL" and " (cm)" to leave just the 4-digit year text
forecast_df['RSL_Scenario_Year'] = forecast_df['RSL_Scenario_Year'].str.replace('RSL', '').str.replace(' (cm)', '', regex=False)

# 4. Do the math: Convert the baseline rise from cm to meters, then add the storm spike!
forecast_df['Total_Flood_Height_m'] = (forecast_df['RSL_Value_cm'] / 100) + storm_spike_m

# # 5. Build the final line chart
fig_forecast = px.line(
    forecast_df,
    x='RSL_Scenario_Year',
    y='Total_Flood_Height_m',
    title=f"⚠️ Future Crest Height of a {selected_metric} Event Under the {selected_scenario} Scenario",
    labels={'RSL_Scenario_Year': 'Year(RSL)', 'Total_Flood_Height_m': 'Total Crest Height (meters)'}
)

# Style it with a high-danger crimson color line
fig_forecast.update_traces(line_color='#A020F0', line_width=4)

# Force the horizontal axis ticks to format cleanly as simple year numbers
fig_forecast.update_layout(
    xaxis=dict(
        type='category'
    )
)

st.plotly_chart(fig_forecast, use_container_width=True)

# --- THE PUNCHLINE ---
st.markdown("### 🎯 Connecting the Pieces: The Big Picture")

# 1. Open the expander out in the open (not inside quotes!)
with st.expander("📖 Click here to learn how this graph combines both datasets"):
    # 2. Put the internal bullet points inside here
    st.markdown("""
    1. **The Line Graph** tells us: *"The normal, everyday sea level at this specific year will have permanently risen by this much."*
    2. **The Bar Graph** tells us: *"When a specific extreme water event (like a storm or king tide) hits us, the water level temporarily spikes by this much."*
    3. **The Combined Graph** tells us: *"During a specific storm event, if we take the relative sea level during that specific year, the crest height will be this high"*
    """)

# 3. Put the final concluding text below the expander
st.markdown("""
**The Ultimate Threat:** When you add a permanent baseline rise (the line graph) to a temporary storm spike (the bar graph), 
the water line pushes deep into the island. What used to be an manageable high-water event will eventually cause severe, 
regular flooding on Mokuoloe.
""")


