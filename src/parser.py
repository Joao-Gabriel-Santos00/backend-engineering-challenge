import json
from datetime import datetime
from typing import Iterator, Dict, Any

def parse_events(file_path: str) -> Iterator[Dict[str, Any]]:
    """
    Reads a JSON file line by line and yields parsed events.
    
    Args:
        file_path: Path to the input file.
        
    Yields:
        A dictionary containing the event data with the 'timestamp'
        converted to a datetime object.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                try:
                    data = json.loads(line)
                    
                    if "timestamp" in data:
                        data["timestamp"] = datetime.strptime(data["timestamp"], "%Y-%m-%d %H:%M:%S.%f")
                    
                    yield data
                    
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        raise