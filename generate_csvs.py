import pandas as pd
from datetime import datetime, timedelta
import random

# Generate animals_data.csv with recent dates
print("Creating animals_data.csv...")

# Base location (Bengaluru area)
base_lat = 12.91
base_lon = 77.30

animals_data = []
current_time = datetime.now()

# Cow Herd 1 - 15 data points over last 30 days
for i in range(15):
    days_ago = random.randint(0, 30)
    timestamp = current_time - timedelta(days=days_ago, hours=random.randint(0, 23))
    animals_data.append({
        'group_id': 'cow_herd_1',
        'timestamp': timestamp.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'animal_type': 'Cow Herd',
        'lat': base_lat + random.uniform(-0.02, 0.02),
        'lon': base_lon + random.uniform(-0.02, 0.02),
        'behaviour_description': random.choice([
            'Grazing peacefully',
            'Near water source',
            'Resting under trees',
            'Moving to pasture',
            'Grouped together'
        ]),
        'anomaly_score': random.randint(5, 30)
    })

# Sheep Flock 1 - 12 data points
for i in range(12):
    days_ago = random.randint(0, 30)
    timestamp = current_time - timedelta(days=days_ago, hours=random.randint(0, 23))
    animals_data.append({
        'group_id': 'sheep_flock_1',
        'timestamp': timestamp.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'animal_type': 'Sheep Flock',
        'lat': base_lat + 0.01 + random.uniform(-0.015, 0.015),
        'lon': base_lon + 0.015 + random.uniform(-0.015, 0.015),
        'behaviour_description': random.choice([
            'Grazing on hillside',
            'Huddled together',
            'Following shepherd',
            'Near village boundary',
            'Scattered formation'
        ]),
        'anomaly_score': random.randint(10, 50)
    })

# Dog 1 - 10 data points with some high anomaly scores
for i in range(10):
    days_ago = random.randint(0, 25)
    timestamp = current_time - timedelta(days=days_ago, hours=random.randint(0, 23))
    animals_data.append({
        'group_id': 'dog_1',
        'timestamp': timestamp.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'animal_type': 'Dog',
        'lat': base_lat - 0.005 + random.uniform(-0.01, 0.01),
        'lon': base_lon + 0.008 + random.uniform(-0.01, 0.01),
        'behaviour_description': random.choice([
            'Roaming near village',
            'Barking continuously',
            'Restless behavior',
            'Searching for food',
            'Alert posture'
        ]),
        'anomaly_score': random.randint(5, 85)
    })

# Deer Group - 8 data points
for i in range(8):
    days_ago = random.randint(0, 30)
    timestamp = current_time - timedelta(days=days_ago, hours=random.randint(0, 23))
    animals_data.append({
        'group_id': 'deer_1',
        'timestamp': timestamp.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'animal_type': 'Deer',
        'lat': base_lat - 0.01 + random.uniform(-0.02, 0.02),
        'lon': base_lon - 0.02 + random.uniform(-0.02, 0.02),
        'behaviour_description': random.choice([
            'Spotted at forest edge',
            'Moving towards hills',
            'Drinking from stream',
            'Alert and watchful',
            'Rapid movement detected'
        ]),
        'anomaly_score': random.randint(15, 60)
    })

# Elephant Herd - 6 data points with higher anomaly
for i in range(6):
    days_ago = random.randint(0, 20)
    timestamp = current_time - timedelta(days=days_ago, hours=random.randint(0, 23))
    animals_data.append({
        'group_id': 'elephant_herd_1',
        'timestamp': timestamp.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'animal_type': 'Elephant Herd',
        'lat': base_lat + 0.02 + random.uniform(-0.015, 0.015),
        'lon': base_lon - 0.015 + random.uniform(-0.015, 0.015),
        'behaviour_description': random.choice([
            'Moving through forest',
            'Near agricultural land',
            'Trumpet calls heard',
            'Large group spotted',
            'Crossing main road'
        ]),
        'anomaly_score': random.randint(40, 90)
    })

df_animals = pd.DataFrame(animals_data)
df_animals = df_animals.sort_values('timestamp')
df_animals.to_csv('animals_data.csv', index=False)
print(f"✅ Created animals_data.csv with {len(animals_data)} records")
print(f"   Date range: {df_animals['timestamp'].min()} to {df_animals['timestamp'].max()}")

# Generate disasters.csv with recent dates
print("\nCreating disasters.csv...")

disasters = [
    {
        'disaster_type': 'Earthquake',
        'region': 'Region A',
        'date': (current_time - timedelta(days=30)).strftime('%d %b %Y'),
        'icon': 'zap'
    },
    {
        'disaster_type': 'Tsunami Warning',
        'region': 'Region B',
        'date': (current_time - timedelta(days=45)).strftime('%d %b %Y'),
        'icon': 'wind'
    },
    {
        'disaster_type': 'Wildfire',
        'region': 'Region C',
        'date': (current_time - timedelta(days=60)).strftime('%d %b %Y'),
        'icon': 'cloud-lightning'
    },
    {
        'disaster_type': 'Flooding',
        'region': 'Region D',
        'date': (current_time - timedelta(days=75)).strftime('%d %b %Y'),
        'icon': 'umbrella'
    },
    {
        'disaster_type': 'Landslide',
        'region': 'Region E',
        'date': (current_time - timedelta(days=90)).strftime('%d %b %Y'),
        'icon': 'alert-triangle'
    }
]

df_disasters = pd.DataFrame(disasters)
df_disasters.to_csv('disasters.csv', index=False)
print(f"✅ Created disasters.csv with {len(disasters)} records")

# Optional: Create animals.csv (current snapshot)
print("\nCreating animals.csv (optional - for current animal status)...")

animals_current = [
    {'lat': 12.9716, 'lon': 77.5946, 'animal_type': 'Elephant Herd', 'status': 'Normal activity'},
    {'lat': 13.0, 'lon': 77.5, 'animal_type': 'Deer Pack', 'status': 'Agitated - Moving North'},
    {'lat': 12.9, 'lon': 77.65, 'animal_type': 'Bird Swarm', 'status': 'Unusual flocking pattern'},
    {'lat': 12.85, 'lon': 77.55, 'animal_type': 'Wild Boars', 'status': 'Spotted near water source'}
]

df_animals_current = pd.DataFrame(animals_current)
df_animals_current.to_csv('animals.csv', index=False)
print(f"✅ Created animals.csv with {len(animals_current)} records")

print("\n" + "="*50)
print("All CSV files created successfully!")
print("="*50)
print("\nTo use these files:")
print("1. Run this script: python generate_csvs.py")
print("2. Make sure the CSV files are in the same directory as app.py")
print("3. Start your Flask app: python app.py")
print("4. Open http://localhost:5002 in your browser")