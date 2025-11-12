import pandas as pd
from flask import Flask, jsonify, render_template
from datetime import datetime, timedelta
import pytz
import json
import os  # <-- Import the OS module

app = Flask(__name__)

# ===================================================================
# 🧠 MAKESHIFT DEMO - DATA LOADER
# ===================================================================

# This will hold all our "replayed" data
# It's a dictionary where:
# key = group_id (e.g., 'farm_cow_1')
# value = a list of all data points (as dicts) for that animal
REPLAY_DATA = {}

# This is a "global" counter to track our position in the replay
REPLAY_STEP_COUNTER = 0
REPLAY_MAX_STEPS = 0

def load_replay_data():
    """
    Loads animals_data.csv into memory on startup
    and prepares it for the replay simulation.
    """
    global REPLAY_DATA, REPLAY_MAX_STEPS
    
    # --- NEW LOGS ---
    print("="*50)
    print(f"--- [LOG] CURRENT WORKING DIRECTORY: {os.getcwd()}")
    print("--- [LOG] Server is looking for files in this folder.")
    print("="*50)
    # --- END LOGS ---

    print("🧠 Loading simulation data from animals_data.csv for demo...")
    animal_file_path = os.path.abspath("animals_data.csv")
    print(f"--- [LOG] Trying to read: {animal_file_path} ---")

    try:
        # This will now load your 120-entry CSV
        df = pd.read_csv("animals_data.csv")
        # CRITICAL FIX for the error you had before
        df['timestamp'] = pd.to_datetime(df['timestamp'], format='mixed')
        # Sort by timestamp to make the replay chronological
        df = df.sort_values(by='timestamp')

        # Group by animal
        for group_id, group_df in df.groupby('group_id'):
            path_data = []
            for _, row in group_df.iterrows():
                path_data.append({
                    "lat": float(row['lat']),
                    "lon": float(row['lon']),
                    "timestamp": row['timestamp'].strftime('%d %b %H:%M'),
                    "animal_type": row['animal_type'],
                    "behaviour": row['behaviour_description'],
                    "anomaly_score": int(row['anomaly_score'])
                })
            REPLAY_DATA[group_id] = path_data
            # print(f"   ...Loaded {len(path_data)} points for {group_id}") # Commented out for cleaner logs
        
        # Find the length of the *shortest* path to use as our max step
        if REPLAY_DATA:
            # All paths have 30 steps in the new data
            REPLAY_MAX_STEPS = min(len(path) for path in REPLAY_DATA.values())
            print(f"✅ Simulation ready. Max steps: {REPLAY_MAX_STEPS}")
        
    except Exception as e:
        print(f"--- [LOG] ❌ FAILED to read animals_data.csv ---")
        print(f"--- [LOG] Error details: {str(e)} ---")


# ===================================================================
# 💻 API ROUTES
# ===================================================================

# --- Main Page Route ---
@app.route("/")
def index():
    print("--- [LOG] Received request for / (index.html) ---")
    # This just shows your webpage
    return render_template('index.html')

# --- NEW API: Live Simulation Replay Route ---
@app.route("/get-live-update", methods=['GET'])
def get_live_update():
    """
    This is our "fake" live feed. Each time it's called,
    it returns the *next* data point for all animals.
    """
    global REPLAY_STEP_COUNTER
    
    current_points = {}
    
    if not REPLAY_DATA or REPLAY_MAX_STEPS == 0:
        return jsonify({"success": False, "error": "Data not loaded"}), 500

    # Get the data point for the current step for each animal
    for group_id, path in REPLAY_DATA.items():
        if REPLAY_STEP_COUNTER < len(path):
            current_points[group_id] = path[REPLAY_STEP_COUNTER]
    
    # Move to the next step
    REPLAY_STEP_COUNTER += 1
    
    # If we reach the end, loop back to the start for a continuous demo
    if REPLAY_STEP_COUNTER >= REPLAY_MAX_STEPS:
        REPLAY_STEP_COUNTER = 0
        
    return jsonify({"success": True, "points": current_points})


