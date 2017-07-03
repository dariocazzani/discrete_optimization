import math
import sys

def distance(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stderr.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush

def tour_length(points, solution):
    # calculate the length of the tour
    tour_length = distance(points[solution[-1]], points[solution[0]])
    for index in range(0, len(points)-1):
        tour_length += distance(points[solution[index]], points[solution[index+1]])
    return tour_length
