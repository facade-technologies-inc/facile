"""
..
    /------------------------------------------------------------------------------\
    |                 -- FACADE TECHNOLOGIES INC.  CONFIDENTIAL --                 |
    |------------------------------------------------------------------------------|
    |                                                                              |
    |    Copyright [2019] Facade Technologies Inc.                                 |
    |    All Rights Reserved.                                                      |
    |                                                                              |
    | NOTICE:  All information contained herein is, and remains the property of    |
    | Facade Technologies Inc. and its suppliers if any.  The intellectual and     |
    | and technical concepts contained herein are proprietary to Facade            |
    | Technologies Inc. and its suppliers and may be covered by U.S. and Foreign   |
    | Patents, patents in process, and are protected by trade secret or copyright  |
    | law.  Dissemination of this information or reproduction of this material is  |
    | strictly forbidden unless prior written permission is obtained from Facade   |
    | Technologies Inc.                                                            |
    |                                                                              |
    \------------------------------------------------------------------------------/

This module contains the Entity class.
"""


import time
from PySide2.QtCore import QObject, Signal

class Entity(QObject):
	"""
	This class is the abstract super class for the Component and VisibilityBehavior classes.
	It defines a unique id for entities that are created, and has a properties object.
	"""
	count: int = 0  # Class variable used to uniquely identify every entity created.
	updated = Signal()
	onCreation = None # If not None, this is a function that will be called when an entity is created.

	def __init__(self):
		"""
		Constructs an Entity object.  Note: This is an abstract class, so this constructor is used
		only by the constructors of Entity's sub-classes.

		:return: The constructed Entity
		:rtype: Entity
		"""
		QObject.__init__(self)
		Entity.count += 1
		self._id: int = Entity.count
		self._properties = None

		if Entity.onCreation:
			Entity.onCreation()
	
	def getId(self) -> int:
		"""
		Gets the unique id for the entity.

		:return: The id for entity.
		:rtype: int
		"""
		
		return self._id
	
	def getProperties(self) -> None:
		"""
		Gets the entity's Properties object.

		:return: The entity's Properties object.
		:rtype: Properties
		"""
		
		return self._properties
	
	def setProperties(self, propertiesObj: 'Properties') -> None:
		"""
		Sets the Properties object for the entity.

		:param propertiesObj: The properties object to be associated with the entity.
		:type propertiesObj: Properties
		:return: None
		:rtype: NoneType
		"""
		
		self._properties = propertiesObj
		
	def getName(self) -> str:
		"""
		Gets the name of this entity.
		
		:return: the name of the entity
		:rtype: str
		"""
		return self.getProperties().getProperty("Name")[1].getValue()
	
	def setName(self, newName:str) -> None:
		"""
		Set the name of this entity.
		
		:param newName: The new name of the entity.
		:type newName: str
		:return: None
		:rtype: NoneType
		"""
		self.getProperties().getProperty("Name")[1].setValue(newName)
	
	def getAnnotation(self) -> str:
		"""
		Gets the annotation for this Entity. The annotation is given by the user.

		:return: The user's comment about this entity.
		:rtype: str
		"""
		return self.getProperties().getProperty("Annotation")[1].getValue()
	
	def setAnnotation(self, annotation: str) -> None:
		"""
		Sets the annotation for this Entity. The annotation is given by the user.

		:param annotation: The user's comment about this entity.
		:type annotation: str
		"""
		return self.getProperties().getProperty("Annotation")[1].setValue(annotation)

	def triggerUpdate(self) -> None:
		"""
		Tries to emit the updated signal, but don't do anything if updated can't be emitted.
		This method shouldn't do anything if it's operating as part of an API.

		:return: None
		:rtype: NoneType
		"""
		try:
			self.updated.emit()
		except:
			print("Couldn't emit updated signal. (Assuming we're running in an API)")
