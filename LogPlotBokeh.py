from functools import partial
from threading import Thread
import math
from queue import Queue
from bokeh.client import push_session
from bokeh.driving import cosine
from bokeh.plotting import figure, curdoc, reset_output, save, output_file
from bokeh.layouts import layout
from bokeh.models.widgets import Panel, Tabs, Button, PreText
from bokeh.models import ColumnDataSource
from bokeh.plotting import curdoc, figure, gridplot
from bokeh.layouts import column, row
from tornado import gen

from misc import get_date_time_string

window_width = 1200

class LinkedPlot(object):
    """ draw back, slower the reset button
        must add values to all the channels at once
    """
    def __init__(self, mainPlot, names, plot_width=window_width, plot_height=120, name="name", enabled=True):
        self.mainPlot = mainPlot
        self.names = names
        self.enabled = enabled
        TOOLS = 'wheel_zoom,pan,box_zoom,undo,hover,reset,hover'

        data = {'time': [0]}
        for i in self.names:
            data[i] = [0]
        source = ColumnDataSource(data=data)

        first_signal = True
        signals = []
        for i in self.names:
            if first_signal:
                first_signal = False
                s1 = figure(plot_width=plot_width, plot_height=plot_height, tools=TOOLS, title=i)
            else:
                s1 = figure(plot_width=plot_width, plot_height=plot_height, x_range=s1.x_range, tools=TOOLS, title=i) 
            s1.line("time", i, source=source, line_width=2, color="navy", alpha=0.5)
            signals.append(s1)

        self.widget = gridplot(signals, ncols=1)
        self._source = source

    @property
    def source(self):
        return self._source

    def _add(self, x, y):
        data = {'time': [x]}
        for i,j in zip(self.names, y):
            _v = y[i]
            if math.isnan(_v):
                _v = 0.
            data[i] = [_v]
        source = ColumnDataSource(data=data)
        self.source.stream(data)

    def _clear(self):
        data = {'time': [0]}
        for i in self.names:
            data[i] = [0]
        self.source.data.update(ColumnDataSource(data=data).data)

    # Interfaces
    def add(self, x, y):
        if self.enabled:
            self.mainPlot.event_stack.put((self._add, x, y))

    def clear(self):
        self.mainPlot.event_stack.put((self._clear,))

class MyPlot(object):
    def __init__(self, mainPlot, name="name", plot_width=window_width, plot_height=120):
        TOOLS = 'wheel_zoom,pan,box_zoom,box_select,resize,reset'
        self.mainPlot = mainPlot
        self._source = ColumnDataSource(data=dict(x=[0], y=[0]))
        self.s1 = figure(plot_width=plot_width, plot_height=plot_height, title=name, tools=TOOLS, toolbar_location="above")
        self.s1.line(x='x', y='y', source=self._source)

    @property
    def source(self):
        return self._source
    @property
    def plot(self):
        return self.s1

    def new_line(self, color="navy"):
        self.source_clone = ColumnDataSource(data=self._source.data)
        self.s1.line(x='x2', y='y2', source=self.source_clone, color=color)

    def _add(self, x, y):
        self.source.stream(dict(x=[x], y=[y]))

    def add(self, x, y):
        if math.isnan(x):
            x = 0.00
        if math.isnan(y):
            y = 0.00
        self.mainPlot.event_stack.put((self._add, x, y))

    def _line(self, x, y):
        src = ColumnDataSource(data=dict(x=x, y=y))
        self.source.data.update(src.data)  # use stream to add data overlay

    def line(self, x, y):
        self.mainPlot.event_stack.put((self._line, x, y))

    def _clear(self):
        src = ColumnDataSource(data=dict(x=[0], y=[0]))
        self._source.data.update(src.data)

    def clear(self):
        self.mainPlot.event_stack.put((self._clear,))

class LogPlot(object):
    """docstring for Log"""
    def __init__(self, name="name", properties=[], properties_telemetry=[], output_path=None):
        self.N = 10
        self.antialias = 10
        self.name = name
        self.output_path = output_path
        reset_output()
        self.event_stack = Queue()

        # open a session to keep our local document in sync with server
        # TODO pass session_id = name to give a name -> doen't work propelry
        # the zoom gets broken
        self.session = push_session(curdoc())

        # This is important! Save curdoc() to make sure all threads
        # see then same document.
        curdoc().title = name
        curdoc().session_id = name
        output_file(name + ".html")
        self.doc = curdoc()

        self.progress = LinkedPlot(mainPlot=self, names=properties, plot_width=window_width, plot_height=110)
        self.disp_text = """
                         Terminal:

                         """

        # need tabs? othewise scretch
        if 1:
            # tab1
            c = column([self.progress.widget])
            tab1 = Panel(child=c, title="Training progress")

            # tab2
            # button
            self.button = Button(label="Enable", button_type="success")
            self.button.on_click(self.button_click_handler)
            self.button_save = Button(label="Save", button_type="success")
            self.button_save.on_click(self.button_save_click_handler)
            # label
            self.pre = PreText(text=self.disp_text, width=window_width, height=300)
            tab2_c = column([self.pre])
            tab2 = Panel(child=tab2_c, title="Dash board")

            # tab4 testing linked plots
            self.telemetry = LinkedPlot(mainPlot=self, names=properties_telemetry, plot_width=window_width, plot_height=110, enabled=True)
            telemetry_tab = Panel(child=column([row([self.button, self.button_save]), self.telemetry.widget]), title="Live Telemetry")

            tabs = [ telemetry_tab,
                     tab1,
                     tab2
                     ]
            self.tabs = Tabs(tabs=tabs)
            self.layout = self.tabs
        else:
            c = column([i.plot for i in self.plots], sizing_mode='scale_width')
            self.layout = c

        self.step = 0
        thread = Thread(target=self.show)
        thread.start()

    def save(self):
        if self.output_path is not None:
            o = self.output_path + "/" + self.name + "_" + get_date_time_string() + ".html"
            save(self.tabs, o)
            print("# Plot saved to:", o)

    def close(self):
        self.save()
        time.sleep(0.5)
        self.session.close()
        time.sleep(0.5)

    def show(self):
        self.doc.add_periodic_callback(self.update, 200)
        self.doc.add_root(self.layout)
        self.session.show(self.layout) # open the document in a browser
        self.session.loop_until_closed() # run forever

    @gen.coroutine
    def update(self):
        while not self.event_stack.empty():
            items = self.event_stack.get()
            func = items[0]
            args = items[1:]
            func(*args)

    def button_save_click_handler(self):
        self.save()

    def button_click_handler(self):
        self.terminal("The other plot is clear now")

        if not self.telemetry.enabled:
            self.button.label = "Disable"
            self.telemetry.enabled = True
            self.telemetry.clear()
        else:
            self.button.label = "Enable"
            self.telemetry.enabled = False

    # terminal
    def _terminal(self, s):
        self.pre.text += s + "\n"

    def terminal(self, s):
        self.event_stack.put((self._terminal, s))

    def clear_all(self):
        for i in self.plots:
            src = ColumnDataSource(data=dict(x=[0], y=[0]))
            i._source.data.update(src.data)