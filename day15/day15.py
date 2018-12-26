import sys
from queue import PriorityQueue, Queue
from collections import defaultdict
from copy import deepcopy
from time import time
from random import shuffle

class Unit:

  def __init__(self, kind, pos, elf_power):
    self.kind = kind
    self.enemy = "G" if kind == "E" else "E"
    self.pos = pos
    self.power = elf_power if self.kind == "E" else 3
    self.HP = 200
    self.alive = True

  def move(self):

    # All (alive) enemies
    enemies = [x for x in units if x.kind == self.enemy and x.alive]

    # If already next to an enemy, don't move
    for enemy in enemies:
      if man_dist(self.pos, enemy.pos) == 1:
        if verbosity >= 2: print("Skip move (already next to enemy)")
        return False

    # Find all eligibile target squares (empty squares next to enemies)
    target_squares = set()
    for enemy in enemies:
      for n in cave.neighbors(enemy.pos):
        target_squares.add(n)

# ************************

    target_squares = list(target_squares)
    shuffle(target_squares)

    all_start = time()
    target_dist = None
    valid_targets = []
    for target in target_squares:
      start = time()
      dist, path = cave.find_distance(self.pos, target, target_dist)
      if path is not None:
        if target_dist is None or dist < target_dist:
          valid_targets = [target]
          target_dist = dist
        elif dist == target_dist:
          valid_targets.append(target)

# ************************

    # Find path to each target square, keep those with minimum path length
    # valid_targets = []
    # min_dist = None
    # for target in target_squares:
    #   path = cave.find_path(self.pos, target)
    #   if path is not None:
    #     dist = len(path) - 1
    #     if min_dist is None or dist < min_dist:
    #       min_dist = dist
    #       valid_targets = [target]
    #     elif dist == min_dist:
    #       valid_targets.append(target)

    # Select the closest target square, breaking ties by reading order
    valid_targets.sort()
    if len(valid_targets) > 0:
      target_square = valid_targets[0]
    else:
      # No reachable target squares
      if verbosity >= 2: print("No move (no reachable target square)")
      return False

    # Determine which of the current unit's neighboring squares are
    # on the optimal path to target square
    possible_moves = []
    for neigh in cave.neighbors(self.pos):
      if man_dist(target_square, neigh) <= target_dist - 1:
        dist, path = cave.find_distance(target_square, neigh, target_dist-1)
        if path is not None:
          possible_moves.append(neigh)

    # Select next move (tie breaking as usual)
    possible_moves.sort()
    next_move = possible_moves[0]

    # Do the move
    if verbosity >= 2:
      path = cave.find_path(next_move, target_square)
      cave.show_path([self.pos] + path)
    i, j = self.pos
    cave.grid[i][j] = '.'
    i, j = next_move
    cave.grid[i][j] = self.kind
    self.pos = next_move
    if verbosity >= 2: print("Moved to", next_move)
    return True

  def attack(self):

    # Find enemies in range
    enemies_in_range = []
    for unit in units:
      if unit.alive and unit.kind == self.enemy and man_dist(self.pos, unit.pos) == 1:
        enemies_in_range.append(unit)

    if len(enemies_in_range) == 0:
      if verbosity >= 2: print("No enemies in range")
      return None

    # Determine enemy in range with lowest HP
    # Break ties by reading order
    enemies_in_range.sort(key=lambda x: (x.HP, x.pos))
    enemy = enemies_in_range[0]

    # Attack!
    if verbosity >= 2: print("Attacking", enemy)
    enemy.HP -= self.power

    return enemy


  def __repr__(self):
    kind = "Elf" if self.kind == "E" else "Goblin"
    return "%s at (%i,%i) with %i HP" % (kind, *self.pos, self.HP)

class SearchNode:
  def __init__(self, priority, pos, path):
    self.priority = priority
    self.pos = pos
    self.path = path
  def __lt__(self, other):
    return self.priority < other.priority
  def __repr__(self):
    return "<%i, %s, %s>" % (self.priority, self.pos, self.path)

