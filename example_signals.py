from random import random
import numpy as np
from numpy import pi
import time

from LogPlotBokeh import LogPlot

def get_sin(f=5):
    import numpy as np
    Fs = 8000
    sample = 8000
    x = np.arange(sample)
    y = np.sin(2 * np.pi * f * x / Fs)
    return x,y

def main():
    try:
        name = "bo1"
        log = LogPlot(name=name,
                properties=["Reward", "Avr_Reward", "Dist_raced", "Best_lap", 'Loss', "Damage", 'epsilon'],
                properties_telemetry=["speedX", "steer", "accel", "brake", "trackPos", "damage", "angle"],
                output_path="."
                )

        # some time to load the browser
        time.sleep(5)

        for i in range(1000):
            x, y = i, i + random()

            if (i % 50) is 0:
                episode_progres = {"Reward":y*2, "Avr_Reward":y*3,
                                "Dist_raced":y*5, "Best_lap":np.sin(2 * np.pi * 5 * x / 200), "Loss":np.sin(2 * np.pi * 5 * x / 100),
                                "Damage":np.sin(2 * np.pi * 5 * x / 100), "epsilon":np.sin(21 * np.pi * 5 * x / 100)}
                log.progress.add(x=i, y=episode_progres)

            telemetry = {"speedX":np.sin(2 * np.pi * 5 * x / 100), "steer":10,
                        "accel":20, "brake":30, "trackPos":40, "damage":50, "angle":60}
            log.telemetry.add(x=i, y=telemetry)

            if (i % 5) is 0:
                log.terminal("Model  parameters %d" % i)

            time.sleep(0.05)

        log.close()
    except KeyboardInterrupt:
        log.session.close()
        print('Got Keyboard interrupt')
    finally:
        print("Finish.")

if __name__ == "__main__":
    main()
