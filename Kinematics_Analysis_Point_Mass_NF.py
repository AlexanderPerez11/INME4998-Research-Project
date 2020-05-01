import numpy as np
import GraphingModule


# Define necessary functions

def num_integration(arr1, arr2, arr3):
    a = arr2[n + 1]  # acceleration value used to calculate velocity and so on
    b = arr1[n + 1] - arr1[n]  # sample interval from point a to b
    c = arr3[n]  # constant of integration, in this case an initial value
    integral_value = (a * b) + c  # integration and sum of constant
    return integral_value

def merge_list(list1, list2, list3, list4, list5, list6, list7, list8, list9, list10):
    # create a list of coordinates to make animation easier
    merged_list = [(list1[n], list2[n], list3[n], list4[n], list5[n], list6[n], list7[n], list8[n], list9[n], list10[n]) for n in range(0, len(list1))]
    return merged_list

# Recolect data from accelerometer and gyroscope

filename = 'Raw Data.csv' #Open .csv file with time and acceleration in 3 axis, x,y,z

samplerate = 50 #Set the sample rate for the specified device

time = np.array(np.loadtxt(filename, delimiter=',', skiprows=1, usecols=0)) #Create an array containing time values

acceleration_x = np.array(np.loadtxt(filename, delimiter=',', skiprows=1, usecols=1)) #Create an array containing acceleration values in x
acceleration_y = np.array(np.loadtxt(filename, delimiter=',', skiprows=1, usecols=2)) #Create an array containing acceleration values in y
acceleration_z = np.array(np.loadtxt(filename, delimiter=',', skiprows=1, usecols=3)) #Create an array containing acceleration values in z

dimensions = np.shape(time) #Determine shape of time array
rows = dimensions[0] #Determine number of rows to be used later to set for loop iterations
cutoff = samplerate / 4

######################################################################
#Declare arrays for velocity and position in x,y,z direcctions with a size equal to that of time
velocity_x = np.zeros(rows)
velocity_y = np.zeros(rows)
velocity_z = np.zeros(rows)
updated_velocity_x = np.array([])
updated_velocity_y = np.array([])
updated_velocity_z = np.array([])
velocity_data=np.array([])

position_x = np.zeros(rows)
position_y = np.zeros(rows)
position_z = np.zeros(rows)
position_data=np.array([])
######################################################################


#Create 3 result variables as temporary value storage set to 0 to have initial velocities and positions set to 0

result_x = 0
result_y = 0
result_z = 0

for n in range(rows - 1):
    # integrate raw acceleration to obtain raw velocity
    result_x = num_integration(time, acceleration_x, velocity_x)
    result_y = num_integration(time, acceleration_y, velocity_y)
    result_z = num_integration(time, acceleration_z, velocity_z)
    #Store integrated data in a velocity array
    velocity_x[n + 1] = result_x
    velocity_y[n + 1] = result_y
    velocity_z[n + 1] = result_z

######################################################################
plyfit_vx = np.polyfit(time,velocity_x,3)               #Create a fitted curve of third degree to the velocity data
plyfit_val_vx = np.polyval(plyfit_vx,time)              #Extract polynomial values for each time signature in the array time

plyfit_vy = np.polyfit(time,velocity_y,3)
plyfit_val_vy = np.polyval(plyfit_vy,time)

plyfit_vz = np.polyfit(time,velocity_z,3)
plyfit_val_vz = np.polyval(plyfit_vz,time)

for i in range(rows):
    a = velocity_x[i]-plyfit_val_vx[i]                          #Subtract the polyfitted value from the original velocity value to obtain detrended curve
    updated_velocity_x = np.append(updated_velocity_x,a)        #Store this new value as the updated velocity

    b = velocity_y[i] - plyfit_val_vy[i]
    updated_velocity_y = np.append(updated_velocity_y,b)

    c = velocity_z[i] - plyfit_val_vz[i]
    updated_velocity_z = np.append(updated_velocity_z, c)

######################################################################
result_x = 0
result_y = 0
result_z = 0

for n in range(rows - 1):
    # integrate raw velocity to obtain raw position
    result_x = num_integration(time, updated_velocity_x, position_x)
    result_y = num_integration(time, updated_velocity_y, position_y)
    result_z = num_integration(time, updated_velocity_z, position_z)
    #Store integrated data in a position array
    position_x[n + 1] = result_x
    position_y[n + 1] = result_y
    position_z[n + 1] = result_z


######################################################################
kinematic_data = np.vstack((position_x,position_y,position_z))


GraphingModule.graph(time, acceleration_x, acceleration_y, acceleration_z, 'Acceleration (m/s^2)', 'Acceleration Data', 1)
GraphingModule.graph(time, updated_velocity_x, updated_velocity_y, updated_velocity_z, 'Velocity (m/s)', 'Velocity Data', 2)
GraphingModule.graph(time, position_x, position_y, position_z, 'Position (m)', 'Position Data', 3)

