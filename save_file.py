import json

def save_explanations_on_json_file(explanations, json_file_name):
    """
    Saves the explanations to a JSON file.

    Args:
        explanations (list): List of explanations.
        json_file_name (str): Name of the output JSON file.
    """
    json.dump(explanations, open(json_file_name, "w"))
