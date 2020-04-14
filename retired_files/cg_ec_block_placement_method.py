def addToExtraComponents(self, component: 'ComponentGraphics') -> None:
    """
    Adds a component to the Extra Components section, finding valid placement.
    *Only for top-level components*, doesn't do anything otherwise.
    TODO: This could probably be greatly improved in terms of runtime.

    :param component: Component to be added to extra components section
    :type component: ComponentGraphics
    :return: None
    :rtype: NoneType
    """
    
    if self._dataComponent.getParent().getParent() is None:
        if self._extraComponents:
            usedSpace = []
            for ec in self._extraComponents:
                usedSpace.append((ec.x() - ComponentGraphics.EC_MARGINS, ec.y() - ComponentGraphics.EC_MARGINS,
                                  ec.width(True), ec.height(True)))
            
            # This section gets the blocks of free space available
            maxX = self.width() - ComponentGraphics.EC_Y_PADDING  # Seems like a typo, its not. just putting small padding on right
            maxY = self.height() - ComponentGraphics.EC_Y_PADDING
            freeSpace = [(0, 0, maxX, maxY)]  # Initialize free space to the entire available block
            for us in usedSpace:
                for fs in freeSpace:  # This nested for loop is why i think this can be improved
                    spacesOverlap = us[0] < fs[0] + fs[2] and \
                                    fs[0] < us[0] + us[2] and \
                                    us[1] < fs[1] + fs[3] and \
                                    fs[1] < us[1] + us[3]
                    if spacesOverlap:  # split fs into parts, excluding the overlapped space, and add back to freespace
                        betterSpaces = self.getFreeSpace(fs, us)
                        for sp in betterSpaces:
                            freeSpace.append(sp)
                        freeSpace.pop(freeSpace.index(fs))
            
            # Now we take the free space blocks and get all the blocks' sides and vertices,
            # and if two sides are duplicated they are removed. Then, from the remaining
            # elements we have polygons defining the free space
            
            ### TODO: STOPPED HERE
            
            bestCoords = [0, 0]
        
        else:
            component.setPos(self._width + ComponentGraphics.EC_X_PADDING, ComponentGraphics.EC_Y_PADDING)
        
        component.setMargin(ComponentGraphics.EC_MARGINS)
        self.expandECSection()
        self._extraComponents.append(component)


def getFreeSpace(self, fs: tuple, us: tuple) -> list:
    """
    Gets the space in tmp that is not overlapped by us.

    :param fs: the general space containing free and used space, of the form (x, y, width, height)
    :type fs: tuple
    :param us: the used space overlapping all or part of tmp, of the form (x, y, width, height)
    :type us: tuple
    :return: new blocks of space that are unused relative to us
    :rtype: list
    """
    
    betterSpaces = []
    
    if us[0] <= fs[0] and us[1] <= fs[1] and us[2] >= fs[2] and us[3] >= fs[3]:
        return betterSpaces
    
    # Left Space
    if fs[0] < us[0]:
        betterSpaces.append((fs[0], fs[1], us[2] - fs[2], fs[3]))
    
    # Right Space
    if us[0] + us[2] < fs[0] + fs[2]:
        betterSpaces.append((us[0] + us[2], fs[1], (fs[0] + fs[2]) - (us[0] + us[2]), fs[3]))
    
    # Upper Space
    if us[1] > fs[1]:
        # if used space goes over free space on the right
        if us[0] + us[2] > fs[0] + fs[2] and us[0] > fs[0]:
            betterSpaces.append((us[0], fs[1], (fs[0] + fs[2]) - us[0], us[1] - fs[1]))
        
        # if used space goes over free space on the left
        elif us[0] < fs[0] and us[0] + us[2] < fs[0] + fs[2]:
            betterSpaces.append((fs[0], fs[1], (us[0] + us[2]) - fs[0], us[1] - fs[1]))
        
        # if it doesnt go over edges of free space in x dir
        elif us[0] + us[2] < fs[0] + fs[2] and us[0] > fs[0]:
            betterSpaces.append((us[0], fs[1], us[2], us[1] - fs[1]))
        
        else:  # goes over both edges
            betterSpaces.append((fs[0], fs[1], fs[2], us[1] - fs[1]))
    
    # Lower Space
    if us[1] + us[3] < fs[1] + fs[3]:
        # if used space goes over free space on the right
        if us[0] + us[2] > fs[0] + fs[2] and us[0] > fs[0]:
            betterSpaces.append((us[0], us[1] + us[3], (fs[0] + fs[2]) - us[0], (fs[1] + fs[3]) - (us[1] + us[3])))
        
        # if used space goes over free space on the left
        elif us[0] < fs[0] and us[0] + us[2] < fs[0] + fs[2]:
            betterSpaces.append((fs[0], us[1] + us[3], (us[0] + us[2]) - fs[0],
                                 (fs[1] + fs[3]) - (us[1] + us[3])))
        
        # if it doesnt go over edges of free space in x dir
        elif us[0] + us[2] < fs[0] + fs[2] and us[0] > fs[0]:
            betterSpaces.append((us[0], us[1] + us[3], us[2], (fs[1] + fs[3]) - (us[1] + us[3])))
        
        else:  # goes over both edges
            betterSpaces.append((fs[0], us[1] + us[3], fs[2], (fs[1] + fs[3]) - (us[1] + us[3])))
    
    return betterSpaces