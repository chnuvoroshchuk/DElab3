import glob
import json
import csv
import os


def flatten_json(json_data, prefix=''):
    flattened = {}
    for key, value in json_data.items():
        if isinstance(value, dict):
            flattened.update(flatten_json(value, prefix + key + '_'))
        else:
            flattened[prefix + key] = value
    return flattened


def convert_to_csv(json_file, csv_dir):
    with open(json_file, 'r') as json_file_obj:
        data = json.load(json_file_obj)
        flattened_data = flatten_json(data)

        csv_file_path = os.path.join(csv_dir, os.path.splitext(os.path.basename(json_file))[0] + '.csv')

        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=flattened_data.keys())
            writer.writeheader()
            writer.writerow(flattened_data)


def process_json_files():
    json_files = glob.glob('data/**/*.json', recursive=True)
    csv_dir = 'csv'

    # Create csv directory if it doesn't exist
    if not os.path.exists(csv_dir):
        os.makedirs(csv_dir)

    for json_file in json_files:
        convert_to_csv(json_file, csv_dir)
        print(f'Converted {json_file} to {csv_dir}')


if __name__ == "__main__":
    process_json_files()
