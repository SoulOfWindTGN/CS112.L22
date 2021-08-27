import math
maxsize = float('inf')
min_cost = maxsize # Khởi tạo trọng số của chu trình ngắn nhất = vô cùng
def get_matrix(cities): # Adjacency matrix chứa khoảng cách giữa các thành phố với nhau
  matrix = []
  for i in range(len(cities)):
    temp = [cities[i].distance(cities[j]) for j in range(len(cities))]
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

def TSP(adj_matrix, lower_bound, curr_cost, level, N, curr_path, final_path, visited, first_min, second_min):
	global min_cost
	# nếu đi đến thành phố thứ N thì đã đi hết qua tất cả thành phố
	if level == N:
    # cộng curr_cost (chính là tổng weight đã đi qua) với khoảng cách giữa thành phố cuối và thành phố đầu để ra weight của chu trình
		curr_cost += adj_matrix[curr_path[-1]][curr_path[0]] 
		if curr_cost < min_cost:
			final_path[:] = curr_path[:]
			min_cost = curr_cost
		return

	for i in range(N):	
		if visited[i] == False: # Xét thành phố/đỉnh tiếp theo mà chưa được đi đến để đi tiếp
			temp = lower_bound
			curr_cost += adj_matrix[curr_path[level - 1]][i] # Giả sử chọn đi đến đỉnh i
      # Giảm lower bound (của min_cost) bằng cách trừ đi trung bình cộng (cạnh có trọng số bé nhì của đỉnh đã đi qua và cạnh có trọng số 
      # bé nhì của đỉnh đang xét để đi đến), nếu đã trừ hết cạnh bé nhì của đỉnh nào thì mới trừ đến cạnh bé nhất của nó để giữ 
      # lower bound (giới hạn dưới) luôn thấp nhất. (Trừ đi để sau đó thay bằng curr_cost, chính là tổng weight đã thực sự đi qua)
			if level ==1:   
				lower_bound -= ((second_min[curr_path[level - 1]] + second_min[i]) / 2)
			else:
				lower_bound -= ((first_min[curr_path[level - 1]] + second_min[i]) / 2)
    
      # Nếu lower bound + curr_cost < min_cost (tức lower bound mà weight của chu trình có thể đạt được nếu đi tiếp tới đỉnh i 
      # đang xét < weight của chu trình ngắn nhất đang có) thì ta mới đi tiếp đến đỉnh đó
			if lower_bound + curr_cost < min_cost:
				curr_path[level] = i
				visited[i] = True
				TSP(adj_matrix, lower_bound, curr_cost, level + 1, N, curr_path, final_path, visited, first_min, second_min)

			# Nếu không thì ta phục hồi trạng thái cũ của lower bound, curr_cost và visited (tức bỏ qua đỉnh i và chọn xét tiếp đỉnh khác)
			lower_bound = temp
			curr_cost -= adj_matrix[curr_path[level - 1]][i]	
			visited = [False] * N
			for j in range(level):
				if curr_path[j] != -1:
					visited[curr_path[j]] = True


def branch_and_bound(cities):
  global min_cost
  min_cost = maxsize
  adj_matrix = get_matrix(cities) 
  N = len(cities)
  
  lower_bound = 0
  curr_path = [0] + [-1] * (N-1) # Bắt đầu đi từ thành phố đầu tiên (thành phố thứ 0)
  visited = [True] + [False] * (N-1) # Đã ghé qua thành phố đầu tiên
  final_path = [-1] * (N)
  
  # Khởi tạo lower bound (của min_cost) = Tổng(Trung bình cộng(2 cạnh có trọng số bé nhất và bé nhì của mỗi đỉnh)), tức là weight của mọi
  # chu trình có thể có được từ đồ thị luôn >= lower bound này
  first_min, second_min = [], []
  for i in range(N):
    first, second = first_and_second_min(adj_matrix, i, N)
    first_min.append(first); second_min.append(second)
    lower_bound += first + second
  lower_bound = lower_bound / 2 

	# Gọi hàm TSP với curr_cost = 0 và level = 1 (trọng số đã đi được = 0, đi đến thành phố thứ 1)
  TSP(adj_matrix, lower_bound, 0, 1, N, curr_path, final_path, visited, first_min, second_min)

  route = [cities[i] for i in final_path]
  return min_cost, route

# Link tham khảo: https://www.geeksforgeeks.org/traveling-salesman-problem-using-branch-and-bound-2/