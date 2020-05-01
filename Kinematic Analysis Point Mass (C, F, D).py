import numpy as np
import GraphingModule
import AnimationModule


def num_integration(arr1, arr2, arr3):
    a = arr2[n + 1]                # acceleration value used to calculate velocity and so on
    b = arr1[n + 1] - arr1[n]      # sample interval from point a to b
    c = arr3[n]                   # constant of integration, in this case an initial value
    integral_value = (a * b) + c  # integration and sum of constant
    return integral_value


# Recollect data from accelerometer and gyroscope

filename1 = 'sensor_data/Raw Data 13.csv'  # Open .csv file with time and acceleration in 3 axis, x,y,z

sample_rate = 100  # Set the sample rate for the specified device

time = np.array(
    np.loadtxt(filename1, delimiter=',', skiprows=1, usecols=0))  # Create an array containing time values
acceleration_x = np.array(
    np.loadtxt(filename1, delimiter=',', skiprows=1, usecols=1))  # Create an array containing acceleration values in x
acceleration_y = np.array(
    np.loadtxt(filename1, delimiter=',', skiprows=1, usecols=2))  # Create an array containing acceleration values in y
acceleration_z = np.array(
    np.loadtxt(filename1, delimiter=',', skiprows=1, usecols=3))  # Create an array containing acceleration values in z

dimensions = np.shape(time)  # Determine shape of time array
rows = dimensions[0]         # Determine number of rows to be used later to set for loop iterations

calibration_x = np.max(abs(acceleration_x[0:100]))
calibration_y = np.max(abs(acceleration_y[0:100]))
calibration_z = np.max(abs(acceleration_z[0:100]))

time = time[100:rows - 100]
acceleration_x = acceleration_x[100:rows - 100]
acceleration_y = acceleration_y[100:rows - 100]
acceleration_z = acceleration_z[100:rows - 100]

# Declare arrays for velocity and position in x,y,z directions with a size equal to that of time
velocity_x = np.zeros(len(time))
velocity_y = np.zeros(len(time))
velocity_z = np.zeros(len(time))
updated_velocity_x = np.array([])
updated_velocity_y = np.array([])
updated_velocity_z = np.array([])
velocity_data = np.array([])

position_x = np.zeros(len(time))
position_y = np.zeros(len(time))
position_z = np.zeros(len(time))
position_data = np.array([])

for i in range(len(time)):
    acceleration_x[i] = acceleration_x[i] - calibration_x

    acceleration_y[i] = acceleration_y[i] - calibration_y

    acceleration_z[i] = acceleration_z[i] - calibration_z

for i in range(len(time) - 1):
    if abs(acceleration_x[i]) < calibration_x:
        acceleration_x[i] = 0

    if abs(acceleration_y[i]) < calibration_y:
        acceleration_y[i] = 0

    if abs(acceleration_z[i]) < calibration_z:
        acceleration_z[i] = 0


result_x = 0
result_y = 0
result_z = 0

for n in range(len(time) - 1):
    # integrate raw acceleration to obtain raw velocity
    result_x = num_integration(time, acceleration_x, velocity_x)
    result_y = num_integration(time, acceleration_y, velocity_y)
    result_z = num_integration(time, acceleration_z, velocity_z)
    # Store integrated data in a velocity array
    velocity_x[n+1] = result_x
    velocity_y[n+1] = result_y
    velocity_z[n+1] = result_z


########################################################################################################################

plyfit_vx = np.polyfit(time, velocity_x, 5)  # Create a fitted curve of third degree to the velocity data
plyfit_val_vx = np.polyval(plyfit_vx, time)  # Extract polynomial values for each time signature in the array time

plyfit_vy = np.polyfit(time, velocity_y, 5)
plyfit_val_vy = np.polyval(plyfit_vy, time)

plyfit_vz = np.polyfit(time, velocity_z, 5)
plyfit_val_vz = np.polyval(plyfit_vz, time)

for i in range(len(time)):
    a = velocity_x[i] - plyfit_val_vx[i]  # Subtract the poly fitted value from the original velocity value
    updated_velocity_x = np.append(updated_velocity_x, a)  # Store this new value as the updated velocity

    b = velocity_y[i] - plyfit_val_vy[i]
    updated_velocity_y = np.append(updated_velocity_y, b)

    c = velocity_z[i] - plyfit_val_vz[i]
    updated_velocity_z = np.append(updated_velocity_z, c)


count_x = 0
count_y = 0
count_z = 0
for i in range(len(time)):
    if acceleration_x[i] == 0:
        count_x += 1
    if count_x == 450:
        updated_velocity_x[i - 450:i] = 0
        count_x = 0

    if acceleration_y[i] == 0:
        count_y += 1
    if count_y == 450:
        updated_velocity_y[i - 450:i] = 0
        count_y = 0

    if acceleration_z[i] == 0:
        count_z += 1
    if count_z == 450:
        updated_velocity_z[i - 450:i] = 0
        count_z = 0


########################################################################################################################
result_x = 0
result_y = 0
result_z = 0

for n in range(len(time) - 1):
    # integrate raw velocity to obtain raw position
    result_x = num_integration(time, updated_velocity_x, position_x)
    result_y = num_integration(time, updated_velocity_y, position_y)
    result_z = num_integration(time, updated_velocity_z, position_z)
    # Store integrated data in a position array
    position_x[n+1] = result_x
    position_y[n+1] = result_y
    position_z[n+1] = result_z

########################################################################################################################

GraphingModule.graph(time, acceleration_x, acceleration_y, acceleration_z, 'Acceleration (m/s^2)', 'Acceleration Data',
                     1)
GraphingModule.graph(time, velocity_x, velocity_y, velocity_z, 'Velocity (m/s)',
                     'Velocity Data', 2)
GraphingModule.graph(time, updated_velocity_x, updated_velocity_y, updated_velocity_z, 'Velocity (m/s)',
                     'Velocity Data', 3)
GraphingModule.graph(time, position_x, position_y, position_z, 'Position (m)', 'Position Data', 4)
GraphingModule.animation1d(position_x, position_y)
# AnimationModule.animation(position_x, position_z, position_y)
