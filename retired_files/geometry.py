class Point:
    """
    The class used to define a corner in the extra components placement algorithm.
    """
    
    def __init__(self, x: float, y: float) -> None:
        """
        Initializes the point class with coordinates.

        :param x: x value of point
        :type x: float
        :param y: y value of point
        :type y: float
        """
        
        self.x = round(Decimal(str(x)), 2)
        self.y = round(Decimal(str(y)), 2)
    
    def toHashkey(self) -> str:
        """
        Returns point as a hashkey. Returns it as a string.

        :return: hashkey
        :rtype: str
        """
        
        return str(self.x) + "_" + str(self.y)
    
    def clone(self) -> 'Point':
        """
        returns identical copy of self

        :return: clone of self
        :rtype: Point
        """
        
        return Point(float(self.x), float(self.y))


class Segment:
    """
    Defines a segment between two points
    """
    
    def __init__(self, a: 'Point', b: 'Point'):
        """
        Initializes a segment
        """
        
        self.ptA = a
        self.ptB = b


class Contour:
    """
    The class that makes a contour out of points, for the extra components placement algorithm
    """
    
    def __init__(self, points: list):
        """
        Initializes a contour based off initial array

        :param points: list of Points
        :type points: list
        """
        
        self.pts = points[:]
    
    def addPoint(self, point: 'Point'):
        """
        Adds a point to self.pts
        :param point: Point to add
        :type point: Point
        :return: None
        """
        
        self.pts.append(point)
    
    def clone(self) -> 'Contour':
        """
        Returns exact copy of self

        :return: Clone of self
        :rtype: Contour
        """
        
        return Contour(self.pts)


class Polygon:
    """
    The free space in the Extra Components placement algorithm is defined by several of these polygons.
    One Polygon class can actually store several
    """
    
    def __init__(self, poly: 'Polygon' = None, points: list = None):
        """
        Initializes a polygon based on what is supplied

        :param poly: another polygon object off which to base this one
        :type poly: Polygon
        :param points: list of points for first contour of this polygon
        :type points: list
        """
        
        self.contours = []
        if poly:
            self.contours = poly.contours[:]
        elif points:
            self.contours.append(Contour(points))
    
    def merge(self, other: 'Polygon'):
        """
        This function merges another polygon into this one.

        :param other: Polygon to merge with self
        :type other: Polygon
        :return: None
        """
        
        # Based on code from
        # https://stackoverflow.com/questions/643995/algorithm-to-merge-adjacent-rectangles-into-polygon
        
        segments = {}
        for contour in self.contours:
            pts = contour.pts
            for ptA in pts:
                if contour.pts.index(ptA) == len(contour.pts) - 1:
                    ptB = contour.pts[0]
                else:
                    ptB = contour.pts[contour.pts.index(ptA) + 1]
                
                idA = ptA.toHashkey()
                idB = ptB.toHashkey()
                if not segments[idA]:
                    segments[idA] = {'n': 0, 'pts': {}}
                segments[idA]['pts'][idB] = Segment(ptA.clone(), ptB.clone())
                segments[idA]['n'] = segments[idA]['n'] + 1
        
        # Enumerate segments in other's contours and eliminate duplicates
        for contour in other.contours:
            pts = contour.pts
            for ptA in pts:
                if contour.pts.index(ptA) == len(contour.pts) - 1:
                    ptB = contour.pts[0]
                else:
                    ptB = contour.pts[contour.pts.index(ptA) + 1]
                
                idA = ptA.toHashkey()
                idB = ptB.toHashkey()
                if segments[idB]['pts'][idA]:
                    del segments[idB]['pts'][idA]
                    if not (segments[idB]['n'] - 1):
                        del segments[idB]
                else:
                    if not segments[idA]:
                        segments[idA] = {'n': 0, 'pts': {}}
                    segments[idA]['pts'][idB] = Segment(ptA.clone(), ptB.clone())
                    segments[idA]['n'] = segments[idA]['n'] + 1
        
        # Recreate and store new contours by jumping from one point to the next,
        # using the second point of the segment as hash key for next segment
        self.contours = []
        for idA in segments:
            contour = Contour([])
            self.contours.append(contour)
            for idB in segments[idA]['pts']:  # gets a random element, doesn't matter which one
                break
            segment = segments[idA]['pts'][idB]
            while segment:
                contour.addPoint(segment.ptA.clone())
                
                del segments[idA]['pts'][idB]
                if not (segments[idA]['n'] - 1):
                    del segments[idA]
                
                idA = segment.ptB.toHashkey()
                if segments[idA]:
                    for idB in segments[idA]['pts']:
                        break
                    segment = segments[idA]['pts'][idB]
                else:
                    segment = None

