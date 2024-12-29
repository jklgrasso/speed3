from tkinter import *
from tkinter import ttk
import vehicle_data

debug = FALSE
root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()

# Get data from vehicle_speed and devide it to convert to aproximate MPH
def speed_data():
    kmh_speed = vehicle_data.vehicle_speed()

    if kmh_speed is not None:
        # convert km/h to mph
        speed_value = kmh_speed.value.magnitude
        speed_divsor = 1.609
        devided_speed = speed_value / speed_divsor

        print(f"Speed: {devided_speed:.2f} MPH")
        return devided_speed
    else:
        print("Speed: <1 MPH")
        return " <1 MPH"

def rpm_data():
    rpm = vehicle_data.vehicle_rpm()

    if rpm is not None:
        print(f"Vehicle RPM: {rpm}")
        return rpm
    else:
        print("Vehicle RPM: 0")
        return None

def throttle_data():
    throttle_pos = vehicle_data.throttle_position()

    if throttle_pos is not None:
        print(f"Throttle: {throttle_pos} %")
    else:
        print("Vehicle is off or throttle is not found")
        return "Error"

def coolant_temperature():
    coolant_temp = vehicle_data.coolant_temperature()

    if coolant_temp is None:
        print("Coolant temp data not found.")
        return "Error"
    else:
        print(f"Coolant Temp: {coolant_temp} F")
        return coolant_temp

def main():
    ttk.Label(frm, text=f"Speed: {speed_data()}").grid(column=0, row=0)
    ttk.Label(frm, text=f"RPM: {rpm_data()}").grid(column=0, row=1)
    ttk.Label(frm, text=f"Throttle Position: {throttle_data()}").grid(column=0, row=2)
    ttk.Label(frm, text=f"Coolant Temp: {coolant_temperature()}").grid(column=0, row=3)

    ttk.Button(frm, text="goodbye", command=root.destroy).grid(column=0, row=4)

    root.mainloop()

# use for critical things. Like overheating, over boost, misfire, etc...
# for this I will need more info from the ECU. I will probably need to add
# custom PIDs or a list of trouble codes so that they can be properly "decoded"
#def crit():

#if the vehicle is off, display "vehicle off"
if rpm_data() is None:
    # Remove the while loop from the if statement when ready to deploy 
    if debug is True:
        while rpm_data() is None:
            ttk.Label(frm, text=f"Vehicle OFF").grid(column=0, row=0)
            ttk.Button(frm, text="goodbye", command=root.destroy).grid(column=0, row=4)
            print("Vehicle OFF")

            root.mainloop()
    else:
        main()