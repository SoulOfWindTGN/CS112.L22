from gene import City, generate_input, path_cost
import matplotlib.pyplot as plt
from timeit import default_timer as timer

def visualize(cities):
    fig = plt.figure()
    fig.suptitle('2-OPT')
    x_list, y_list = [], []
    for city in cities:
        x_list.append(city.x)
        y_list.append(city.y)
    x_list.append(cities[0].x)
    y_list.append(cities[0].y)

    plt.plot(x_list, y_list, 'ro')
    plt.plot(x_list, y_list, 'g')
    plt.show(block=True)

def swap(route, i, j):
    out = route[:i]
    temp = route[i:j+1]
    out += temp[::-1]
    if (j != len(route)-1):
        out += route[j+1:]
    return out

def two_opt(route):
    best = route
    best_cost = path_cost(best)
    improvement = True
    while improvement:
        improvement = False
        for i in range(0, len(best)-1):
            for j in range(i+1, len(best)):
                new_route = swap(best, i, j)
                if (path_cost(new_route) < best_cost):
                    best = new_route
                    best_cost = path_cost(best)
                    improvement = True
    return best

size = int(input())
range_ = int(input())

cities = generate_input(size, range_)
cities = two_opt(cities)
visualize(cities)
print('min_path_cost = ', path_cost(cities))

'''
Mã giả đã tham khảo tại:
https://en.wikipedia.org/wiki/2-opt
'''