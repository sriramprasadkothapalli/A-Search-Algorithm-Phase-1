import pygame
import math
import time
import heapq

# Initialize Pygame
pygame.init()

# Define screen dimensions
width, height = 1200, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('A*')

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)  # For the clearance
red = (255, 0, 0)  # For the obstacle space
blue = (0, 0, 255)

# Define hexagon parameters
edge_length_ncl = 150  # Edge length with no clearance
edge_length = 155.88  # Edge length with clearance
cx, cy = 650, 250  # Center of hexagon
angles = [30, 90, 150, 210, 270, 330]  # angles for vertices from the top

# Calculate the hexagon vertices without clearance
hexagon_points_no_clearance = [
    (cx + edge_length_ncl * math.cos(math.radians(angle)), cy + edge_length_ncl * math.sin(math.radians(angle)))
    for angle in angles
]

clearance = int(input("Enter clearance(5mm): "))

# Calculate the hexagon vertices with clearance
hexagon_points = [
    (cx + (edge_length + clearance) * math.cos(math.radians(angle)), cy + (edge_length + clearance) * math.sin(math.radians(angle)))
    for angle in angles
]

def draw_scene(screen):
    # Fill the screen with black color
    screen.fill(black)
    # Draw the rectangle with clearance
    clearance_rectangles = [
        (100 - clearance, 0 - clearance, 75 + (2 * clearance), 400 + (2 * clearance)),  # Left vertical
        (275 - clearance, 100 - clearance, 75 + (2 * clearance), 400 + (2 * clearance)),  # Right vertical
        (900 - clearance, 50 - clearance, 200 + (2 * clearance), 75 + (2 * clearance)),  # Bottom horizontal
        (1020 - clearance, 50 - clearance, 80 + (2 * clearance), 400 + (2 * clearance)),  # Right vertical small
        (900 - clearance, 375 - clearance, 200 + (2 * clearance), 75 + (2 * clearance))  # Top horizontal
    ]
    for rect in clearance_rectangles:
        pygame.draw.rect(screen, green, rect)

    # Draw the hexagon with clearance
    pygame.draw.polygon(screen, green, hexagon_points)

    # Draw the rectangle without clearance (red color)
    no_clearance_rectangles = [
        (100, 0, 75, 400),  # Left vertical
        (275, 100, 75, 400),  # Right vertical
        (900, 50, 200, 75),  # Bottom horizontal
        (1020, 50, 80, 400),  # Right vertical small
        (900, 375, 200, 75)  # Top horizontal
    ]
    for rect in no_clearance_rectangles:
        pygame.draw.rect(screen, red, rect)

    # Draw the hexagon without clearance (red color)
    pygame.draw.polygon(screen, red, hexagon_points_no_clearance)

    # Draw the lines at 5mm distance from each corner
    # Draw the lines and fill the areas with green
    lines = [
        (0, 0, clearance, height),  # Left line
        (0, 0, width, clearance),  # Top line
        (width - clearance, 0, clearance, height),  # Right line
        (0, height - clearance, width, clearance)  # Bottom line
    ]
    for line in lines:
        pygame.draw.rect(screen, green, line)


def get_valid_input(prompt, robot_radius, clearance):
    while True:
        try:
            x = int(input(prompt + " X coordinate: "))
            y = int(input(prompt + " Y coordinate: "))
            theta = int(input(prompt + " angle (theta): "))
            y = height - y
            if not (0 <= x <= 1200 and 0 <= y <= 500):
                raise ValueError("Coordinates out of bounds")
            elif point_inside_hexagon(x, y, hexagon_points):
                raise ValueError("Coordinates within hexagon obstacle space")
            elif point_inside_rectangle(x, y, robot_radius):
                raise ValueError("Coordinates within rectangle obstacle space")
            return x, y, theta  # Adjust y-coordinate
        except ValueError as e:
            print("Invalid input:", e)


