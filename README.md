# What-Can-Brown-Do-For-You
Smart Delivery Solution: Route Optimization and Package Handling

## Project Details

| **Title**                         | Content         |
| ---                               | ---             |
| **Author**                        | Chuah Jong Lik  |
| **Cumulative Development Time**   | About 8 hours <br/> excluding documentation time |
| **Progamming language**:          | Python          |

**Challenges**:
- Simulating the movement time
- Making the animation continous without overlapping

## Overview of the Code

This program simulates a delivery scenario where a delivery person picks up packages from various points on a 2D map and delivers them to a warehouse based on their urgency and weight, while adhering to weight limits. The delivery is visualized with dynamic animations, showing the paths taken and the state of the delivery truck at each step.

#### Key Features:

1. **Package Handling**:
   - Packages are sorted by **urgency** (ascending) and within the same urgency by **weight** (descending).
   - Packages are picked up only if their weight fits within the remaining capacity of the truck.

2. **Pathfinding**:
   - Uses the **A* algorithm** to compute the shortest path between two points on the map.
   - Supports diagonal movement if it's unblocked.

3. **Visualization**:
   - Real-time, animated updates of the route, showing the movement of the delivery person on the map.
   - Displays information such as:
     - Contents of the truck (using the descriptions of packages).
     - The total weight of the current load.
     - The total running time of the simulation.

4. **Time Simulation**:
   - Pickup time is proportional to package weight (`0.5 * weight` seconds).
   - The speed of moving between grid points depends on the total weight of packages being handled (`0.2 * (weight + 1)` seconds per unit block).

5. **Dynamic Map Updates**:
   - When a package is picked up, it is removed from the map, unblocking the grid space.
   - Paths are recalculated after every change to the map.

6. **Cool Ending Animation**:
   - A brief celebratory message and animation are shown once all packages are successfully delivered.

#### Example Output:
- Animated visualization showing the movement through the grid.
- Console logs tracking pickups, deliveries, and remaining capacity.
- Final map state displayed after completing the simulation.

This approach efficiently handles multiple deliveries with varying priorities, provides clear insights via animations, and simulates realistic timing constraints for package handling and movement.

## Code Operation
### Additional Packages Used:
- matplotlib
- numpy

### Brief Execution Flow:
1. **Parsing Inputs**:
   - The package list and map are parsed to extract information like the starting point, end point, and package locations.
2. **Delivery Simulation**:
   - The delivery person starts at the designated starting point and moves sequentially to pick up packages based on the sorted list.
   - After reaching the capacity limit or exhausting the sorted package list, the delivery person travels to the warehouse to unload.
3. **Animation and Visualization**:
   - Every movement, package pickup, and delivery step is dynamically visualized, providing real-time feedback.

### Detailed Execution Flow:
1. **The Very First Thing:**
   - Storing packages list and route: `packages: List[Dict], route: List[List[str]}`
   - `execute_delivery(packages, route)` function is called to start the simulation.

2. **Identifying Start, End Points, and Package Locations**
   - Now inside `execute_delivery(packages, route)` function,

      `start, end, package_locations = parse_route_and_packages(route, packages)`: Calling `parse_route_and_packages()` function to get coordinates of the start, end points, and each package locations.
   - Inside `parse_route_and_packages()` function, 
      ```python
      for i, row in enumerate(route):
        for j, cell in enumerate(row):
            # Identify the start, end and package cell by the letter or first letter of the cell
            if cell == 'S':
                start = (i, j)
            elif cell == 'E':
                end = (i, j)
            elif cell.startswith('P'):
                package_locations[cell] = (i, j)    # Storing based on the id of the package
      ```
      Looping is done to identify the start, end and all package cells by matching the first letter of the cell.

      Then, once the start, end and all package cells are identified, it will be stored and returned. If the start and end points failed to be located, it will return an error.

3. **Parsing and sorting the package list based on urgency (1: urgent, 5: not urgent)**
   - `sorted_packages = parse_packages(packages)` is used to store the list of sorted/ arranged package list based on urgency and weight.
   - `sorted()` function is used for the sorting process by prioritising the urgent and heavier packages.

4. **Initializing Mr Brown's truck position, capacity, content and running time**
   ```python
      current_position = start
      truck_capacity = 10
      remaining_capacity = truck_capacity
      truck_contents = []
      total_running_time = 0
   ```
   This will set Brown's truck position to the starting point previously identified and set how much unit weight can the truck handle and how much it still can handle (i.e. <= 10). The other variables are used for displaying the packages the truck are handling and the current cumulative running time.

5. **Initializing the matplot figure**
   ```python
      plt.ion()
      fig, ax = plt.subplots(figsize=(8, 8))
   ```
   This enables the interative mode of the figure so that the animation is continous. `figsize=(8, 8)` will set the size of the map. **These values need be changed if you wants a visually bigger or smaller figure**.

6. **Simulating pathplannning** 
   - `while sorted_packages:` is used to ensure the all code will loop until all packages is fully removed (delivered). 
   - `for package in sorted_packages[:]` as the variable name suggests, the packages to be picked up first are based on urgency and weight with no limitations on the total number of packages to be handled.
   - `if package_weight <= remaining_capacity:` is used to ensure the truck is not overloaded.
   - `a_star(route, current_position, package_location)` function is called to determine the shortest possible path to reach to the target package and also to the warehouse (end point). Heap queue algorithm is used to find the shortest path.
   - matplotlib is then used to visualize the movement and the map.


## References
- Our Favourite Assistant, ChatGPT ✨
- https://www.w3schools.com/
- https://www.markdownguide.org/
- https://docs.python.org/3/library/
- https://www.learnbyexample.org/
- https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-tables