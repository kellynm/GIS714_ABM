from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from .model import DiseaseSpread

COLORS = {"Fine": "#00AA00",
          "Infected": "#880000",
          "Dead": "#000000"}


def disease_spread_portrayal(tree):
    if tree is None:
        return
    portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
    (x, y) = tree.get_pos()
    portrayal["x"] = x
    portrayal["y"] = y
    portrayal["Color"] = COLORS[tree.condition]
    return portrayal


canvas_element = CanvasGrid(disease_spread_portrayal, 100, 100, 500, 500)
tree_chart = ChartModule([{"Label": label, "Color": color} for (label, color) in COLORS.items()])

model_params = {
    "height": 100,
    "width": 100,
    "density": UserSettableParameter("slider", "Tree density", 0.65, 0.01, 1.0, 0.01),
    "steps_to_mortality": UserSettableParameter("slider", "Steps to mortality", 3, 1, 8, 1),
    "infection_rate": UserSettableParameter("slider", "Infection Rate", 0.60, 0.01, 1.0, 0.01),
    "max_distance": UserSettableParameter("slider", 'Max spread distance', 3, 1, 10, 1),
    "wind": UserSettableParameter('choice', 'Prevailing wind direction', value='N',
                                  choices=['N', 'S', 'E', 'W']),
    "cluster_size": UserSettableParameter("slider", "Initial infection size", 3, 1, 10, 1)
}
server = ModularServer(DiseaseSpread, [canvas_element, tree_chart], "Disease Spread", model_params)
