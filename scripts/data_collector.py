import json
import glob

# Get all JSON files in the current directory (or specify the path)
json_files = glob.glob("merged_data/*.json")

merged_data = []

# Read and merge all JSON files
for file in json_files:
    with open(file, "r") as f:
        data = json.load(f)
        merged_data.extend(data)  # Append the data from each file

# Save merged data into a new JSON file
with open("master_data.json", "w") as f:
    json.dump(merged_data, f, indent=4)
