def resolveCollisions1(self, collidingSiblings: list) -> None:
    """
    This function will resolve collisions of a component with its siblings.

    :param collidingSiblings: siblings colliding with this component
    :type collidingSiblings: list
    :return: None
    :rtype: NoneType
    """
    
    work = [(self, collidingSiblings)]
    while work:
        cur, siblings = work.pop()
        
        for sib in siblings:
            print("{} ({},{}) vs. {} ({},{}):".format(cur.getLabel(), cur.x(), cur.y(),
                                                      sib.getLabel(), sib.x(), sib.y()))
            sb = sib.boundingRect(False)
            cb = cur.boundingRect(False)
            dx = cur.getX() - sib.getX()
            dy = cur.getY() - sib.getY()
            
            # same corner
            if dx == 0 and dy == 0:
                print("\tCorner is same")
                angle = 0
                siblingWins = (sb.width() * sb.height() > cb.width() * cb.height())
            
            # corner is shifted vertically
            elif dx == 0:
                print("\tCorner is shifted vertically")
                angle = 90
                siblingWins = (sib.getY() < cur.getY())
            
            # corner is shifted horizontally
            elif dy == 0:
                print("\tCorner is shifted horizontally")
                angle = 0
                siblingWins = (sib.getX() < cur.getX())
            
            # slope is negative
            elif dy / dx < 0:
                print("\tThe slope is negative")
                print("\t", dy, dx)
                if abs(dx) >= abs(dy):
                    print("\tDecided to shift horizontally")
                    angle = 0
                    siblingWins = (sib.getX() < cur.getX())
                else:
                    angle = 90
                    print("\tDecided to shift vertically")
                    siblingWins = (sib.getY() < cur.getY())
            
            # slope is positive
            else:
                angle = 45  # The exact number doesn't matter as long as it's not 0 or 90.
                siblingWins = (sib.getX() < cur.getX()) and (sib.getY() < cur.getY())
            
            print("\tAngle:", angle)
            if siblingWins:
                winner = sib
                loser = cur
            else:
                winner = cur
                loser = sib
            
            lop = loser.pos()  # loser old pos
            if angle == 0:
                print("\tShifting {} Right".format(loser.getLabel()))
                loser.setX(winner.x() + winner.boundingRect(True).width() +
                           max(winner.getMargin(), loser.getMargin()))
            
            elif angle == 90:
                print("\tShifting {} Down".format(loser.getLabel()))
                loser.setY(winner.y() + winner.boundingRect(True).height() +
                           max(winner.getMargin(), loser.getMargin()))
            
            else:
                print("\tShifting {} Diagonally".format(loser.getLabel()))
                slope = dy / dx
                n = slope * winner.boundingRect().height()  # Number of iterations of slope to reach bottom
                m = winner.boundingRect().width() / slope  # Number of iterations of slope to
                # reach right
                
                if n < m:  # bottom is closer
                    loser.setX(winner.x() + n)
                    loser.setY(winner.y() + winner.boundingRect(True).height() +
                               max(winner.getMargin(), loser.getMargin()))
                else:
                    loser.setX(winner.x() + winner.boundingRect(True).width() +
                               max(winner.getMargin(), loser.getMargin()))
                    loser.setY(winner.y() + m)
            lnp = loser.pos()  # loser new pos
            
            print("\t{}: ({},{}) -> ({},{})".format(loser.getLabel(), lop.x(), lop.y(),
                                                    lnp.x(), lnp.y()))
            
            assert (not winner.overlapsWith(loser))
            
            try:
                sibsibs = [self.scene().getGraphics(sibling) for sibling in
                           sib._dataComponent.getSiblings() if
                           sibling is not sib._dataComponent]
            except:
                sibsibs = []
            
            sibsibCollisions = sib.getCollidingComponents(sibsibs)
            
            if sibsibCollisions:
                work.insert(0, (sib, sibsibCollisions))