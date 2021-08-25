from gene import City, generate_input
import math
import matplotlib.pyplot as plt
def visualize(cities, title):
    fig = plt.figure()
    fig.suptitle(title)
    x_list, y_list = [], []
    for city in cities:
        x_list.append(city.x)
        y_list.append(city.y)
    x_list.append(cities[0].x)
    y_list.append(cities[0].y)
    plt.plot(x_list, y_list, 'ro')
    plt.plot(x_list, y_list, 'g')
    plt.show(block=True)

# Branch_and_bound
maxsize = float('inf')
min_cost = maxsize # Khởi tạo độ dài của chu trình có trọng số ngắn nhất = vô cùng

def get_matrix(cities):
  matrix=[]
  for i in range(len(cities)):
    temp=[cities[i].distance(cities[j]) for j in range(len(cities))]
    matrix.append(temp)
  return matrix

def first_and_second_min(adj_matrix, i, N): # Hàm tìm 2 cạnh có weight bé nhất nối với đỉnh i
  first, second = maxsize, maxsize
  for j in range(N):
    if adj_matrix[i][j] < first and i!=j:
        second = first
        first = adj_matrix[i][j]
    elif adj_matrix[i][j] < second and i!=j:
        second=adj_matrix[i][j]
  return first, second 

def TSP(adj_matrix, lower_bound, curr_weight, curr_path, visited, level, N, first_min, second_min, final_path):
	global min_cost
	# nếu đi đến thành phố thứ N thì đã đi hết qua tất cả thành phố
	if level == N:
    # cộng curr_weight (tổng weight đã đi) với khoảng cách giữa thành phố cuối và thành phố đầu để ra tổng weight của chu trình
		total_cost = curr_weight + adj_matrix[curr_path[-1]][curr_path[0]] 
		if total_cost < min_cost:
			final_path[:]=curr_path[:]
			min_cost=total_cost
		return

	for i in range(N):	
		if visited[i] == False: # Xét thành phố/đỉnh tiếp theo mà chưa được đi đến để đi tiếp
			temp = lower_bound
			curr_weight += adj_matrix[curr_path[level - 1]][i]
      # Giảm lower bound (của min_cost) bằng cách trừ đi trung bình cộng (cạnh có trọng số bé nhì của đỉnh đã đi qua và cạnh có trọng số 
      # bé nhì của đỉnh đang xét để đi đến), nếu đã trừ hết cạnh bé nhì của đỉnh nào thì mới trừ đến cạnh bé nhất của nó để giữ 
      # lower bound (giới hạn dưới) luôn thấp nhất. (Trừ đi để thay bằng curr_weight, chính là tổng weight đã thực sự đi qua)
			if level ==1:   
				lower_bound -= ((second_min[curr_path[level - 1]] + second_min[i]) / 2)
			else:
				lower_bound -= ((first_min[curr_path[level - 1]] + second_min[i]) / 2)
      # Nếu lower bound + tổng weight đã đi qua (tức lower bound thực sự có thể đạt được nếu đi tiếp với tổng trọng số đó) < min_cost 
      # thì ta mới đi tiếp đến đỉnh đó
			if lower_bound + curr_weight < min_cost:
				curr_path[level] = i
				visited[i] = True
				TSP(adj_matrix, lower_bound, curr_weight, curr_path, visited, level + 1, N, first_min, second_min, final_path)

			# Nếu không thì ta phục hồi trạng thái cũ của lower bound, curr_weight và visited
			lower_bound = temp
			curr_weight -= adj_matrix[curr_path[level - 1]][i]	
			visited = [False] * N
			for j in range(level):
				if curr_path[j] != -1:
					visited[curr_path[j]] = True

def branch_and_bound(cities):
  global min_cost
  min_cost = maxsize
  adj_matrix = get_matrix(cities) # Adjacency matrix chứa khoảng cách giữa các thành phố với nhau
  N = len(cities)
  
  lower_bound = 0
  curr_path = [0] + [-1] * (N-1) # Bắt đầu đi từ thành phố đầu tiên (thành phố thứ 0)
  visited = [True] + [False] * (N-1) # Đã ghé qua thành phố đầu tiên
  final_path = [-1] * (N)
  
  # Khởi tạo lower bound (của min_cost) = Tổng(Trung bình cộng(2 cạnh có trọng số bé nhất và bé nhì của mỗi đỉnh))
  first_min, second_min = [], []
  for i in range(N):
    first, second = first_and_second_min(adj_matrix, i, N)
    first_min.append(first); second_min.append(second)
    lower_bound += first + second
  lower_bound = lower_bound / 2 

	# Gọi hàm TSP với curr_weight = 0 và level = 1 (trọng số đã đi được = 0, đi đến thành phố thứ 1)
  TSP(adj_matrix, lower_bound, 0, curr_path, visited, 1, N, first_min, second_min, final_path)
  return min_cost, final_path

cities= generate_input(8, 20)
min_cost,final_path=branch_and_bound(cities)
route=[cities[i] for i in final_path]
print('min cost:',min_cost)
print('route:', route)
visualize(route,'Branch and bound (BackTracking)')

# Link tham khảo: https://www.geeksforgeeks.org/traveling-salesman-problem-using-branch-and-bound-2/