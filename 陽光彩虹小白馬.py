# Importing Python module
import heapq
import matplotlib.pyplot as plt
import numpy as np
import time
import webbrowser
import tkinter as tk
from tkinter import *
from tkinter import messagebox as mb
from typing import List, Dict, Tuple

# Function to show a pop-up box when Mr Brown encounters a package ... possibly from a ChingChong ?
def MsgBox():
    """
    Messagebox function from Tkinter module

    """
    res=mb.askquestion('Oh? A suprise', 'You might want to open this package')
    if res == 'yes' :
        webbrowser.open('https://www.youtube.com/embed/_TiSUBMCJ90?autoplay=1')
    else :
        mb.showwarning('Alert', 'Social credits -1')

# Function to calculate Manhattan distance between two points (distance between two points in a grid-like path)
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

# Function to parse and sort the package list based on urgency (ascending)
def parse_packages(package_list: List[Dict]) -> List[Dict]:
    """
    Parse and sort the package list based on urgency (ascending).
    Within the same urgency, sort by weight (descending).

    Args:
        package_list (List[Dict]): List of package details.

    Returns:
        List[Dict]: Sorted package list.
    """
    # Sorting by bringing the urgent and heavier packages to the front in the list
    return sorted(package_list, key=lambda x: (x['urgency'], -x['weight']))     

# Function to identify start, end points, and package locations
def parse_route_and_packages(route: List[List[str]], packages: List[Dict]) -> Tuple[Tuple[int, int], Tuple[int, int], Dict[str, Tuple[int, int]]]:
    """
    Parse the route to identify start, end points, and package locations.

    Args:
        route (List[List[str]]): 2D map representation of the route.
        packages (List[Dict]): List of package details.

    Returns:
        Tuple[Tuple[int, int], Tuple[int, int], Dict[str, Tuple[int, int]]]: Coordinates of the start, end points, and package locations.
    """

    # Initialize the variables with null values
    start, end = None, None
    package_locations = {}

    # Loop to read each cell in route matrix
    for i, row in enumerate(route):
        for j, cell in enumerate(row):
            # Identify the start, end and package cell by the letter or first letter of the cell
            if cell == 'S':
                start = (i, j)
            elif cell == 'E':
                end = (i, j)
            elif cell.startswith('P'):
                package_locations[cell] = (i, j)    # Storing based on the id of the package

    # Returning error if did not detect the the start and end points
    if not start or not end:
        raise ValueError("Route must contain start (S) and end (E) points.")

    return start, end, package_locations