def point_inside_hexagon(x, y, hexagon_points):
    # Initialize winding number
    winding_number = 0

    # Iterate through each edge of the hexagon
    for i in range(len(hexagon_points)):
        # Define the current and next vertex of the edge
        current_vertex = hexagon_points[i]
        next_vertex = hexagon_points[(i + 1) % len(hexagon_points)]

        # Check if the point is above the edge
        if current_vertex[1] <= y < next_vertex[1] or next_vertex[1] <= y < current_vertex[1]:
            # Calculate the intersection point with the edge
            intersection_x = (next_vertex[0] - current_vertex[0]) * (y - current_vertex[1]) / (
                        next_vertex[1] - current_vertex[1]) + current_vertex[0]

            # Update the winding number based on the intersection point
            if x < intersection_x:
                winding_number += 1

    # Return True if winding number is odd (point is inside hexagon), False otherwise
    return winding_number % 2 == 1

def point_inside_rectangle(x, y, robot_radius):
    # Define boundaries of each rectangular obstacle
    rectangle_boundaries = [
        (100 - clearance - robot_radius, 0, 175 + clearance + robot_radius, 400 + robot_radius + clearance),
        # Rectangle 1
        (275 - clearance - robot_radius, 100 - clearance - robot_radius, 350 + clearance + robot_radius, 500),
        # Rectangle 2
        (900 - clearance - robot_radius, 50 - clearance - robot_radius, 1100 + clearance + robot_radius,
         125 + robot_radius + clearance),  # Rectangle 3
        (1020 - clearance - robot_radius, 50 - clearance - robot_radius, 1100 + clearance + robot_radius,
         450 + robot_radius + clearance),
        # Rectangle 4
        (900 - clearance - robot_radius, 375 - clearance - robot_radius, 1100 + clearance + robot_radius,
         450 + robot_radius + clearance),
        # Rectangle 5
        (0, 0, robot_radius + clearance, height),  # Left boundary
        (0, 0, width, robot_radius + clearance),  # Top boundary
        (width - robot_radius - clearance, 0, width, height),  # Right boundary
        (0, height - robot_radius - clearance, width, height)  # Bottom boundary
    ]

    # Check if the point lies inside any of the rectangles or boundaries
    for rect in rectangle_boundaries:
        if rect[0] <= x <= rect[2] and rect[1] <= y <= rect[3]:
            return True  # Point is inside the rectangle
    return False  # Point is not inside any rectangle


def draw_point_with_orientation(surface, point, orientation_deg, color):
    # Draw point
    pygame.draw.circle(surface,color, point[:2], 5)  # Draw point

    # Draw robot orientation line
    orientation_rad = math.radians(orientation_deg)
    end_x = point[0] + 5 * math.cos(orientation_rad)  # Assuming 5mm radius for the robot
    end_y = point[1] + 5 * math.sin(orientation_rad)
    pygame.draw.line(surface, red, point[:2], (end_x, end_y), 2)  # Draw line representing robot orientation

# Get input points
robot_radius = int(input("Enter robot radius(5mm): "))
start_point = get_valid_input("Enter start", robot_radius, clearance)
start_theta = start_point[2]
end_point = get_valid_input("End point", robot_radius, clearance)
end_theta = end_point[2]
L = float(input("Enter the step size (L): "))

# Actions
def move_straight(x, y, theta, L):
    """Move straight without changing orientation"""
    new_x = x + L * math.cos(math.radians(theta))
    new_y = y + L * math.sin(math.radians(theta))
    return new_x, new_y, theta

def turn_left_30(x, y, theta, L):
    """Turn left by 30 degrees and move forward"""
    new_theta = (theta + 30) % 360
    new_x = x + L * math.cos(math.radians(new_theta))
    new_y = y + L * math.sin(math.radians(new_theta))
    return new_x, new_y, new_theta

def turn_left_60(x, y, theta, L):
    """Turn left by 60 degrees and move forward"""
    new_theta = (theta + 60) % 360
    new_x = x + L * math.cos(math.radians(new_theta))
    new_y = y + L * math.sin(math.radians(new_theta))
    return new_x, new_y, new_theta

def turn_right_30(x, y, theta, L):
    """Turn right by 30 degrees and move forward"""
    new_theta = (theta - 30) % 360
    new_x = x + L * math.cos(math.radians(new_theta))
    new_y = y + L * math.sin(math.radians(new_theta))
    return new_x, new_y, new_theta

def turn_right_60(x, y, theta, L):
    """Turn right by 60 degrees and move forward"""
    new_theta = (theta - 60) % 360
    new_x = x + L * math.cos(math.radians(new_theta))
    new_y = y + L * math.sin(math.radians(new_theta))
    return new_x, new_y, new_theta

