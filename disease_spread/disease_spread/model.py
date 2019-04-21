from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import Grid
from mesa.time import RandomActivation

from .agent import TreeCell


class DiseaseSpread(Model):
    """
    Simple Disease Spread model.
    """
    def __init__(self, height=100, width=100, density=0.65, steps_to_mortality=3, infection_rate=0.6, max_distance=10, wind='N', cluster_size=3):
        """
        Create a new Disease Spread model.

        Args:
            height, width: The size of the grid to model
            density: What fraction of grid cells have a tree in them.
            steps_to_mortality: The number of steps a tree remains infected before dying.
            infection_rate: The probability that infected tree will infect neighboring tree (stochasitc).
            max_distance: The maximum distance that infection can travel. Random distance traveled chosen between 1 and max distance (stochastic).
            wind: The prevailing wind direction.
            cluster_size: The size of the initial infection cluster in the grid center.

        """
        # Initialize model parameters
        self.height = height
        self.width = width
        self.density = density
        self.steps_to_mortality = steps_to_mortality
        self.infection_rate = infection_rate
        self.max_distance=max_distance
        self.wind = wind
        self.cluster_size = cluster_size

        # Set up model objects
        self.schedule = RandomActivation(self)
        self.grid = Grid(height, width, torus=False)

        self.datacollector = DataCollector(
            {"Fine": lambda m: self.count_type(m, "Fine"),
             "Infected": lambda m: self.count_type(m, "Infected"),
             "Dead": lambda m: self.count_type(m, "Dead")})

        # Place a tree in each cell with Prob = density
        center_cluster_x_max = (int(self.width / 2)) + self.cluster_size
        center_cluster_x_min = (int(self.width / 2)) - self.cluster_size
        center_cluster_y_max = (int(self.height / 2)) + self.cluster_size
        center_cluster_y_min = (int(self.height / 2)) - self.cluster_size
        for (contents, x, y) in self.grid.coord_iter():
            if self.random.random() < self.density:
                # Create a tree
                new_tree = TreeCell((x, y), self)
                # Set all trees in grid center cluster Infected.
                if center_cluster_x_min <= x <= center_cluster_x_max and center_cluster_y_min <= y <= center_cluster_y_max:
                    new_tree.condition = "Infected"
                self.grid._place_agent((x, y), new_tree)
                self.schedule.add(new_tree)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """
        Advance the model by one step.
        """
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

        # Halt if no more disease
        if self.count_type(self, "Infected") == 0:
            self.running = False

    @staticmethod
    def count_type(model, tree_condition):
        """
        Helper method to count trees in a given condition in a given model.
        """
        count = 0
        for tree in model.schedule.agents:
            if tree.condition == tree_condition:
                count += 1
        return count
