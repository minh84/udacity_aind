# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def generalSearch(problem, fn):
    dataStructure = {'bfs': util.Queue(), 'dfs': util.Stack()}
    root = problem.getStartState()
    try:
        visited = set()
        fringe = dataStructure[fn]
        fringe.push((root, [], 0))
        while not fringe.isEmpty():
            location, path, cost = fringe.pop()
            if problem.isGoalState(location):
                # print path
                return path
            if location not in visited:
                visited.add(location)
                for x, y, z in problem.getSuccessors(location):
                    if x not in visited:
                        fringe.push((x, path + [y], z))
        return []
    except Exception as e:
        print e
        return []

def graphSearch(problem, frontier):
  start_state = problem.getStartState()
  explored    = set()
  parents     = dict()
  parents[start_state] = None
  explored.add(start_state)
  frontier.push(start_state)

  while not frontier.isEmpty():
    top = frontier.pop()

    # if we at goal, we go backward to the origin
    if problem.isGoalState(top):
      actions = []
      curr = top
      while (parents[curr] is not None):
        curr, move = parents[curr]
        actions.append(move)
      return actions[::-1]

    for next_node, move,_ in problem.getSuccessors(top):
      if not next_node in explored:
        # push here is very important since it can change magnitude number of node to be searched
        explored.add(next_node)
        parents[next_node] = (top, move)
        frontier.push(next_node)

  # can't not find path to Goal
  return None

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first
  [2nd Edition: p 75, 3rd Edition: p 87]
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm 
  [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """
  "*** YOUR CODE HERE ***"
  # util.raiseNotDefined()

  # some debug to get started
  # print('Start state {}'.format(start_state))
  # print('Is the start a goal? {}'.format(problem.isGoalState(start_state)))
  # print('Start\'s successors: {}'.format(problem.getSuccessors(start_state)))

  # can't not find path to Goal
  return graphSearch(problem, util.Stack())

def breadthFirstSearch(problem):
  """
  Search the shallowest nodes in the search tree first.
  [2nd Edition: p 73, 3rd Edition: p 82]
  """
  "*** YOUR CODE HERE ***"
  return graphSearch(problem, util.Queue())
  # return generalSearch(problem, fn='bfs')

def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  "*** YOUR CODE HERE ***"
  # util.raiseNotDefined()
  start_state = problem.getStartState()

  priorityFn = lambda cost_node : cost_node[0]

  frontier = util.PriorityQueueWithFunction(priorityFn)
  frontier.push((0, start_state))

  # set up expolored to seen state, parents to get back the path
  explored = set()
  explored.add(start_state)

  parents = dict()
  parents[start_state] = None

  min_cost = float('inf')
  min_path = None

  while not frontier.isEmpty():
    top_cost, top_state = frontier.pop()
    # if we at goal, we go backward to the origin
    if problem.isGoalState(top_state):
      if top_cost < min_cost:
        min_cost = top_cost
        actions = []
        curr = top_state
        while (parents[curr] is not None):
          curr, move = parents[curr]
          actions.append(move)
        # update min_path
        min_path = actions[::-1]

    for next_node, move, cost in problem.getSuccessors(top_state):
      if not next_node in explored:
        explored.add(next_node)
        parents[next_node] = (top_state, move)
        frontier.push((top_cost + cost, next_node))

  return min_path

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  "*** YOUR CODE HERE ***"

  start_state = problem.getStartState()

  priorityFn = lambda cost_node: cost_node[0] + heuristic(cost_node[1], problem=problem)

  frontier = util.PriorityQueueWithFunction(priorityFn)
  frontier.push((0, start_state))

  # set up expolored to seen state, parents to get back the path
  explored = set()
  explored.add(start_state)

  parents = dict()
  parents[start_state] = None

  min_cost = float('inf')
  min_path = None

  while not frontier.isEmpty():
    top_cost, top_state = frontier.pop()


    # if we at goal, we go backward to the origin
    if problem.isGoalState(top_state):
      actions = []
      curr = top_state
      while (parents[curr] is not None):
        curr, move = parents[curr]
        actions.append(move)
      return actions[::-1]

    for next_node, move, cost in problem.getSuccessors(top_state):
      if not next_node in explored:
        explored.add(next_node)
        parents[next_node] = (top_state, move)
        frontier.push((top_cost + cost, next_node))

  return min_path

  return uniformCostSearch(problem, heuristic)

  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
