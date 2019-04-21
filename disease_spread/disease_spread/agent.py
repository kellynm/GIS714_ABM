from mesa import Agent
import random
from random import choice

class TreeCell(Agent):
    """
    A tree cell.

    Attributes:
        x, y: Grid coordinates
        condition: Can be "Fine", "Infected", or "Dead"
        unique_id: (x,y) tuple.

    unique_id isn't strictly necessary here, but it's good
    practice to give one to each agent anyway.
    """
    def __init__(self, pos, model):
        """
        Create a new tree.
        Args:
            pos: The tree's coordinates on the grid.
            model: standard model reference for agent.
        """
        super().__init__(pos, model)
        self.pos = pos
        self.condition = "Fine"
        self.num_steps = 0

    def is_direction(self, pos1, pos2, direction):
        if direction == 'N' and (pos2[1] - pos1[1] > 0):
            return True
        if direction == 'S' and (pos2[1] - pos1[1] < 0):
            return True
        if direction == 'E' and (pos2[0] - pos1[0] > 0):
            return True
        if direction == 'W' and (pos2[0] - pos1[0] < 0):
            return True
        return False
   
    def step(self):
        """
        Randomly choose a spread distance between 1 and maximum distance (stochastic).
        If the tree is Infected, spread it to fine trees nearby at infection rate (stochastic).
        Kill trees after number of steps defined by steps_to_mortality arg.
        """
        if self.condition == "Infected":
            self.num_steps = self.num_steps + 1
            for neighbor in self.model.grid.iter_neighbors(self.pos, moore=True,
                                                           include_center=False,
                                                           radius=random.randrange(1,self.model.max_distance, 1)):
                direction = choice(self.model.wind * 2 + 'NSEW')
                if self.is_direction(self.pos, neighbor.pos, direction):
                    if neighbor.condition == "Fine":
                        if random.random() < self.model.infection_rate:
                            neighbor.condition = "Infected"
            if self.num_steps > self.model.steps_to_mortality:
                self.condition = "Dead"

    def get_pos(self):
        return self.pos