actions = [move_straight, turn_left_30, turn_left_60, turn_right_30, turn_right_60]

def is_valid_point(x, y, theta):
    # Check if the point is within the boundaries of the map
    if not (0 <= x < width and 0 <= y < height):
        return False

    # Check if the point is inside any obstacle space or clearance area
    if point_inside_hexagon(x, y, hexagon_points) or point_inside_rectangle(x, y, robot_radius):
        return False
    
    # Check if the angle is within valid bounds
    if not (0 <= theta < 360):
        return False

    # If none of the above conditions are met, the point is valid
    return True

def euclidean_distance(point1, point2):
    # Calculate Euclidean distance between two points
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


# Initialize a set to store visited nodes
visited_nodes = set()

def round_coordinates(x, y, theta):
    # Round coordinates to the nearest threshold
    new_x = round(x / 0.5) * 0.5
    new_y = round(y / 0.5) * 0.5
    new_theta = round(theta / 30) * 30
    return new_x, new_y, new_theta

def is_visited(x, y, theta):
    # Check if the region has been visited
    new_x, new_y, new_theta = round_coordinates(x, y, theta)
    return (int(new_x), int(new_y), int(new_theta / 30)) in visited_nodes

def mark_visited(x, y, theta):
    # Mark the region as visited
    new_x, new_y, new_theta = round_coordinates(x, y, theta)
    return visited_nodes.add((int(new_x), int(new_y), int(new_theta / 30)))

def a_star_search(start, goal):
    print("Start")
    pq = []  # Priority queue for open set
    g_score = {start: 0}  # Cost from start to node
    f_score = {start: euclidean_distance(start, goal)}  # Estimated total cost from start to goal
    heapq.heappush(pq, (f_score[start], start))  # Add the start node to the priority queue

    came_from = {}  # For path reconstruction
    update_frequency = 200  # Update visualization every 100 nodes
    nodes_processed = 0  # Counter for nodes processed

    while pq:
        current_f, current_node = heapq.heappop(pq)
        x, y, theta = current_node

        if euclidean_distance(current_node[:2], goal[:2]) <= 1.5 and theta == end_theta:
            # Goal reached
            return reconstruct_path(came_from, current_node)

        # Check if the current region has been visited
        if is_visited(x, y, theta):
            continue

        # Mark the current region as visited
        mark_visited(x, y, theta)

        for action in actions:
            # Generate successors
            new_x, new_y, new_theta = action(x, y, theta, L)

            if not is_valid_point(new_x, new_y, new_theta):
                continue  # Skip invalid or obstacle nodes

            new_cost = g_score[current_node] + L
            new_node = (new_x, new_y, new_theta)

            if new_node not in g_score or new_cost < g_score[new_node]:
                came_from[new_node] = current_node
                g_score[new_node] = new_cost
                f_score[new_node] = new_cost + euclidean_distance(new_node, goal)
                heapq.heappush(pq, (f_score[new_node], new_node))

                # Visualize the node
                draw_point_with_orientation(screen, (int(new_x), int(new_y)), new_theta, black)
                nodes_processed += 1  # Increment nodes processed counter

        # Update display for visualization effect if update frequency is reached
        if nodes_processed % update_frequency == 0:
            pygame.display.flip()

    return []  # If no path is found



def reconstruct_path(came_from, current):
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.append(current)  # Add the start node
    return path[::-1]  # Return reversed path

def draw_path(surface, path):
    for i in range(len(path) - 1):
        # Draw line segment between consecutive points in the path
        pygame.draw.line(surface, blue, path[i][:2], path[i + 1][:2], 3)


# Main Loop
running = True
path_found = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    start = time.time()
    draw_scene(screen)

    # Draw start and end points with robot orientation
    draw_point_with_orientation(screen, start_point, start_theta, white)  # Start point with orientation
    draw_point_with_orientation(screen, end_point, end_theta, white)  # End point with orientation

    # Visualize node exploration and the shortest path
    if not path_found:  # Replace this condition with your start search condition
        print("Start search")
        path = a_star_search(start_point, end_point)
        if path:
            draw_path(screen, path)
            path_found = True
        else:
            print("No path found")

    pygame.display.flip()

    end = time.time()
    print("Time taken = ", (end - start) / 60, " min")

    if path_found:
        pygame.time.delay(10000)
        break


pygame.quit()
print("End")

