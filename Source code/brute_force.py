from gene import City, generate_input, path_cost
import itertools
import matplotlib.pyplot as plt

def visualize(cities):
    fig = plt.figure()
    fig.suptitle('Brute force')
    x_list, y_list = [], []
    for city in cities:
        x_list.append(city.x)
        y_list.append(city.y)
    x_list.append(cities[0].x)
    y_list.append(cities[0].y)

    plt.plot(x_list, y_list, 'ro')
    plt.plot(x_list, y_list, 'g')
    plt.show(block=True)

#size là số lượng thành phố
#range là khoảng cách tọa độ tối đa của x (trên trục hoành) và y(trên trục hoành) so với gốc tọa độ
# size = int(input())
# range = int(input())

#Tạo ngẫu nhiên input
cities = [City(5,6),City(3,2),City(4,8),City(5,10),City(4,20)]

#Lập ra các hoán vị để vét hết các đường đi
temp = list(itertools.permutations(cities))

min_path_cost = float('inf')
route = temp[0]
for i in temp:
     cost = path_cost(i)
     if min_path_cost > cost:
          route = i
          min_path_cost = cost

visualize(route)
print("min_cost =", min_path_cost)
'''
Mã giả tham khảo:
https://www.geeksforgeeks.org/traveling-salesman-problem-tsp-implementation/
'''
