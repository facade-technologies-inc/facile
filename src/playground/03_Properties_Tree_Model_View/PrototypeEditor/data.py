from collections import OrderedDict

class Property:
	def __init__(self, name, value, type, readOnly=False):
		self._name = name
		self._value = value
		self._type = type
		self._readOnly = readOnly
		
	def getName(self):
		return self._name
	
	def getValue(self):
		return self._value
	
	def getType(self):
                return self._type
	
	def __str__(self):
		return "{}:{}".format(self._name, self._value)
	
	def __repr__(self):
		return str(self)


class Properties:
	def __init__(self):
                self._categories = OrderedDict()
                self._model = PropModel(self)
		
	def getCategories(self):
		return self._categories
	
	def addProperty(self, category, name, value, type, readOnly = False):
		
		if category not in self._categories.keys():
			raise Exception("{} does not exist".format(category))
		
		self._categories[category].append(Property(name, value, type, readOnly))


        def getModel(self):
            return self._model

        def getNumCategories(self):
            return len(self._categories)

        def getCategories(self):
            return list(self._categories.keys())

		
	def __str__(self):
		retStr = "/-------------------------------------------------------\n"
		for category in self._categories.keys():
			retStr += "| {} -> {}\n".format(category, self._categories[category])
		retStr += "\\-------------------------------------------------------\n"
		return retStr

		
class BaseProperties(Properties):
	def __init__(self):
		Properties.__init__(self)
		self._categories["Base"] = []
		self.addProperty("Base", "Name", "default", str)
		self.addProperty("Base", "Type", "Push Button", str)
		self.addProperty("Base", "Annotation", "", str)
		
class VisualProperties(BaseProperties):
	def __init__(self):
		BaseProperties.__init__(self)
		self._categories["Visual"] = []
		self.addProperty("Visual", "BoxColor", "black", str)
		self.addProperty("Visual", "TextColor", "black", str)
		self.addProperty("Visual", "BorderWidth", 1, int)
		self.addProperty("Visual", "X", 0, int)
		self.addProperty("Visual", "Y", 0, int)
		self.addProperty("Visual", "Width", 100, int)
		self.addProperty("Visual", "Height", 100, int)
	
class GUIComponentProperties(VisualProperties):
	def __init__(self):
		VisualProperties.__init__(self)
		self._categories["GUI Component"] = []
		self.addProperty("GUI Component", "Parent", 1, int, True)
		self.addProperty("GUI Component", "Children", [], list, True)
		
class VisibilityBehaviorProperties(VisualProperties):
	def __init__(self):
		VisualProperties.__init__(self)
		self._categories["Visibility Behavior"] = []
		self.addProperty("Visibility Behavior", "From", 1, int, True)
		self.addProperty("Visibility Behavior", "To", 1, int, True)



if __name__ == "__main__":
	mainWindow = GUIComponentProperties()
	textEdit = GUIComponentProperties()
	button1 = GUIComponentProperties()
	button2 = GUIComponentProperties()
	fileSelectorWindow = GUIComponentProperties()
	
	print(mainWindow)
	print(textEdit)
	print(button1)
	print(button2)
	print(fileSelectorWindow)
