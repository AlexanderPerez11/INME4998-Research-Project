import numpy as np
import matplotlib.pyplot as plt
# result_x = 0
# result_y = 0
# result_z = 0
def num_integration(arr1, arr2, arr3, n):
    a = arr2[n + 1]  # acceleration value used to calculate velocity and so on
    b = arr1[n + 1] - arr1[n]  # sample interval from point a to b
    c = arr3[n]  # constant of integration, in this case an initial value
    integral_value = (a * b) + c  # integration and sum of constant
    return integral_value


def merge_list(arr1, arr2, arr3, arr4, arr5, arr6, arr7, arr8, arr9, arr10):
    # create a list of coordinates to make animation easier
    merged_list = [[arr1], [arr2], [arr3], [arr4], [arr5], [arr6], [arr7], [arr8], [arr9], [arr10]]
    return merged_list

def graph(var1, var2, var3, var4, ylabel, title, fig):
    plt.figure(fig)
    plt.clf()
    plt.plot(var1, var2, color="Orange",label="x")
    plt.plot(var1, var3, color="Green",label="y")
    plt.plot(var1, var4, color="Blue",label="z")
    plt.xlabel('time(s)')
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid()
    plt.show()

    # Recollect data from accelerometer and gyroscope
    # gyro_data = 'sensor_data/Full Motion/Gyroscope.csv'  # Open .csv file with time and
    # acceleration in 3 axis, x,y,z
accelerometer_data = "Raw Data.csv"

    # time1 = np.array(
    #     np.loadtxt(gyro_data, delimiter=',', skiprows=1, usecols=0))  # Create an array containing time values
    # w_x = np.array(
    #     np.loadtxt(gyro_data, delimiter=',', skiprows=1,
    #                usecols=1))  # Create an array containing acceleration values in x
    # w_y = np.array(
    #     np.loadtxt(gyro_data, delimiter=',', skiprows=1,
    #                usecols=2))  # Create an array containing acceleration values in y
    # w_z = np.array(
    #     np.loadtxt(gyro_data, delimiter=',', skiprows=1,
    #                usecols=3))  # Create an array containing acceleration values in z

time = np.array(
        np.loadtxt(accelerometer_data, delimiter=',', skiprows=1, usecols=0))  # Create an array containing time values
acceleration_x = np.array(
        np.loadtxt(accelerometer_data, delimiter=',', skiprows=1,
                   usecols=1))  # Create an array containing acceleration values in x
acceleration_y = np.array(
        np.loadtxt(accelerometer_data, delimiter=',', skiprows=1,
                   usecols=2))  # Create an array containing acceleration values in y
acceleration_z = np.array(
        np.loadtxt(accelerometer_data, delimiter=',', skiprows=1,
                   usecols=3))  # Create an array containing acceleration values in z


    # time = np.array([])
    #
    # if len(time1) == len(time2):
    #     time = time1
    #
    # else:
    #     if len(time1) > len(time2):
    #         time = time2
    #         w_x = w_x[0:-(len(time1) - len(time2))]
    #         w_y = w_y[0:-(len(time1) - len(time2))]
    #         w_z = w_z[0:-(len(time1) - len(time2))]
    #     else:
    #         time = time1
    #         acceleration_x = acceleration_x[0:-(len(time2) - len(time1))]
    #         acceleration_y = acceleration_y[0:-(len(time2) - len(time1))]
    #         acceleration_z = acceleration_z[0:-(len(time2) - len(time1))]

    # sample_rate = 100  # Set the sample rate for the specified device

    # Declare arrays for velocity and position in x,y,z directions with a size equal to that of time
    # theta_x = np.zeros(len(time))
    # theta_y = np.zeros(len(time))
    # theta_z = np.zeros(len(time))

velocity_x = np.zeros(len(time))
velocity_y = np.zeros(len(time))
velocity_z = np.zeros(len(time))
updated_velocity_x = np.array([])
updated_velocity_y = np.array([])
updated_velocity_z = np.array([])

position_x = np.zeros(len(time))
position_y = np.zeros(len(time))
position_z = np.zeros(len(time))

    # result_x = 0
    # result_y = 0
    # result_z = 0
    #
    # for n in range(len(time) - 1):
    #     # integrate raw acceleration to obtain raw velocity
    #     result_x = num_integration(time, w_x, theta_x, n)
    #     result_y = num_integration(time, w_y, theta_y, n)
    #     result_z = num_integration(time, w_z, theta_z, n)
    #     # Store integrated data in a velocity array
    #     theta_x[n + 1] = result_x
    #     theta_y[n + 1] = result_y
    #     theta_z[n + 1] = result_z
    #
    # theta_x = theta_x * 0
    # theta_y = theta_y * 0
calibration_x = np.max(abs(acceleration_x[0:100]))
calibration_y = np.max(abs(acceleration_y[0:100]))
calibration_z = np.max(abs(acceleration_z[0:100]))

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
    result_x = num_integration(time, acceleration_x, velocity_x, n)
    result_y = num_integration(time, acceleration_y, velocity_y, n)
    result_z = num_integration(time, acceleration_z, velocity_z, n)
        # Store integrated data in a velocity array
    velocity_x[n + 1] = result_x
    velocity_y[n + 1] = result_y
    velocity_z[n + 1] = result_z

poly_fit_vx = np.polyfit(time, velocity_x, 3)  # Create a fitted curve of third degree to the velocity data
poly_fit_values_vx = np.polyval(poly_fit_vx,
                                    time)  # Extract polynomial values for each time signature in the array time

poly_fit_vy = np.polyfit(time, velocity_y, 3)
poly_fit_values_vy = np.polyval(poly_fit_vy, time)

poly_fit_vz = np.polyfit(time, velocity_z, 3)
ply_fit_values_vz = np.polyval(poly_fit_vz, time)

for i in range(len(time)):
    a = velocity_x[i] - poly_fit_values_vx[i]  # Subtract the poly fitted value from the original velocity value
    updated_velocity_x = np.append(updated_velocity_x, a)  # Store this new value as the updated velocity

    b = velocity_y[i] - poly_fit_values_vy[i]
    updated_velocity_y = np.append(updated_velocity_y, b)

    c = velocity_z[i] - ply_fit_values_vz[i]
    updated_velocity_z = np.append(updated_velocity_z, c)

count_x = 0
count_y = 0
count_z = 0
for i in range(len(time)):
    if acceleration_x[i] == 0:
        count_x += 1
    if count_x == 400:
        updated_velocity_x[i - 400:i] = 0
        count_x = 0

    if acceleration_y[i] == 0:
        count_y += 1
    if count_y == 400:
        updated_velocity_y[i - 400:i] = 0
        count_y = 0

    if acceleration_z[i] == 0:
        count_z += 1
    if count_z == 400:
        updated_velocity_z[i - 400:i] = 0
        count_z = 0

result_x = 0
result_y = 0
result_z = 0
for n in range(len(time) - 1):
        # integrate raw velocity to obtain raw position
    result_x = num_integration(time, updated_velocity_x, position_x, n)
    result_y = num_integration(time, updated_velocity_y, position_y, n)
    result_z = num_integration(time, updated_velocity_z, position_z, n)
        # Store integrated data in a position array
    position_x[n + 1] = result_x
    position_y[n + 1] = result_y
    position_z[n + 1] = result_z

graph(time, position_x, position_y, position_z, "Position (m)", "Position with Zero Velocity Update",1)
