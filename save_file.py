import json
import os
import re

if not os.path.exists('outputs'):
    os.makedirs('outputs')

def save_explanations_on_json_file(explanations, json_file_name):
    """
    Saves the explanations to a JSON file.

    Args:
        explanations (list): List of explanations.
        json_file_name (str): Name of the output JSON file.
    """
    # Replace "uploads" with "output" using regular expressions
    new_file_path = re.sub(r"uploads\\", r"outputs\\", json_file_name)

    json.dump(explanations, open(new_file_path, "w"))
