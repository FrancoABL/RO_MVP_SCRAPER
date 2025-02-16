import pandas as pd
from datetime import datetime, timedelta
import json

# Load the MVP kills data
mvp_kills = pd.read_csv('mvp_names.csv')

# Load the spawn time dictionary from dic.json
with open('dic.json', 'r') as f:
    boss_data = json.load(f)

def calculate_spawn_time(row):
    mvp_name = row['MVP Name']
    death_time = datetime.strptime(row['MVP Time'], '%Y-%m-%d %H:%M:%S')
    map_name = row['MVP MAP']
    
    print(f"Calculating spawn time for {mvp_name} on map {map_name} at {death_time}")
    
    # Check if MVP exists in boss_data
    if mvp_name not in boss_data:
        print(f"MVP {mvp_name} not found in boss_data")
        return None
    
    # Find the correct spawn time for the map
    spawn_data = boss_data[mvp_name]
    map_index = -1
    
    try:
        map_index = spawn_data['maps'].index(map_name)
    except ValueError:
        # If map not found, try to use the first spawn time
        map_index = 0
    
    if map_index >= 0:
        spawn_minutes = spawn_data['spawn_times'][map_index]
        spawn_time = death_time + timedelta(minutes=spawn_minutes)
        print(f"Spawn time for {mvp_name} on map {map_name} is {spawn_time}")
        return spawn_time
    
    print(f"Map {map_name} not found for MVP {mvp_name}")
    return None

def format_time_until(spawn_time):
    if spawn_time is None:
        return "Unknown"
    
    now = datetime.now()
    if spawn_time < now:
        return "Already spawned"
    
    time_left = spawn_time - now
    hours = time_left.seconds // 3600
    minutes = (time_left.seconds % 3600) // 60
    return f"{hours}h {minutes}m"

# Calculate spawn times and create a new dataframe with the results
results = []
current_time = datetime.now()

for _, row in mvp_kills.iterrows():
    spawn_time = calculate_spawn_time(row)
    
    result = {
        'MVP Name': row['MVP Name'],
        'Map': row['MVP MAP'],
        'Last Death': row['MVP Time'],
        'Next Spawn': spawn_time.strftime('%Y-%m-%d %H:%M:%S') if spawn_time else 'Unknown',
        'Time Until Spawn': format_time_until(spawn_time)
    }
    results.append(result)

# Create and sort the results dataframe
spawn_times_df = pd.DataFrame(results)
spawn_times_df = spawn_times_df.sort_values(by='Next Spawn')

# Print the results
print("\nMVP Spawn Times:")
print("=" * 100)
for _, row in spawn_times_df.iterrows():
    print(f"{row['MVP Name']:<20} {row['Map']:<15} Next Spawn: {row['Next Spawn']} ({row['Time Until Spawn']})")