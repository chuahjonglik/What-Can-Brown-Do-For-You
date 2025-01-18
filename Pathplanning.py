import heapq
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict, Tuple
import time

def heuristic(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    """
    Heuristic function for A* algorithm: Manhattan distance between two points.

    Args:
        a (Tuple[int, int]): Point A (row, column).
        b (Tuple[int, int]): Point B (row, column).

    Returns:
        int: Estimated distance between A and B.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def parse_packages(package_list: List[Dict]) -> List[Dict]:
    """
    Parse and sort the package list based on urgency (ascending).
    Within the same urgency, sort by weight (descending).

    Args:
        package_list (List[Dict]): List of package details.

    Returns:
        List[Dict]: Sorted package list.
    """
    return sorted(package_list, key=lambda x: (x['urgency'], -x['weight']))

def parse_route_and_packages(route: List[List[str]], packages: List[Dict]) -> Tuple[Tuple[int, int], Tuple[int, int], Dict[str, Tuple[int, int]]]:
    """
    Parse the route to identify start, end points, and package locations.

    Args:
        route (List[List[str]]): 2D map representation of the route.
        packages (List[Dict]): List of package details.

    Returns:
        Tuple[Tuple[int, int], Tuple[int, int], Dict[str, Tuple[int, int]]]: Coordinates of the start, end points, and package locations.
    """
    start, end = None, None
    package_locations = {}
    for i, row in enumerate(route):
        for j, cell in enumerate(row):
            if cell == 'S':
                start = (i, j)
            elif cell == 'E':
                end = (i, j)
            elif cell.startswith('P'):
                package_locations[cell] = (i, j)

    if not start or not end:
        raise ValueError("Route must contain start (S) and end (E) points.")

    return start, end, package_locations

def a_star(route: List[List[str]], start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
    """
    Implement A* algorithm to find the shortest path between start and end.

    Args:
        route (List[List[str]]): 2D map of the route.
        start (Tuple[int, int]): Starting coordinates.
        end (Tuple[int, int]): Ending coordinates.

    Returns:
        List[Tuple[int, int]]: Path from start to end.
    """
    rows, cols = len(route), len(route[0])
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}

    def get_neighbors(node):
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),  # Cardinal directions
            (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonal directions
        ]
        neighbors = []
        for dr, dc in directions:
            r, c = node[0] + dr, node[1] + dc
            if 0 <= r < rows and 0 <= c < cols and route[r][c] != 'X':
                neighbors.append((r, c))
        return neighbors

    # def heuristic(a, b):
    #     return abs(a[0] - b[0]) + abs(a[1] - b[1])

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for neighbor in get_neighbors(current):
            tentative_g_score = g_score[current] + 1
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                if neighbor not in [i[1] for i in open_set]:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    raise ValueError("No path found from start to end.")

def visualize_with_animation(route: List[List[str]], path: List[Tuple[int, int]], title: str) -> None:
    """
    Visualize the route and path with animation using Matplotlib.

    Args:
        route (List[List[str]]): 2D grid map of the route.
        path (List[Tuple[int, int]]): Path to visualize.
        title (str): Title for the visualization.
    """
    rows, cols = len(route), len(route[0])
    grid = np.zeros((rows, cols))
    for r in range(rows):
        for c in range(cols):
            if route[r][c] == 'X':
                grid[r][c] = -1
            elif route[r][c] == 'S':
                grid[r][c] = 2
            elif route[r][c] == 'E':
                grid[r][c] = 3
            elif route[r][c].startswith('P'):
                grid[r][c] = 4

    plt.ion()
    fig, ax = plt.subplots(figsize=(8, 8))
    for r, c in path:
        grid[r][c] = 1
        ax.clear()
        ax.imshow(grid, cmap="coolwarm", origin="upper")
        ax.set_xticks(range(cols))
        ax.set_yticks(range(rows))
        ax.set_title(title)
        plt.pause(0.1)

    plt.ioff()
    plt.show()

def execute_delivery(packages: List[Dict], route: List[List[str]]) -> None:
    """
    Simulate package delivery based on urgency, package weight limits, and shortest route.

    Args:
        packages (List[Dict]): List of package details.
        route (List[List[str]]): 2D map representation of the route.
    """
    start, end, package_locations = parse_route_and_packages(route, packages)

    sorted_packages = parse_packages(packages)

    for i in range(len(sorted_packages)):
        print(f"Sorted: {sorted_packages[i]}")
    
    print(f"Delivery Simulation Starts with {len(sorted_packages)} packages.")

    current_position = start
    truck_capacity = 100
    remaining_capacity = truck_capacity
    truck_contents = []

    while sorted_packages:
        for package in sorted_packages[:]:
            package_id = package['id']
            package_weight = package['weight']
            package_location = package_locations[package_id]

            if package_weight <= remaining_capacity:
                # Pick up the package
                path_to_package = a_star(route, current_position, package_location)
                print(f"Picking up Package {package_id} at {package_location}: Path {path_to_package}")
                visualize_with_animation(route, path_to_package, f"Picking up {package_id}")

                remaining_capacity -= package_weight
                truck_contents.append(package)
                sorted_packages.remove(package)
                current_position = package_location

                # Remove package from map
                route[package_location[0]][package_location[1]] = '.'

        # Deliver to warehouse
        path_to_warehouse = a_star(route, current_position, end)
        print(f"Delivering to Warehouse: Path {path_to_warehouse}")
        visualize_with_animation(route, path_to_warehouse, "Delivering to Warehouse")

        current_position = end
        remaining_capacity = truck_capacity
        truck_contents.clear()
    
    time.sleep(5)

if __name__ == "__main__":
    # List of Packages in format of dictionary in a list
    packages = [
        {"id": "PKG4", "urgency": 2, "weight": 13, "description": "A Live Body"},
        {"id": "PKG7", "urgency": 2, "weight": 12, "description": "The President"},
        {"id": "PKG6", "urgency": 3, "weight": 15, "description": "The President"},
        {"id": "PKG5", "urgency": 3, "weight": 10, "description": "An Elephant"},
        {"id": "PKG3", "urgency": 3, "weight": 7, "description": "A Secret Letter"},
        {"id": "PKG1", "urgency": 3, "weight": 3, "description": "Chinese Propaganda Books"},
        {"id": "PKG8", "urgency": 4, "weight": 13, "description": "The President"},
        {"id": "PKG9", "urgency": 5, "weight": 13, "description": "A Live Body"},
        {"id": "PKG2", "urgency": 5, "weight": 5, "description": "A Bomb"},
        {"id": "PKG10", "urgency": 5, "weight": 3, "description": "A Feather"},
    ]

    # 2D Map of route in format of matrix
    # route = [
    #     ['PKG4', '.', '.', '.', 'X', 'X', '.', 'X', 'X', 'X'],
    #     ['.', 'X', '.', '.', 'X', '.', '.', 'PKG8', '.', '.'],
    #     ['.', '.', 'PKG7', '.', '.', '.', '.', '.', 'PKG9', '.'],
    #     ['PKG10', '.', '.', '.', 'X', '.', '.', 'X', '.', 'X'],
    #     ['.', '.', '.', 'PKG2', '.', '.', '.', '.', 'X', '.'],
    #     ['.', '.', 'X', '.', '.', '.', 'X', '.', 'X', 'X'],
    #     ['.', 'PKG6', '.', '.', '.', '.', '.', '.', '.', '.'],
    #     ['X', '.', 'X', 'E', '.', '.', '.', 'PKG5', 'X', '.'],
    #     ['X', '.', '.', '.', 'S', 'X', '.', 'X', 'X', '.'],
    #     ['X', 'PKG3', '.', '.', 'PKG1', 'X', 'X', '.', '.', '.']
    # ]
    route = [
        ['X', '.', '.', '.', '.', '.', '.', 'X', 'X', 'X', '.', '.', '.', '.', '.', '.', 'X', '.', '.'],
        ['.', 'PKG4', 'X', '.', '.', '.', '.', '.', '.', '.', '.', 'X', '.', 'X', '.', '.', '.', 'X', '.'],
        ['.', '.', '.', 'X', '.', '.', '.', '.', '.', 'X', '.', '.', '.', 'X', '.', '.', 'X', 'PKG5', 'X'],
        ['X', '.', '.', '.', '.', '.', '.', 'X', '.', 'PKG1', '.', '.', '.', '.', 'X', '.', '.', 'X', '.'],
        ['X', '.', '.', '.', '.', '.', '.', 'E', '.', '.', 'X', '.', '.', '.', '.', 'X', 'X', '.', '.', '.'],
        ['X', '.', 'X', '.', 'X', '.', '.', '.', '.', '.', 'X', 'X', '.', '.', '.', '.', '.', 'X', '.', 'X'],
        ['PKG10', '.', '.', '.', '.', '.', '.', '.', 'X', '.', '.', '.', '.', '.', '.', '.', 'X', '.', '.', '.'],
        ['.', 'X', 'X', '.', '.', '.', '.', 'X', 'X', '.', 'X', '.', '.', 'X', '.', '.', '.', '.', 'X', 'X'],
        ['X', '.', 'X', '.', 'X', '.', 'X', '.', '.', 'PKG7', '.', 'X', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', 'X', '.', '.', '.', 'X', '.', '.', '.', '.', '.', '.', 'X', '.', 'X', '.', '.', '.', 'X', '.'],
        ['.', 'X', '.', 'PKG3', '.', '.', 'X', '.', '.', '.', '.', 'X', 'X', '.', '.', '.', 'X', '.', '.', '.'],
        ['X', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'X', 'X', 'X', 'X', 'X', '.', 'X', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'X', '.', 'X', '.', '.', '.', 'X', '.', 'X', '.'],
        ['.', 'X', '.', '.', 'X', '.', 'PKG8', '.', '.', 'X', 'X', '.', 'X', '.', '.', 'X', '.', '.', 'PKG6', '.'],
        ['.', '.', '.', '.', '.', 'X', '.', '.', '.', '.', '.', '.', 'X', '.', '.', '.', 'X', '.', '.', '.'],
        ['.', '.', 'X', '.', '.', 'X', '.', '.', '.', '.', 'X', '.', '.', '.', 'PKG2', '.', 'X', '.', '.', '.'],
        ['.', '.', 'X', 'X', 'X', 'X', 'X', '.', '.', 'X', 'X', '.', '.', '.', '.', '.', 'X', '.', '.', '.'],
        ['X', '.', '.', 'X', 'X', '.', 'X', 'X', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'X'],
        ['S', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'X', '.', 'X', '.', 'X', '.', '.', 'X', '.'],
        ['.', '.', '.', '.', 'PKG9', '.', '.', '.', '.', '.', '.', 'X', '.', '.', '.', 'X', 'X', '.', '.', 'X'],
    ]


    execute_delivery(packages, route)
