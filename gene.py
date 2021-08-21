import random
import math

class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Tính khoảng cách
    def distance(self, city):
        return math.sqrt((self.x - city.x)**2 + (self.y - city.y)**2)
    
    def __repr__(self):
        return f"({self.x}, {self.y})"

# Tạo input với num_city là số lượng thành phố muốn tạo và range_x là khoảng tọa độ tối đa
def generate_input(num_city: int, range_: int) -> City:
    return [City(x = random.randint(1, range_), y = random.randint(1, range_)) for i in range(num_city)]

# Tính chi phí
def path_cost(route) -> float:
    cost = 0
    for i in range(len(route)):
        cost = cost + route[i].distance(route[i-1])
    return cost


'''
c = generate_input(5,10)
for i in c:
    print(repr(i))
'''