def man_dist(pos1, pos2):
  return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

class Cave:

  def __init__(self, lines):
    self.grid = []
    for line in lines:
      self.grid.append(list(line.strip()))
    self.NX = len(self.grid)
    self.NY = len(self.grid[0])

  def grid_at(self, pos):
    return self.grid[pos[0]][pos[1]]

  def neighbors(self, pos, include_units=False):
    i, j = pos
    neighs = [(i+1,j), (i-1,j), (i,j+1), (i,j-1)]
    if include_units:
      valid = ['.', 'G', 'E']
    else:
      valid = ['.']
    return [n for n in neighs if self.grid_at(n) in valid]

  def find_path(self, start, goal, max_dist=None):

    min_path_dist = None
    closed_set = set()
    open_set = PriorityQueue()
    open_set.put(SearchNode(0, start, []))
    dist_so_far = defaultdict(lambda: float('inf'))
    dist_so_far[start] = 0
    if max_dist is None: max_dist = float('inf')

    while not open_set.empty():

      current = open_set.get()
      closed_set.add(current.pos)
      # print(">> Opening", current)

      if current.pos == goal:
        return [start] + current.path

      for neigh_pos in self.neighbors(current.pos):

        if neigh_pos in closed_set:
          # print("Neighbor %s already visited" % str(neigh_pos))
          continue

        # print("Checking neighbor %s" % str(neigh_pos))
        new_dist = dist_so_far[current.pos] + 1
        if new_dist <= dist_so_far[neigh_pos] and new_dist <= max_dist:
          dist_so_far[neigh_pos] = new_dist
          priority = new_dist + man_dist(neigh_pos, goal)
          new_node = SearchNode(priority, neigh_pos, current.path + [neigh_pos])
          # print("Adding", new_node)
          open_set.put(new_node)

    return None

  def find_distance(self, start, goal, max_dist=None):

    min_path_dist = None
    closed_set = set()
    open_set = PriorityQueue()
    open_set.put(SearchNode(0, start, []))
    dist_so_far = defaultdict(lambda: float('inf'))
    dist_so_far[start] = 0
    if max_dist is None: max_dist = float('inf')

    while not open_set.empty():

      current = open_set.get()
      closed_set.add(current.pos)
      # print(">> Opening", current)

      if current.pos == goal:
        path = [start] + current.path
        return (len(path)-1, path)

      for neigh_pos in self.neighbors(current.pos):

        if neigh_pos in closed_set:
          # print("Neighbor %s already visited" % str(neigh_pos))
          continue

        # print("Checking neighbor %s" % str(neigh_pos))
        child_dist = dist_so_far[current.pos] + 1
        if child_dist <= dist_so_far[neigh_pos] and child_dist <= max_dist:
          dist_so_far[neigh_pos] = child_dist
          priority = child_dist + man_dist(neigh_pos, goal)
          new_node = SearchNode(priority, neigh_pos, current.path + [neigh_pos])
          # print("Adding", new_node)
          open_set.put(new_node)

    return (float("inf"), None)



  def show_path(self, path):
    cave1 = deepcopy(self)
    i,j = path[0]
    cave1.grid[i][j] = '\033[5;36;40;1m' + cave1.grid[i][j] +'\033[0m'
    i,j = path[-1]
    cave1.grid[i][j] = '\033[1;31;43mx\033[0m'
    for i,j in path[1:-1]:
      cave1.grid[i][j] = '\033[1;36mx\033[0m'
    cave1.print()

  def print(self, active=None):
    for i in range(self.NX):
      s = ""
      for j in range(self.NY):
        if active is not None and active == (i,j):
          s += self.grid[i][j]
        elif self.grid[i][j] == 'G':
          s += self.grid[i][j]
        elif self.grid[i][j] == 'E':
          s += self.grid[i][j]
        elif self.grid[i][j] == '.':
          s += "."
        else:
          s += self.grid[i][j]
      us = []
      for j in range(self.NY):
        if self.grid[i][j] in ['E', 'G']:
          for unit in units:
            if unit.pos == (i,j):
              us.append("%s(%i)" % (self.grid[i][j], unit.HP))
      if (len(us)) > 0:
        s += "   " + ", ".join(us)
      print(s)

