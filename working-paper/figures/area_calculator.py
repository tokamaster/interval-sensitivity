import numpy as np

def area_calculator(x, y, step_size=100, plot=False):
    """
    This function measures the area covered by x and y,
    and returns the relative amount of area left uncovered.

    Integral is calculated with the trapezoid rule.

    Example:

    if it returns 0 means that the whole area has been
    covered by x and y

    Args:
        x ([array]): data array (size N) containing independent variable samples
        y ([array]): data array (size N) containing dependent variable samples
        step_size (int, optional): sets the number of trapezoids. Defaults to 100.
        plot (bool, optional): shows distance plot. Defaults to False.

    Returns:
        [float]: relative amount of area left uncovered by x and y.
    """
    bin_edges = np.linspace(np.min(x), np.max(x), step_size + 1)
    edge_location = []
    for i in range(len(x)):
        for j in range(step_size):
            if bin_edges[j] <= x[i] <= bin_edges[j+1]:
                edge_location.append(j)
                break

    areas = []
    heights = []

    for i in range(step_size):
        samps = []
        for j in range(len(y)):
            if edge_location[j] == i:
                samps.append(y[j])
        height = np.max(samps) - np.min(samps)
        heights.append(height)
        base = bin_edges[i+1]-bin_edges[i]
        areas.append(height*base)

    absolute_area = np.sum(areas)
    total_area = (np.max(y)-np.min(y))*(np.max(x)-np.min(x))
    if plot == True:
        import matplotlib.pyplot as plt
        plt.hist(bin_edges[:-1], bin_edges, weights=heights)
        plt.show()
    return 1-(absolute_area/total_area)

def box_plotter(x, y, step_size=100):

    bin_edges = np.linspace(np.min(x), np.max(x), step_size + 1)
    edge_location = []
    for i in range(len(x)):
        for j in range(step_size):
            if bin_edges[j] <= x[i] <= bin_edges[j+1]:
                edge_location.append(j)
                break

    heights = []
    points = []
    widths = []

    for i in range(step_size):
        samps = []
        for j in range(len(y)):
            if edge_location[j] == i:
                samps.append(y[j])
        height = np.max(samps) - np.min(samps)
        heights.append(height)
        base = bin_edges[i+1]-bin_edges[i]
        points.append([np.min(samps), np.max(samps)])
        widths.append(base)

    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    fig, ax = plt.subplots()
    ax.scatter(x,y)
    ax.add_patch(Rectangle((np.min(x), np.min(y)), width=np.max(x)-np.min(x),
                 height=np.max(y)-np.min(y), linewidth=3, edgecolor='black', facecolor='black', fill=True, alpha=0.2))
    for i in range(len(widths)):
        ax.add_patch(Rectangle((bin_edges[i], points[i][0]), widths[i],
                     heights[i], linewidth=3, edgecolor='r', facecolor='r', fill=True, alpha=0.5))
