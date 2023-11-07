import os
import re
import csv

# Function to parse the text and return a dictionary with the required info
def parse_maneuver(text_block):
    # A dictionary to hold the parsed data
    parsed_data = {
        'name': '',
        'activation': '',
        'target': '',
        'area': '',
        'duration': '',
        'range': '',
        'savetype': '',
        'onsave': '',
        'school': '',
        'description': '',
        'level': ''
    }

    # Check if the text is NOT a stance
    if "(Stance)" not in text_block:
        # Extract the name of the maneuver
        parsed_data['name'] = text_block.split('\n')[0].strip()

 # Extract and simplify the activation action
        activation = re.search(r'Initiation Action: (.+)', text_block)
        if activation:
            parsed_data['activation'] = activation.group(1).replace('1 standard action', 'standard').replace('1 swift action', 'swift').replace('1 full round action', 'full').replace('1 immediate action', 'immediate')

        
        target = re.search(r'Target: (.+)', text_block)
        if target:
            parsed_data['target'] = target.group(1)

        area = re.search(r'Area: (.+)', text_block)
        if area:
            parsed_data['area'] = area.group(1)

        duration = re.search(r'Duration: (.+)', text_block)
        if duration:
            parsed_data['duration'] = duration.group(1)

        range = re.search(r'Range: (.+)', text_block)
        if range:
            parsed_data['range'] = range.group(1)

        parsed_data['level'] = re.search(r'Level: (.+)', text_block).group(1)

        save_match = re.search(r'Saving Throw: (.+)', text_block)
        if save_match:
            parsed_data['savetype'] = save_match.group(1).split()[0]  # Just the first word
            parsed_data['onsave'] = ' '.join(save_match.group(1).split()[1:])  # The rest

        discipline_match = re.search(r'Discipline: (.+)', text_block)
        if discipline_match:
            parsed_data['school'] = discipline_match.group(1)

        match = re.search(r'Duration:.*?\n(.*?)(?=^(?:[A-Z\s\']+)$|\Z)', text_block, re.DOTALL)
        if match:
            parsed_data['description'] = match.group(1).strip()

        return parsed_data
    else:
        return None

# Function to read a file, parse its content
def process_files(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            # Read the content of the input file
            with open(os.path.join(input_dir, filename), 'r', encoding='utf-8') as file:
                content = file.read()
                
                # Split the content into blocks based on titles
                # The pattern looks for titles in all caps possibly followed by more text
                # We split using lookahead and lookbehind to keep the delimiters
                blocks = re.findall(r'(?m)^(?:[A-Z\s\']+)$.*?(?=^(?:[A-Z\s\']+)$|\Z)', content.strip(), re.DOTALL)
                
                maneuver_dict = {}
                for block in blocks:
                    print(block)
                    maneuver = parse_maneuver(block)
                    if maneuver:
                        maneuver_dict[maneuver['name']] = maneuver

            # Write to CSV
            output_file = os.path.join(output_dir, f'maneuvers.csv')
            with open(output_file, 'a', newline='', encoding='utf-8') as csvfile:
                first_key = next(iter(maneuver_dict))
                writer = csv.DictWriter(csvfile, fieldnames=maneuver_dict[first_key].keys())
                # Only write header if the file is new
                if not os.path.isfile(output_file):
                    writer.writeheader()
                for key in maneuver_dict:
                    writer.writerow(maneuver_dict[key])

# Set your input and output directories here
input_directory = 'input'
output_directory = 'output'

process_files(input_directory, output_directory)

print("Processing complete.")
