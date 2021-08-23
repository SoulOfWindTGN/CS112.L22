''' 
Thuật toán tham khảo: https://en.wikipedia.org/wiki/Christofides_algorithm
Code tham khảo: https://github.com/Retsediv/ChristofidesAlgorithm/blob/master/christofides.py
'''


from gene import City, generate_input, path_cost
import matplotlib.pyplot as plt

#Xây đồ thị là một dict với key là đỉnh và mỗi cây có thêm một dict chứa các key là đỉnh khác và value là khoảng cách tới đỉnh đó
def build_graph(cities: list):
    graph = {}

    for i in range(len(cities)):
        for j in range(len(cities)):
            if i != j: # Nếu 2 đỉnh khác nhau thì tính khoảng cách và đưa vào dict
                if i not in graph: # i chưa có trong đồ thị thì đưa vào đồ thị bằng cách tạo một dict rỗng
                    graph[i] = {}

                graph[i][j] = cities[i].distance(cities[j])

    return graph

#Tim cây bao trùm nhỏ nhất

class UnionFind:
    def __init__(self):
        self.weights = {}
        self.parents = {}

    #Phương thức get
    def __getitem__(self, object):
        if object not in self.parents:
            self.parents[object] = object
            self.weights[object] = 1
            return object

        # find path of objects leading to the root
        path = [object]
        root = self.parents[object]
        while root != path[-1]:
            path.append(root)
            root = self.parents[root]

        # compress the path and return
        for ancestor in path:
            self.parents[ancestor] = root
        return root

    def __iter__(self):
        return iter(self.parents)

    def union(self, *objects):
        roots = [self[x] for x in objects]
        heaviest = max([(self.weights[r], r) for r in roots])[1]
        for r in roots:
            if r != heaviest:
                self.weights[heaviest] += self.weights[r]
                self.parents[r] = heaviest

def minimum_spanning_tree(G):
    tree = []
    subtrees = UnionFind()
    for W, u, v in sorted((G[u][v], u, v) for u in G for v in G[u]):
        if subtrees[u] != subtrees[v]:
            tree.append((u, v, W))
            subtrees.union(u, v)

    return tree

# Tìm đỉnh có bậc lẻ
def find_odd_vertexes(MST):
    tmp_g = {} #Đếm tần suất xuất hiện
    vertexes = [] #Lưu kết quả
    for edge in MST:
        if edge[0] not in tmp_g:
            tmp_g[edge[0]] = 0

        if edge[1] not in tmp_g:
            tmp_g[edge[1]] = 0

        tmp_g[edge[0]] += 1
        tmp_g[edge[1]] += 1

    for vertex in tmp_g:
        if tmp_g[vertex] % 2 == 1:
            vertexes.append(vertex)

    return vertexes

# tìm cặp ghép đầy đủ có trọng số nhỏ nhất
def minimum_weight_matching(MST, G, odd_vert):
    while odd_vert:
        v = odd_vert.pop()
        length = float("inf")
        u = 1
        closest = 0
        for u in odd_vert:
            if v != u and G[v][u] < length:
                length = G[v][u]
                closest = u

        MST.append((v, closest, length))
        odd_vert.remove(closest)

#Tìm chu trình Euler
def find_eulerian_tour(MatchedMSTree, G):
    # Tìm neighbours
    neighbours = {}
    for edge in MatchedMSTree:
        if edge[0] not in neighbours:
            neighbours[edge[0]] = []

        if edge[1] not in neighbours:
            neighbours[edge[1]] = []

        neighbours[edge[0]].append(edge[1])
        neighbours[edge[1]].append(edge[0])

    # print("Neighbours: ", neighbours)

    # Tìm chu trình Hamilton
    start_vertex = MatchedMSTree[0][0]
    EP = [neighbours[start_vertex][0]]

    while len(MatchedMSTree) > 0:
        for i, v in enumerate(EP):
            if len(neighbours[v]) > 0:
                break

        while len(neighbours[v]) > 0:
            w = neighbours[v][0]

            remove_edge_from_matchedMST(MatchedMSTree, v, w)

            del neighbours[v][(neighbours[v].index(w))]
            del neighbours[w][(neighbours[w].index(v))]

            i += 1
            EP.insert(i, w)

            v = w

    return EP

# Xóa cạnh trùng
def remove_edge_from_matchedMST(MatchedMST, v1, v2):

    for i, item in enumerate(MatchedMST):
        if (item[0] == v2 and item[1] == v1) or (item[0] == v1 and item[1] == v2):
            del MatchedMST[i]

    return MatchedMST

def visualize(cities):
    fig = plt.figure()
    fig.suptitle('Christofides')
    x_list, y_list = [], []
    for city in cities:
        x_list.append(city.x)
        y_list.append(city.y)
    x_list.append(cities[0].x)
    y_list.append(cities[0].y)

    plt.plot(x_list, y_list, 'ro')
    plt.plot(x_list, y_list, 'g')
    plt.show(block=True)

cities = [City(5,6),City(3,2),City(4,8),City(5,10),City(4,20)]
print(cities)
graph = build_graph(cities)
print(graph)
mst = minimum_spanning_tree(graph)
print(mst)
odd_vertex = find_odd_vertexes((mst))
print(odd_vertex)
minimum_weight_matching(mst, graph, odd_vertex)
print(mst)

eulerian_tour = find_eulerian_tour(mst, graph)
print("Eulerian tour: ", eulerian_tour)

#In ra đường đi bằng cách bỏ qua các đỉnh trùng
current = eulerian_tour[0]
path = [current]
visited = [False] * len(eulerian_tour)


length = 0

for v in eulerian_tour[1:]:
    if not visited[v]:
        path.append(v)
        visited[v] = True

        length += graph[current][v]
        current = v

#Lấy đường đi để visualize
visual = []
for i in range(len(path)):
    visual.append(cities[path[i]])

#In kết quả
print("Result path: ", path)
print("Result length of the path: ", length)
visualize(visual)
