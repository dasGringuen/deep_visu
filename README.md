# deep_visu
Visualization and experiments framework for training Deep learning and Machine learning algorithms.

Help to keep track of experiments by saving the results and configurations on single html file.

## Features

*   Visualization for real time signals
*   Written in Python 3
*   Based on Bokeh

## Requirements

* Python 3
* Bokeh

## Use

-   Run bokeh in a separated terminal

```
~$ bokeh serve
```

-   Run the Python script

```
~$ python3 example_signals.py
```

## How to use it in Python script

```
# Import the plot
from LogPlotBokeh import LogPlot

# Create an instance
log = LogPlot(name="Title",
        properties=["Reward", "Avr_Reward"],
        properties_telemetry=["speedX", "steer"],
        output_path="."
        )

# Feed data to both plots and the text log
episode_progres = {"Reward":10, "Avr_Reward":20}
log.progress.add(x=i, y=episode_progres)

# telemetry
telemetry = {"speedX":10, "accel":20}
log.telemetry.add(x=i, y=telemetry)

# Add some text to the log
log.terminal("Model  parameters %d" % i)

# Close
log.close()
```



## Todos

-   Improve performance
-   Remove the use of Bokeh client

## License

-   GPL v3

**Free Software**

