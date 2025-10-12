import pandas as pd
from flask import Flask, jsonify, render_template
from datetime import datetime, timedelta
import pytz
import json

app = Flask(__name__)

# --- Main Page Route ---
@app.route("/")
def index():
    return render_template('index.html')

# --- API Routes for Data ---
@app.route("/animal-locations", methods=['GET'])
def get_animal_locations():
    try:
        df = pd.read_csv("animals_data.csv")
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values(by='timestamp')

        paths = {}
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
            paths[group_id] = path_data
        
        return jsonify({"success": True, "paths": paths})
    except Exception as e:
        print(f"Error in animal-locations: {str(e)}")
        return jsonify({"success": False, "error": str(e), "paths": {}}), 500

@app.route("/anomaly-chart-data")
def get_anomaly_chart_data():
    try:
        df = pd.read_csv("animals_data.csv")
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values(by='timestamp')
        
        # Get last 30 days of data
        utc_now = datetime.now(pytz.utc)
        thirty_days_ago = utc_now - timedelta(days=30)
        df_filtered = df[df['timestamp'] >= thirty_days_ago]
        
        # Group by date and get average anomaly score
        df_filtered['date'] = df_filtered['timestamp'].dt.date
        daily_scores = df_filtered.groupby('date')['anomaly_score'].mean().reset_index()
        
        labels = [d.strftime('%d %b') for d in daily_scores['date']]
        data = [int(score) for score in daily_scores['anomaly_score']]
        
        # Calculate average for the period
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
    try:
        df = pd.read_csv("animals_data.csv")
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Get last 7 days
        utc_now = datetime.now(pytz.utc)
        seven_days_ago = utc_now - timedelta(days=7)
        df_filtered = df[df['timestamp'] >= seven_days_ago]
        
        # Group by date and count reports
        df_filtered['date'] = df_filtered['timestamp'].dt.date
        daily_counts = df_filtered.groupby('date').size().reset_index(name='count')
        
        labels = [d.strftime('%a') for d in daily_counts['date']]
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
    try:
        df = pd.read_csv("disasters.csv")
        disasters = []
        for _, row in df.iterrows():
            disasters.append({
                "type": row['disaster_type'],
                "region": row['region'],
                "date": row['date'],
                "icon": row['icon']
            })
        return jsonify({"success": True, "disasters": disasters})
    except Exception as e:
        print(f"Error in natural-disasters: {str(e)}")
        return jsonify({"success": False, "disasters": []})

# --- Run the App ---
if __name__ == "__main__":
    app.run(debug=True, port=5002)