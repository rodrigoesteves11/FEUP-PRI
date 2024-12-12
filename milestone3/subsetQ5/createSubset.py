import json
import random

# Function to filter and include random keys from a JSON file
def filter_and_add_random_keys(file_path, keys_file_path, output_path):
    try:
        # Read the JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Ensure data is a list
        if not isinstance(data, list):
            raise ValueError("Invalid JSON structure. Expected a list of dictionaries.")

        # Read the keys from the keys file
        with open(keys_file_path, 'r') as keys_file:
            search_keys = [line.strip() for line in keys_file.readlines()]

        # Filter data to keep only matching keys
        filtered_data = [item for item in data if item['id'] in search_keys]

        # Add 10 random keys from the original data
        additional_keys = random.sample(data, min(10, len(data)))
        filtered_data.extend([key for key in additional_keys if key not in filtered_data])

        # Write the output to a new file
        with open(output_path, 'w') as outfile:
            json.dump(filtered_data, outfile, indent=4)

        print(f"Filtered data saved to {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Input and output file paths
input_file = 'transformed_species_data.json'  # Replace with your input file path
keys_file = 'sample.txt'  # Replace with your keys file path
output_file = 'subsetq5.json'  # Replace with your desired output file path

# Run the function
filter_and_add_random_keys(input_file, keys_file, output_file)
