import sys
import math


def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def calculate_angle(x1, y1, x2, y2):
    return math.atan2(y2 - y1, x2 - x1)


class Pod:
    def __init__(self, x, y, vx, vy, angle, next_checkpoint_id, boost_available=True):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.angle = angle
        self.next_checkpoint_id = next_checkpoint_id
        self.boost_available = boost_available

    def update(self, data):
        self.x, self.y, self.vx, self.vy, self.angle, self.next_checkpoint_id = data

    def speed(self):
        return math.sqrt(self.vx ** 2 + self.vy ** 2)

    def speed_direction(self):
        norm = math.sqrt(self.vx ** 2 + self.vy ** 2)
        if norm == 0:
            return 0, 0
        return self.vx / norm, self.vy / norm
    
    def calc_future_position(self, steps):
        future_x, future_y = self.x, self.y
        future_vx, future_vy = self.vx, self.vy
        future_ax, future_ay = getattr(self, "ax", 0), getattr(self, "ay", 0)  # Utilisation de l'accélération si elle est définie

        for _ in range(steps):
            future_x += future_vx
            future_y += future_vy
            future_vx += future_ax
            future_vy += future_ay

        return future_x, future_y

    


def calc_target_position(x, y, next_checkpoint_x, next_checkpoint_y, radius):
    angle_to_checkpoint = calculate_angle(x, y, next_checkpoint_x, next_checkpoint_y)
    target_x = next_checkpoint_x + radius * math.cos(angle_to_checkpoint)
    target_y = next_checkpoint_y + radius * math.sin(angle_to_checkpoint)
    return target_x, target_y


def adjust_target_position(target_x, target_y, speed, speed_direction):
    adjust_factor = OFFSET_COEF * speed / max_speed
    dx, dy = speed_direction
    adjusted_x = target_x - dx * adjust_factor
    adjusted_y = target_y - dy * adjust_factor
    return adjusted_x, adjusted_y


def go_next_checkpoint(map_memory, next_cp_id, checkpoint_count):
    if next_cp_id == checkpoint_count - 1:
        return map_memory[0]
    else:
        return map_memory[next_cp_id + 1]


def calculate_distance_threshold(speed):
    distance_threshold = speed * THRESHOLD_COEF
    if distance_threshold > MAX_DISTANCE:
        distance_threshold = MAX_DISTANCE
    return distance_threshold


def is_opponent_close(pod_x, pod_y, opponents):
    for opponent in opponents:
        if distance(pod_x, pod_y, opponent.x, opponent.y) < 1000:
            return True
    return False


# Initialisation
laps = int(input())
checkpoint_count = int(input())
map_memory = []
for i in range(checkpoint_count):
    checkpoint_x, checkpoint_y = [int(j) for j in input().split()]
    map_memory.append((checkpoint_x, checkpoint_y))

checkpoint_radius = 600
max_speed = 961
while_count = 0

OFFSET_COEF = 3000
MAX_DISTANCE = 2500
THRESHOLD_COEF = 4
BOOST_WAIT = 15

pods = [Pod(0, 0, 0, 0, 0, 0), Pod(0, 0, 0, 0, 0, 0)]
opponents = [Pod(0, 0, 0, 0, 0, 0), Pod(0, 0, 0, 0, 0, 0)]

# Boucle principale
while True:
    while_count += 1

    for i in range(2):
        pods[i].update([int(j) for j in input().split()])

    for i in range(2):
        opponents[i].update([int(j) for j in input().split()])

    # Logique pour chaque pod
    for i, pod in enumerate(pods):
        x, y, vx, vy, pod_angle, next_checkpoint_id = pod.x, pod.y, pod.vx, pod.vy, pod.angle, pod.next_checkpoint_id

        # Calcul des variables
        next_checkpoint_x, next_checkpoint_y = map_memory[next_checkpoint_id]
        next_checkpoint_dist = distance(x, y, next_checkpoint_x, next_checkpoint_y)
        speed = pod.speed()
        speed_direction = pod.speed_direction()

        # Détermination de la position cible
        threshold = calculate_distance_threshold(speed)
        if next_checkpoint_dist < threshold:
            next_checkpoint_x, next_checkpoint_y = go_next_checkpoint(map_memory, next_checkpoint_id, checkpoint_count)

        target_x, target_y = calc_target_position(x, y, next_checkpoint_x, next_checkpoint_y, checkpoint_radius)
        target_x, target_y = adjust_target_position(target_x, target_y, speed, speed_direction)

        # Gestion de l'angle
        angle_to_checkpoint = calculate_angle(x, y, next_checkpoint_x, next_checkpoint_y)
        next_checkpoint_angle = math.degrees(angle_to_checkpoint) - pod_angle
        next_checkpoint_angle = (next_checkpoint_angle + 360) % 360
        if next_checkpoint_angle > 180:
            next_checkpoint_angle -= 360

        # Détermination de l'action
        if is_opponent_close(x, y, opponents) and next_checkpoint_dist < 1000:
            boost = "SHIELD"
        elif (i == 0 or while_count > BOOST_WAIT) and abs(next_checkpoint_angle) < 2 and next_checkpoint_dist > 4000 and pod.boost_available:
            boost = "BOOST"
            pod.boost_available = False
        elif abs(next_checkpoint_angle) < 45:
            boost = "100"
        elif abs(next_checkpoint_angle) < 65:
            boost = "66"
        else:
            boost = "0"

        # Debugging
        print(f"--- POD {i + 1} --- Position: ({x}, {y}), Speed: {speed}", file=sys.stderr)
        print(f"Target: ({int(target_x)}, {int(target_y)}), Boost: {boost}", file=sys.stderr)

        # Commandes
        print(f"{int(target_x)} {int(target_y)} {boost}")
