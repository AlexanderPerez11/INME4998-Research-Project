import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def graph(var1, var2, var3, var4, ylabel, title, fig):

    plt.figure(fig)
    plt.clf()
    plt.plot(var1, var2, color="Orange", label='X')
    plt.plot(var1, var3, color="Green", label='Y')
    plt.plot(var1, var4, color="Blue", label='z')
    plt.axhline(lw=1, color='k')
    plt.axvline(lw=1, color='k')
    plt.xlabel('time(s)')
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid()
    plt.show()


def animation1d(xpos, ypos):

    # from celluloid import Camera
    fig = plt.figure()
    fig.canvas.set_window_title('1D Animation')
    ax1 = fig.add_subplot(211, autoscale_on=False, xlim=(-2, 2), ylim=(-2, 2))
    ax1.grid()
    ax1.set_title('Motion in x-Axis')
    ax1.set_xlabel("Position (m)")
    ax1.axes.yaxis.set_ticklabels([])
    ax1.axhline(lw=1, color='k')
    l1, = ax1.plot([], [], 'ro', markersize=10)

    ax2 = fig.add_subplot(212, autoscale_on=False, xlim=(-2, 2), ylim=(-2, 2))
    ax2.grid()
    ax2.set_title('Motion in y-Axis')
    ax2.set_xlabel("Position (m)")
    ax2.axes.yaxis.set_ticklabels([])
    ax2.axhline(lw=1, color='k')
    l2, = ax2.plot([], [], 'ro', markersize=10)

    plt.subplots_adjust(wspace=0.6, hspace=0.8)

    # initialization function
    def init1():
        l1.set_data([], [])
        return l1,

    def init2():
        l2.set_data([], [])
        return l2,

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

    # call the animation
    animation.FuncAnimation(fig, animate1, init_func=init1, frames=len(xpos), interval=10, blit=True,
                                   repeat=False)
    animation.FuncAnimation(fig, animate2, init_func=init2, frames=len(ypos), interval=10, blit=True,
                                   repeat=False)
    plt.show()