# --- Your OLD API Routes ---
# We keep these so your charts on the page still work
# They will just show the full historical data

@app.route("/animal-locations", methods=['GET'])
def get_animal_locations():
    # This now just returns the *full* paths for historical view
    # This is for any part of your original code that might still use it
    try:
        paths = {}
        for group_id, path_data in REPLAY_DATA.items():
            paths[group_id] = path_data
        return jsonify({"success": True, "paths": paths})
    except Exception as e:
        return jsonify({"success": False, "error": str(e), "paths": {}}), 500

@app.route("/anomaly-chart-data")
def get_anomaly_chart_data():
    # This route is unchanged and reads from the CSV
    try:
        df = pd.read_csv("animals_data.csv")
        df['timestamp'] = pd.to_datetime(df['timestamp'], format='mixed')
        df = df.sort_values(by='timestamp')
        
        # Use a wide date range to ensure our new demo data is included
        thirty_days_ago = datetime.now(pytz.utc) - timedelta(days=90)
        df_filtered = df[df['timestamp'] >= thirty_days_ago]
        
        df_filtered['date'] = df_filtered['timestamp'].dt.date
        daily_scores = df_filtered.groupby('date')['anomaly_score'].mean().reset_index()
        
        labels = [d.strftime('%d %b') for d in daily_scores['date']]
        data = [int(score) for score in daily_scores['anomaly_score']]
        
        avg_score = int(df_filtered['anomaly_score'].mean()) if not df_filtered.empty else 0
        
        return jsonify({
            "labels": labels,
            "data": data,
            "average": avg_score
        })
    except Exception as e:
        print(f"Error in anomaly-chart-data: {str(e)}")
        return jsonify({"labels": [], "data": [], "average": 0})

@app.route("/behaviour-chart-data")
def get_behaviour_chart_data():
    # This route is unchanged and reads from the CSV
    try:
        df = pd.read_csv("animals_data.csv")
        df['timestamp'] = pd.to_datetime(df['timestamp'], format='mixed')
        
        # Use a wide date range
        seven_days_ago = datetime.now(pytz.utc) - timedelta(days=90)
        df_filtered = df[df['timestamp'] >= seven_days_ago]
        
        df_filtered['date'] = df_filtered['timestamp'].dt.date
        daily_counts = df_filtered.groupby('date').size().reset_index(name='count')
        
        labels = [d.strftime('%a, %d %b') for d in daily_counts['date']]
        data = daily_counts['count'].tolist()
        
        total_reports = len(df_filtered)
        
        return jsonify({
            "labels": labels,
            "data": data,
            "total": total_reports
        })
    except Exception as e:
        print(f"Error in behaviour-chart-data: {str(e)}")
        return jsonify({"labels": [], "data": [], "total": 0})

@app.route("/natural-disasters")
def get_natural_disasters():
    
    # --- NEW LOGS ---
    print("\n--- [LOG] Received request for /natural-disasters ---")
    disaster_file_path = os.path.abspath("disasters.csv")
    print(f"--- [LOG] Trying to read: {disaster_file_path} ---")
    # --- END LOGS ---
    
    try:
        df = pd.read_csv("disasters.csv")
        disasters = []
        for _, row in df.iterrows():
            disasters.append({
                "type": row['disaster_type'],
                "region": row['region'],
                "date": row['date'], # Use the date string from the new CSV
                "icon": row['icon']
            })
        
        # --- NEW LOGS ---
        print(f"--- [LOG] Success! Found {len(disasters)} disasters. ---")
        # --- END LOGS ---
        return jsonify({"success": True, "disasters": disasters})
    
    except Exception as e:
        # --- NEW LOGS ---
        print(f"--- [LOG] ❌ FAILED to read disasters.csv ---")
        print(f"--- [LOG] Error details: {str(e)} ---")
        # --- END LOGS ---
        return jsonify({"success": False, "disasters": []})

# --- Run the App ---
if __name__ == "__main__":
    load_replay_data()  # Load the data *before* starting the app
    app.run(debug=True, port=5006)