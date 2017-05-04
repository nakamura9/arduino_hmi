import Tkinter as tk
import ttk
import datetime, time
import serial
import subprocess
import json
import os 

class GeneratorApplication(ttk.Frame):
    def __init__(self, conn, master=None):
        ttk.Frame.__init__(self, master)
        if not os.path.isfile("persistent.json"):    
            data = {"total_run": 0,
                    "service": 200}

            with open("persistent.json", 'w+') as fil:
                json.dump(data, fil)
            
        with open("persistent.json", 'r') as f:
            persistent = json.load(f)
        
        self.total_run_time = persistent["total_run"]
        self.service = persistent["service"]
        self._start = None
        self.conn = conn
        self.hours_run = 0
        self.due = "30/04/17"
        self.fuel_level = "High"
        self.oil_temp = "Ok"
        self.fuel_level = "Too High"
        self.cool_temp = "Ok"
        self.run_state = tk.IntVar()
        self._events = ["Window started..."]
        self.grid()
        self.createWidgets()
        self.start = datetime.datetime.now()

    @property
    def events(self):
        if len(self._events) > 100:
            self._events = self._events[98:]
        return "\n".join(self._events)

    @property
    def now(self):
        return datetime.datetime.now().strftime("%H:%M:%S")
    def createWidgets(self):
        
        self.radioLabel = ttk.Labelframe(self, text="Running Mode:")
        self.radioAuto = ttk.Radiobutton(self.radioLabel, text="Auto", variable=self.run_state, value=1, command=self.radio_changed)
        self.radioManual = ttk.Radiobutton(self.radioLabel, text="Manual",variable=self.run_state, value=0, command=self.radio_changed)
        self.radioLabel.grid(row=0, column=0, columnspan=2)
        self.radioAuto.pack(side="left")
        self.radioManual.pack(side="right")

        self.controlLabel = ttk.Labelframe(self, text="Generator Control")
        self.startButton = ttk.Button(self.controlLabel, text="Start", command=self.start)
        self.stopButton = ttk.Button(self.controlLabel, 
        text="Stop", command=self.stop)
        self.startButton.pack(side="left")
        self.stopButton.pack(side="right")
        self.controlLabel.grid(row=0, column=2, columnspan=2)
        
        self.controlLabel = ttk.Labelframe(self, text="Fuel Pump Control")
        self.startButton = ttk.Button(self.controlLabel, text="Start", command=self.start_pump)
        self.stopButton = ttk.Button(self.controlLabel, 
        text="Stop", command=self.stop_pump)
        self.startButton.pack(side="left")
        self.stopButton.pack(side="right")
        self.controlLabel.grid(row=1, column=0, columnspan=2)
        
        
        self.hoursTitleLabel= ttk.Labelframe(self, text="Running hours:")
        self.hoursContentLabel= ttk.Label(self.hoursTitleLabel, text=self.hours_run)
        self.hoursContentLabel.pack()
        self.hoursTitleLabel.grid(row=1, column=2, columnspan=2)
        


        self.dueTitleLabel= ttk.Labelframe(self, text="Service Time Due:")
        self.dueContentLabel= ttk.Label(self.dueTitleLabel, text=self.due)
        self.dueContentLabel.pack()
        self.dueTitleLabel.grid(row=2, column=0, columnspan=2)
        

        self.fuelTitleLabel= ttk.Labelframe(self, text="Fuel Level:")
        self.fuelContentLabel= ttk.Label(self.fuelTitleLabel, text=self.fuel_level)
        self.fuelContentLabel.pack()
        self.fuelTitleLabel.grid(row=2, column=2, columnspan=2)
        
        
        self.oilTitleLabel= ttk.Labelframe(self, text="Temperature:")
        self.oilContentLabel= ttk.Label(self.oilTitleLabel, text=self.oil_temp)
        self.oilContentLabel.pack()
        self.oilTitleLabel.grid(row=3, column=0, columnspan=2)


        self.coolTitleLabel= ttk.Labelframe(self, text="Coolant Temperature:")
        self.coolContentLabel= ttk.Label(self.coolTitleLabel, text=self.cool_temp)
        self.coolContentLabel.pack()
        self.coolTitleLabel.grid(row=3, column=2, columnspan=2)



        self.alarmsTitleLabel= ttk.Labelframe(self, text="Events/ Alarms:")
        self.alarmsContentLabel= ttk.Label(self.alarmsTitleLabel, text=self.events)
        self.alarmsContentLabel.pack()
        self.alarmsTitleLabel.grid(row=4, column=0, columnspan=4)
    
    def start(self):
        if self.run_state.get():
            self._events.append("Cannot start the generator in auto mode")    
        else:
            self._events.append("Generator started at %s" % self.now)
            self.conn.write("2")
            self._start = time.time()
    
    def stop(self):
        if self.run_state.get():
            self._events.append("Cannot stop the generator in auto mode")
        else: 
            self._events.append("Generator stopped at %s" % self.now)
            self.conn.write("3")
            self.total_run_time += self._start - time.time()
            self._start = None

    def start_pump(self):
        if self.run_state.get():
            self._events.append("Cannot start the pump in auto mode")
        else: 
            self._events.append("Pump started at %s" % self.now)
            self.conn.write("4")

    def stop_pump(self):
        if self.run_state.get():
            self._events.append("Cannot stop the pump in auto mode")
        else: 
            self._events.append("Pump stopped at %s" % self.now)
            self.conn.write("5")
        

    def update(self):
        data = self.conn.read(7)
        values = data.split(',')
        temp, cool, level, generator = values[0], values[1], values[2], values[3]
        
        if int(level):
            self.fuelContentLabel.configure(text = "LOW")
        else:
            self.fuelContentLabel.configure(text="OK")

        if int(cool):
            self.coolContentLabel.configure(text = "Too Hot")
        else:
            self.coolContentLabel.configure(text="OK")

        if int(temp):
            self.oilContentLabel.configure(text = "Too Hot")
        else:
            self.oilContentLabel.configure(text="OK")

        if not self._start:
            self.hours_run = 0
        else:
            seconds_run =(time.time() - self._start)
            self.hours_run = round((seconds_run / 3600), 2)
        
        self.dueContentLabel.configure(text = self.service- self.total_run_time)
        self.alarmsContentLabel.configure(text=self.events)
        self.hoursContentLabel.configure(text = self.hours_run)
        self.after(2000, self.update)
    
    def auto(self):
        self._events.append("Generator set to Auto at at %s" % self.now)
        self.conn.write("1")

    def manual(self):
        self._events.append("Generator state reverted to manual at %s" % self.now)
        self.conn.write("0")

    def radio_changed(self):
        if self.run_state.get():
            self.auto()
        else:
            self.manual()

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        raise Exception("Argument error, This program needs a port and \
                \n baudrate to start as arguments")
    

    s = serial.Serial()
    s.port = sys.argv[1]
    s.baudrate = sys.argv[2]
    try:
        s.open()
    except serial.SerialException:
        raise Exception("Failed to connect to the serial interface \n These ports \
        are available: \n %s" % subprocess.check_output(['python',
                                    '-m', 'serial.tools.list_ports']))
        

    
app = GeneratorApplication(s)
app.master.size()
app.master.title("Generator Control Console")
app.after(2000, app.update)
app.mainloop()


