# What-Can-Brown-Do-For-You
Pathfinding and Urgency-based Package Sorting with Current Weight Handled Limitation

### Overview of the Code

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

#### Execution Flow:
1. **Parsing Inputs**:
   - The package list and map are parsed to extract information like the starting point, end point, and package locations.
2. **Delivery Simulation**:
   - The delivery person starts at the designated starting point and moves sequentially to pick up packages based on the sorted list.
   - After reaching the capacity limit or exhausting the sorted package list, the delivery person travels to the warehouse to unload.
3. **Animation and Visualization**:
   - Every movement, package pickup, and delivery step is dynamically visualized, providing real-time feedback.

#### Example Output:
- Animated visualization showing the movement through the grid.
- Console logs tracking pickups, deliveries, and remaining capacity.
- Final map state displayed after completing the simulation.

This approach efficiently handles multiple deliveries with varying priorities, provides clear insights via animations, and simulates realistic timing constraints for package handling and movement.
