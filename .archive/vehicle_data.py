import obd
from obd import OBDStatus
#import subprocess

# I may be wrong but at the moment it seems this will only query 
# the vehicle for information once, then stop. I need to fix this.
# Maybe with while loops? Or for loops in the other file. 
# I am still learning lol

# will not work in windows lol. When on the raspi, remember to 
# uncomment the import of subprocess
#sh_sleep = subprocess.Popen(['sleep', '5'])

# Create an OBD connection
connection = obd.Async()  # Automatically detects and connects to the OBD-II adapter

#OBDStatus.NOT_CONNECTED # "Not Connected"
#OBDStatus.ELM_CONNECTED # "ELM Connected"

#use PIDs for status? https://python-obd.readthedocs.io/en/latest/Command%20Tables/ from the manual too :)
def check_obd_status():
    connection.status() == OBDStatus.CAR_CONNECTED

    if connection.status() is True:
        print("ELM device connected.")
        return True
    else:
        print("ELM device not connected.")
        return False

# Get the vehicles speed 
def speed():
    speed_response = connection.query(obd.commands.SPEED) # Vehicle speed
    
    if speed_response.value is not None:
        return speed_response
    else:
        return None
    
# Get data from speed and devide it to convert to aproximate MPH
def convert_speed():
    kmh_speed = speed()

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

# Get the vehicles rpm 
def rpm():
    rpm_response = connection.query(obd.commands.RPM)      # Engine RPM
    
    if rpm_response.value is not None:
        print(f"Vehicle RPM: {rpm}")
        return rpm_response
    else:
        print("Vehicle RPM: 0")
        return None

# Get the vehicles throttle position
def throttle_position():
    throttle_pos_b = connection.query(obd.commands.THROTTLE_POS_B)
    throttle_pos_c = connection.query(obd.commands.THROTTLE_POS_C)
    
    if throttle_pos_b.value is not None:
        print(f"Throttle: {throttle_pos_b} %")
        return throttle_pos_b
    elif throttle_pos_c.value is not None:
        print(f"Throttle: {throttle_pos_c} %")
        return throttle_pos_c
    else:
        print("Neither Throttle is used. Vehicle is off, or throttle data not available.")
        return None

# Get the vehicles coolant temperature 
def coolant_temperature():
    coolant_temp = connection.query(obd.commands.COOLANT_TEMP)  # Coolant temperature

    if coolant_temp.value is not None:
        print(f"Coolant Temp: {coolant_temp} F")
        return coolant_temp
    else:
        print("Coolant temp data not found.")
        return None

# Print/send vehicle data
def main():
    # Just writing this now to be prepaired for the future...
    check_obd_status()
    # while check_obd_status() is True:
    #
    # should the below functions be in here? I think that would constantly query
    # the vehicle for information. I may want to add wait time for this to not 
    # be too fast. Assuming this isn't slow... or maybe I need this in the
    # other file? That way it will run this instead of this running over and over?
    # But will this be too long and cause ACTUAL issues with response time?
    # I don't think that will be the case because "main()" is the only thing
    # that will be running. idk. Again, I am still learning. I also wonder if
    # doing it this way would cause memory leaks. Probably not but idk.
    # Maybe this should all be in the other file so it doesn't cause extra problems.
    speed()
    convert_speed()
    rpm()
    throttle_position()
    coolant_temperature()

    # Test and "enable" once deployed... for now
    connection.close()
    # If the OBDII adapter is not found, attempt to connect 10 times
#    if connection.status() is not True:
#        for number in range(1, 10, 1):
#            print("Vehicle not connected. Attempting to connect 10 times.")
#            connection.__connect
#            sh_sleep.wait()
#        else:
#            print("Could not connect after 10 attempts. Closing connection.")
#            connection.close()

main()