# ===================================

def simulate_combat(cave, units, part):

  if verbosity >= 2: cave.print()

  round = 1
  combat_ended = False
  deadlocked = False
  while True:

    round_start = time()

    if verbosity >= 1: print("--------------------------------------------------------------------")
    if verbosity >= 1:
      print("Start of round", round)
      print("Deadlocked:", repr(deadlocked))

    # Determine order of initiative
    units.sort(key=lambda x: x.pos)

    # Execute turn for each unit
    nobody_moved = True
    for unit in units:

      if not unit.alive: continue

      if verbosity >= 2: print("\nTurn:", unit)
      # if verbosity >= 2: cave.print(active=unit.pos)

      # End combat if no enemies remain
      enemies = [x for x in units if x.kind == unit.enemy and x.alive]
      if len(enemies) == 0:
        if verbosity >= 2: print("No more enemies!")
        combat_ended = True
        break

      # Move
      if not deadlocked:
        moved = unit.move()
        if moved: nobody_moved = False
      else:
        if verbosity >= 2: print("Deadlocked; skipping move")

      # Attack
      attacked = unit.attack()

      # If the attacked enemy was killed, set it as dead, clear its space
      if attacked is not None and attacked.HP <= 0:

        if verbosity >= 1: print(attacked, "\033[1;31m" + "killed" + "\033[0m")
        attacked.alive = False
        i,j = attacked.pos
        cave.grid[i][j] = '.'
        deadlocked = False
        nobody_moved = False

        if part == 2:
          if attacked.kind == "E":
            return None


      if verbosity >= 2: cave.print(active=unit.pos)

    # Remove dead units
    units = [u for u in units if u.alive]

    if combat_ended: break

    if not deadlocked and nobody_moved:
      deadlocked = True
      if verbosity >= 1: print("Entered deadlock")

    if verbosity >= 1:
      print("\nCompleted round %i in %.3f s" % (round, time()-round_start))
      cave.print()

    round += 1

  if units[0].kind == "G":
    winner = "Goblins"
  else:
    winner = "Elves"

  completed_rounds = round - 1
  HP_left = sum([x.HP for x in units])
  outcome = completed_rounds * HP_left
  if verbosity >= 1:
    print()
    cave.print()
    print()
    print(sum([x.HP for x in units]), [x.HP for x in units])
  print("\nCompleted rounds:", completed_rounds)
  print("%s win with %i total HP left" % (winner, HP_left))
  print("Outcome:", outcome)

  return outcome


# ===================================

verbosity = 1
part = 1

# Read in cave layout and unit positions from input
cave_orig = Cave(open(sys.argv[1]).readlines())

if part == 1:

  # Copy original cave
  cave = deepcopy(cave_orig)

  # Load goblins and elves, with correct power
  units = []
  elf_power = 3
  for i in range(cave_orig.NX):
    for j in range(cave_orig.NY):
      if cave_orig.grid[i][j] in ["G", "E"]:
        units.append(Unit(cave_orig.grid[i][j], (i,j), elf_power))

  # Simulate
  outcome = simulate_combat(cave, units, part=1)

elif part == 2:

  for elf_power in range(5,100+1,2):
  # for elf_power in range(4,100+1):

    # Copy original cave
    cave = deepcopy(cave_orig)

    # Load goblins and elves, with correct power
    units = []
    for i in range(cave_orig.NX):
      for j in range(cave_orig.NY):
        if cave_orig.grid[i][j] in ["G", "E"]:
          units.append(Unit(cave_orig.grid[i][j], (i,j), elf_power))

    # Simulate
    print("\nSimulating with elf power", elf_power)
    outcome = simulate_combat(cave, units, part=2)
    if outcome is None:
      print("Elves suffered loss")
    else:
      print("Elves win without losses", outcome)
      print("Elf power", elf_power)
      sys.exit()