# Function to find the shortest path between start and end. Uses Heap queue algorithm to assist the process.
def a_star(route: List[List[str]], start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
    """
    Implement A* algorithm to find the shortest path between start and end.

    Args:
        route (List[List[str]]): 2D map of the route.
        start (Tuple[int, int]): Starting coordinates. Eg. start, current position after pickup or unload
        end (Tuple[int, int]): Ending coordinates. Eg. warehouse, package location

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

# Function to visualize the path
def visualize_with_animation(route: List[List[str]], path: List[Tuple[int, int]], ax, truck_contents=None, total_weight=0, running_time=0):
    """
    Visualize the route and path dynamically using Matplotlib.

    Args:
        route (List[List[str]]): 2D grid map of the route.
        path (List[Tuple[int, int]]): Path to visualize.
        ax: Matplotlib axis object for plotting.
        truck_contents (List[str], optional): Descriptions of items in the truck.
        total_weight (int, optional): Total weight of items in the truck.
        running_time (float, optional): Total running time of the simulation.
    """
    # Creating Grid and Setting Cell
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

    # Display Brown's location
    for r, c in path:
        grid[r][c] = 1
        ax.clear()
        ax.imshow(grid, cmap="coolwarm", origin="upper")
        ax.set_xticks(range(cols))
        ax.set_yticks(range(rows))

        # Display what Brown is handling and the cumulative running time
        if truck_contents:
            contents_str = ", ".join(truck_contents)
            ax.set_title(f"Currently handling: {contents_str}\nTotal weight: {total_weight}kg\nRunning time: {running_time:.1f}s")
        else:
            ax.set_title(f"Running time: {running_time:.1f}s")
        plt.pause(0.1)

def visualize_path(route: List[List[str]], path: List[Tuple[int, int]]) -> List[List[str]]:
    """
    Visualize the path taken on the route grid.

    Args:
        route (List[List[str]]): Original 2D map of the route.
        path (List[Tuple[int, int]]): List of coordinates in the path.

    Returns:
        List[List[str]]: Updated 2D map with the path visualized.
    """
    visualized_route = [row[:] for row in route]  # Make a deep copy of the route
    for r, c in path:
        if visualized_route[r][c] not in ['S', 'E']:  # Avoid overwriting Start or End points
            visualized_route[r][c] = 'P'
    return visualized_route

def display_route(route: List[List[str]]) -> None:
    """
    Display the 2D route in a visually friendly format.

    Args:
        route (List[List[str]]): 2D map of the route.
    """

    for row in route:
        print(" ".join(row))
    print("\n")

# Function to simulate package delivery based on urgency, package weight limits, and shortest route
def execute_delivery(packages: List[Dict], route: List[List[str]]) -> None:
    """
    Simulate package delivery based on urgency, package weight limits, and shortest route.

    Args:
        packages (List[Dict]): List of package details.
        route (List[List[str]]): 2D map representation of the route.
    """
    # Finding the coordinates of start, end and all packages, then sorting based on urgency and weight
    start, end, package_locations = parse_route_and_packages(route, packages)
    sorted_packages = parse_packages(packages)
    
    for i in range(len(sorted_packages)):
        print(f"Sorted: {sorted_packages[i]}")

    print(f"Delivery Simulation Starts with {len(sorted_packages)} packages.")

    # Initializing Mr Brown's truck position, capacity, content and running time
    current_position = start
    truck_capacity = 20
    remaining_capacity = truck_capacity
    truck_contents = []
    total_running_time = 0

    # Starting interative mode for figure in matplot and setting the figure dimensions
    plt.ion()
    fig, ax = plt.subplots(figsize=(8, 8))

    # Loop until all packages are delivered to warehouse
    while sorted_packages:
        for package in sorted_packages[:]:
            package_id = package['id']
            package_weight = package['weight']
            package_description = package['description']
            package_location = package_locations[package_id]

            #  Ensure the truck is not overloaded
            if package_weight <= remaining_capacity:
                # Pick up the package
                path_to_package = a_star(route, current_position, package_location)
                print(f"Path Taken: {path_to_package}")

                # Visualize the path on the map
                visualized_route = visualize_path(route, path_to_package)
                display_route(visualized_route)

                for step in path_to_package:
                    total_running_time += (truck_capacity + 1 - remaining_capacity) * 0.1
                    time.sleep((truck_capacity + 1 - remaining_capacity) * 0.1)  # Simulate the moving time
                    visualize_with_animation(route, [step], ax, truck_contents, truck_capacity - remaining_capacity, total_running_time)

                time.sleep(package_weight * 0.1)  # Pickup time proportional to weight

                # Displaying what Brown is handling
                print(f"Picked up Package {package_id} at {package_location}")
                truck_contents.append(package_description)
                remaining_capacity -= package_weight
                sorted_packages.remove(package)

                current_position = package_location

                # Remove package from map
                route[package_location[0]][package_location[1]] = '.'

                # Easter Egg
                # if package_description == 'Chinese Propaganda Books':
                #     MsgBox()

        # Deliver to warehouse
        path_to_warehouse = a_star(route, current_position, end)
        print(f"Path Taken: {path_to_warehouse}")

        # Visualize the path on the map
        visualized_route = visualize_path(route, path_to_warehouse)
        display_route(visualized_route)

        for step in path_to_warehouse:
            total_running_time += (truck_capacity + 1 - remaining_capacity) * 0.1
            time.sleep((truck_capacity + 1 - remaining_capacity) * 0.1)  # Simulate the moving time
            visualize_with_animation(route, [step], ax, truck_contents, truck_capacity - remaining_capacity, total_running_time)

        print("Delivered to Warehouse")
        time.sleep((truck_capacity + 1 - remaining_capacity) * 0.1)  # Unloading time proportional to weight

        current_position = end
        remaining_capacity = truck_capacity
        truck_contents.clear()

    # Ending animation
    for _ in range(3):
        print("Packages delivered! All done!")
        time.sleep(0.5)

    ax.set_title("All packages delivered! Simulation complete.")
    plt.ioff()
    plt.show()

# Main
''' 
Ensure the execution of execute_delivery function only when the script is run directly, rather than when it is imported as a module into another script.
It basically isolate the main logic of the program from reusable components.
'''
if __name__ == "__main__":
    # List of Packages in format of dictionary in a list
    # packages = [
    #     {"id": "PKG001", "urgency": 3, "weight": 10, "description": "An Elephant"},
    #     {"id": "PKG002", "urgency": 5, "weight": 2, "description": "A Tiny Elephant"},
    #     {"id": "PKG003", "urgency": 1, "weight": 7, "description": "Child Labourers"},
    #     {"id": "PKG004", "urgency": 2, "weight": 4, "description": "Drinking Water"},
    #     {"id": "PKG005", "urgency": 2, "weight": 6, "description": "Chinese Propaganda Books"},
    # ]

    # 2D Map of route in format of matrix
    # route = [
    #     ['.', '.', '.', 'X', 'PKG001', '.', '.', '.', '.', '.'],
    #     ['.', 'X', '.', 'X', '.', 'X', '.', '.', '.', '.'],
    #     ['.', 'PKG005', '.', '.', '.', '.', '.', 'X', '.', '.'],
    #     ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
    #     ['X', 'X', '.', 'X', '.', 'X', '.', 'X', '.', '.'],
    #     ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
    #     ['X', 'X', 'X', 'X', 'X', '.', 'PKG002', '.', '.', '.'],
    #     ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
    #     ['.', 'E', '.', '.', '.', 'X', 'X', 'X', 'PKG003', 'X'],
    #     ['.', '.', 'PKG004', '.', '.', '.', '.', '.', '.', '.'],
    # ]

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
    route = [
        ['PKG4', '.', '.', '.', 'X', 'X', '.', 'X', 'X', 'X'],
        ['.', 'X', '.', '.', 'X', '.', '.', 'PKG8', '.', '.'],
        ['.', '.', 'PKG7', '.', '.', '.', '.', '.', 'PKG9', '.'],
        ['PKG10', '.', '.', '.', 'X', '.', '.', 'X', '.', 'X'],
        ['.', '.', '.', 'PKG2', '.', '.', '.', '.', 'X', '.'],
        ['.', '.', 'X', '.', '.', '.', 'X', '.', 'X', 'X'],
        ['.', 'PKG6', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['X', '.', 'X', 'E', '.', '.', '.', 'PKG5', 'X', '.'],
        ['X', '.', '.', '.', 'S', 'X', '.', 'X', 'X', '.'],
        ['X', 'PKG3', '.', '.', 'PKG1', 'X', 'X', '.', '.', '.']
    ]

    # Excute the simulation
    execute_delivery(packages, route)
