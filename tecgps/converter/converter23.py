
import json
import glob

def convert_json_to_geojson(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    features = []
    
    for obj in data['timelineObjects']:
        if 'activitySegment' in obj:
            segment = obj['activitySegment']
            start = segment['startLocation']
            end = segment['endLocation']

            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [start['longitudeE7'] / 1e7, start['latitudeE7'] / 1e7],
                        [end['longitudeE7'] / 1e7, end['latitudeE7'] / 1e7]
                    ]
                },
                "properties": {
                    "startTimestamp": segment['duration']['startTimestamp'],
                    "endTimestamp": segment['duration']['endTimestamp'],
                    "activityType": segment['activityType']
                }
            }
            features.append(feature)

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    output_file_name = file_name.replace(".json", ".geojson")
    with open(output_file_name, 'w', encoding='utf-8') as f:
        json.dump(geojson, f, ensure_ascii=False, indent=4)
    
    print(f"Converted {file_name} to {output_file_name}")


def main():
    for file in glob.glob("2023*.json"):  # Aquí está el cambio
        convert_json_to_geojson(file)

if __name__ == "__main__":
    main()
