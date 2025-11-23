import json
from datetime import datetime, timedelta
from parser import parse_events
from window import SlidingWindow

def floor_minute(t: datetime) -> datetime:
    """Rounds a datetime down to the nearest minute."""
    return t.replace(second=0, microsecond=0)

def process_stream(input_file: str, window_size: int):
    """
    Main loop:
    1. Reads events from the file stream.
    2. Moves time forward minute-by-minute.
    3. Prints the moving average for each minute.
    """
    
    # 1. Initialize the components
    window = SlidingWindow(window_size)
    event_stream = parse_events(input_file)
    
    # 2. Get the first event to set the start time
    try:
        next_event = next(event_stream)
    except StopIteration:
        # File is empty
        return

    # Start the clock at the minute of the first event
    current_time = floor_minute(next_event["timestamp"])
    
    # Stop the clock at the minute right after the last event
    last_event_time = next_event["timestamp"]
    
    # We loop until we run out of events. 
    stream_finished = False
    
    while not stream_finished or current_time <= floor_minute(last_event_time) + timedelta(minutes=1):
        
        # Output logic:
        output_data = {
            "date": str(current_time),
            "average_delivery_time": window.get_average()
        }
        
        # Print valid JSON to stdout
        print(json.dumps(output_data))
        
        # Optimization: Move time forward by 1 minute
        current_time += timedelta(minutes=1)
        
        # Remove old events that are now outside the window
        window.prune(current_time)
        
        # Add new events that happened BEFORE this new current_time
        while next_event and next_event["timestamp"] < current_time:
            # Update the last event tracker
            last_event_time = next_event["timestamp"]
            
            window.add_event(next_event["timestamp"], next_event["duration"])
            
            try:
                next_event = next(event_stream)
            except StopIteration:
                next_event = None
                stream_finished = True
                break