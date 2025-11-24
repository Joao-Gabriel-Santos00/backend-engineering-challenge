# Backend Engineering Challenge (Delivery Time CLI)


The objective of this project is to build a simple command line application that parses a stream of events and produces an aggregated output. This is a forked repo from [backend engineering challenge](https://github.com/Unbabel/backend-engineering-challenge). Please visit the original challenge if you would like to know more!

## Prerequisites
+   Python 3.7 or higher.
+   No external libraries are required (The project relies entirely on the Python Standard Library).

## Installation

This project uses a `setup.py` configuration. Install it in "editable" mode to generate the `delivery_time_cli` command. After cloning this repo and installing Python, you can run the following command:

```
pip install -e .
```

## Running

Once installed, you can run the application directly from your terminal.


**Syntax:**
```
delivery_time_cli --input_file <path_to_input_file> --window_size <minutes>
```

**Example:**
```
delivery_time_cli --input_file events.json --window_size 10
```

If for some reason you cant install the application, you can simply use python:
```
python -m src.main --input_file events.json --window_size 10
```


## Challenge Considerations

In response to the challenge notes regarding optimizations and considerations, here is a breakdown of the choices and decisions I made during this project.

### Initial Idea

My initial approach was to implement a direct aggregation for every minute. For every minute X, iterate backwards through the entire history of events to find those that fall within the range [X - Window, X]. Calculate the sum and count, then output the average. The optimization problem: This results in massive redundancy. If the window size is 10 minutes, the same event is read and calculated 10 times (once for each minute it stays valid).

### Final Solution

To optimize this, I used a queue and a current_sum variable rather than a static query. This was only done because of the order of the input lines, since the input is ordered from lower to higher values by the timestamp key. So as times moves forward, new events are added to the right of the queue and added to the current_sum. At the same time, events that are older than the window size are popped from the left of the queue and subtracted fro mthe current_sum. This makes it so we never re-iterate over the same value, making the solution much more efficient specially for large input files.

### Application Termination

The most important consideration of this project was to decide where to terminate the application. Since the input is a static file, I decided that the solution should stop on the minute right after the last event, to match the example output. But if this application was consuming from a source that is constantly updating the input file, I would need to change the following loop:

	```
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
	```

To make the change to an infinite source environment, the loop would run while True, removing the stream_finished condition. So even if it doesnt find another row in the input file for the respective window_size, it would still keep running and wait for the next line to appear. Instead of jumping time based on event timestamps, the application could also use the system clock to know what the current time is and fetch the input file for the last X minutes.  

### Tests

I built some tests that helped me make sure that the solution works for a few specific cases:

+ Verifies the output matches the challenge's example logic exactly (starting at the first minute, ending at the last event + 1 minute)
+ Verified behavior with empty files and files containing single events
+ Tests the full process_stream pipeline using temporary files.
+ Ensures the queue correctly removes events older than the window_size

To run the tests:

```
python -m unittest discover tests
```

If you want to run other tests, you can change the input_file file (events.json). 