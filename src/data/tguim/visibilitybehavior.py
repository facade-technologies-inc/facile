
from data.entity import Entity


class VisibilityBehavior(Entity):
    def __init__(self):
        super().__init__()
        self._name = None # TODO: Or will this just be in the propertiesObj?
        self._toNode = None
        self._fromNode = None
        self._condition = None
        self._behaviorType = None # show or hide
        # TODO: add reference to the associated QGraphicsItem Ramos creates.

    def getName(self):
        return self._name

    def getToNode(self):
        return self._toNode

    def getFromNode(self):
        return self._fromNode

    def getCondition(self):
        return self._condition

    def setName(self, newName):
        self._name = newName

    def setToNode(self, node):
        self._toNode = node

    def setFromNode(self, node):
        self._fromNode = node

    def setCondition(self, conditionObj):
        self._condition = conditionObj

