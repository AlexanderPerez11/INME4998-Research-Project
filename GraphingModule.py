import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation

matplotlib.use('TkAgg')


def graph(time, xacc, yacc, zacc, xvel, yvel, zvel, xpos, ypos, zpos):
    fig = plt.figure(figsize=(15, 15))
    fig.canvas.set_window_title('1D Animation')
    ax1 = fig.add_subplot(321, autoscale_on=False, xlim=(-2, 2), ylim=(-2, 2))
    ax1.grid()
    ax1.set_title('Motion in x-Axis')
    ax1.set_xlabel("Position (m)")
    ax1.axes.yaxis.set_ticklabels([])
    ax1.axhline(lw=1, color='k')
    l1, = ax1.plot([], [], 'ro', markersize=10)

    ax2 = fig.add_subplot(323, autoscale_on=False, xlim=(-2, 2), ylim=(-2, 2))
    ax2.grid()
    ax2.set_title('Motion in y-Axis')
    ax2.set_xlabel("Position (m)")
    ax2.axes.yaxis.set_ticklabels([])
    ax2.axhline(lw=1, color='k')
    l2, = ax2.plot([], [], 'ro', markersize=10)

    ax3 = fig.add_subplot(325, autoscale_on=False, xlim=(-2, 2), ylim=(-2, 2))
    ax3.grid()
    ax3.set_title('Motion in z-Axis')
    ax3.set_xlabel("Position (m)")
    ax3.axes.yaxis.set_ticklabels([])
    ax3.axhline(lw=1, color='k')
    l3, = ax3.plot([], [], 'ro', markersize=10)
    plt.subplots_adjust(wspace=0.6, hspace=0.8)

    ax4 = fig.add_subplot(322, autoscale_on=True)
    ax4.grid()
    ax4.set_title('Acceleration in XYZ')
    ax4.set_xlabel("time (s)")
    ax4.set_ylabel("Acceleration (m/s^2)")
    ax4.axhline(lw=1, color='k')
    ax4.axvline(lw=1, color='k')
    ax4.plot(time, xacc, label="x")
    ax4.plot(time, yacc, label="y")
    ax4.plot(time, zacc, label="z")
    ax4.legend()

    ax5 = fig.add_subplot(324, autoscale_on=True)
    ax5.grid()
    ax5.set_title('Velocity in XYZ')
    ax5.set_ylabel("Velocity (m/s)")
    ax5.set_xlabel("time (s)")
    ax5.axhline(lw=1, color='k')
    ax5.axvline(lw=1, color='k')
    ax5.plot(time, xvel, label="x")
    ax5.plot(time, yvel, label="y")
    ax5.plot(time, zvel, label="z")
    ax5.legend()

    ax6 = fig.add_subplot(326, autoscale_on=True)
    ax6.grid()
    ax6.set_title('Position in XYZ')
    ax6.set_ylabel("Position (m)")
    ax6.set_xlabel("time (s)")
    ax6.axhline(lw=1, color='k')
    ax6.axvline(lw=1, color='k')
    ax6.plot(time, xpos, label="x")
    ax6.plot(time, ypos, label="y")
    ax6.plot(time, zpos, label="z")
    ax6.legend()

    plt.subplots_adjust(wspace=0.2, hspace=0.8)

    # initialization function
    def init1():
        l1.set_data([], [])
        return l1,

    def init2():
        l2.set_data([], [])
        return l2,

    def init3():
        l3.set_data([], [])
        return l3,

    # animation function
    def animate1(i):
        x_points = [xpos[i]]
        y_points = [0]

        l1.set_data(x_points, y_points)
        return l1,

    def animate2(i):
        x_points = [ypos[i]]
        y_points = [0]

        l2.set_data(x_points, y_points)
        return l2,

    def animate3(i):
        x_points = [ypos[i]]
        y_points = [0]

        l3.set_data(x_points, y_points)
        return l3,

    # call the animation
    animation.FuncAnimation(fig, animate1, init_func=init1, frames=len(xpos), interval=10, blit=True,
                            repeat=False)
    animation.FuncAnimation(fig, animate2, init_func=init2, frames=len(ypos), interval=10, blit=True,
                            repeat=False)
    animation.FuncAnimation(fig, animate3, init_func=init3, frames=len(zpos), interval=10, blit=True,
                            repeat=False)
    plt.show()
