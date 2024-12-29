from tkinter import *
from tkinter import ttk
from typing import Optional, Any
from csv import writer
from dataclasses import dataclass, field 
from vehicle_data import convert_speed
from vehicle_data import rpm
from vehicle_data import throttle_position
from vehicle_data import coolant_temperature
from concurrent.futures import ThreadPoolExecutor, wait

root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()


# Stolen from https://github.com/jacobktm/stressmon/updatepool.py
class UpdatePool:

    def __init__(self) -> None:
        self.update_pool = {}
        self.executor = None

    def __del__(self) -> None:
        if self.executor:
            self.executor.shutdown()

    def add_executor(self, classname, update_fn) -> None:
        """Add sensor.update function to update pool
        """
        self.update_pool[classname] = update_fn

    def do_updates(self, *args, **kwargs) -> None:
        """Perform updates asynchronously"""
        futures = []
        if self.executor is None:
            self.executor = ThreadPoolExecutor(max_workers=len(self.update_pool.keys()))
        for _, func in self.update_pool.items():
            futures.append(self.executor.submit(func, *args, **kwargs))
        wait(futures)

class OutputData:
    csv_fn: Optional[str] = field(default=None)
    summary_fn: Optional[str] = field(default=None)
    # vehicle run time
    run_time: Optional[float] = field(default=None)
    data: Optional[list] = field(default=None)
    time: Optional[str] = field(default=None)
    speed: Optional[convert_speed] = field(default=None)
    rpm_data: Optional[rpm] = field(default=None)
    throttle: Optional[throttle_position] = field(default=None)
    coolant: Optional[coolant_temperature] = field(default=None)

# Write to csv for data log
# I will have to adjust this to how I need. Read the docs
def write_csv(output_data: OutputData) -> None:
    with open(file=output_data.csv_fn, mode='a', encoding='utf-8') as outfile:
        csv_writer = writer(outfile)
        csv_writer.writerow(output_data.data)

class DataGUI:
    def __init__(self, root):
        self.root

tkinter:Tk(screenName=None, baseName=None, className='Tk', useTk=True, sync=False, use=None)


ttk.Label(frm, text=f"Speed: {convert_speed()}").grid(column=0, row=0)
ttk.Label(frm, text=f"RPM: {rpm()}").grid(column=0, row=1)
ttk.Label(frm, text=f"Throttle Position: {throttle_position()}").grid(column=0, row=2)
ttk.Label(frm, text=f"Coolant Temp: {coolant_temperature()}").grid(column=0, row=3)

ttk.Button(frm, text="goodbye", command=root.destroy).grid(column=0, row=4)

root.mainloop()