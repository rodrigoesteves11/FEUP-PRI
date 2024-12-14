import sys

def process_files(file1, file2):
    """
    Processes two files and updates the numbers in the first file based on matches.

    Args:
        file1 (str): Path to the first input file (to be updated).
        file2 (str): Path to the second input file (reference for matching).
    """
    # Read the second file into a set for fast lookup
    with open(file2, 'r') as f2:
        values_to_check = set(line.strip() for line in f2)

    # Read and process the first file
    with open(file1, 'r') as f1:
        lines = f1.readlines()

    # Update the first file with the modified data
    with open(file1, 'w') as f1:
        for line in lines:
            parts = line.strip().split()
            if len(parts) == 4:  # Ensure the line is correctly formatted
                name = parts[2]
                if name in values_to_check:
                    parts[3] = '1'
                else:
                    parts[3] = '0'
                f1.write(' '.join(parts) + '\n')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 code.py <file1> <file2>")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]
    process_files(file1, file2)