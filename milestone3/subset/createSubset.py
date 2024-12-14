import json

# Function to filter data based only on specified keys
def filter_keys(file_path, keys_file_path, output_path):
    try:
        # Read the JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Ensure data is a list
        if not isinstance(data, list):
            raise ValueError("Invalid JSON structure. Expected a list of dictionaries.")

        # Read the keys from the keys file
        with open(keys_file_path, 'r') as keys_file:
            search_keys = {line.strip() for line in keys_file.readlines()}  # Use a set for faster lookup

        # Filter data to keep only matching keys
        filtered_data = [item for item in data if item['id'] in search_keys]

        # Write the filtered output to a new file
        with open(output_path, 'w') as outfile:
            json.dump(filtered_data, outfile, indent=4)

        print(f"Filtered data saved to {output_path} with {len(filtered_data)} entries.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Input and output file paths
input_file = 'transformed_species_data.json'  # Replace with your input file path
keys_file = 'values.txt'  # Replace with your keys file path
output_file = 'subset.json'  # Replace with your desired output file path

# Run the function
filter_keys(input_file, keys_file, output_file)
