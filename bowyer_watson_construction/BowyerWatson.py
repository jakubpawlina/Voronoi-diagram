import random
import time
from math import sqrt


# Define Euclidean metric on R^2
def d(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return (x2-x1)**2 + (y2-y1)**2


# Calculate radius of a circumcircle of a triangle ABC
def radius(A, B, C):
    a, b, c = sqrt(d(A, B)), sqrt(d(B, C)), sqrt(d(C, A))
    s = (a+b+c)/2
    return a * b * c/(4 * sqrt(s * (s-a) * (s-b) * (s-c)))


# Calculate centre of a circumcircle of a triangle ABC
def centre(A, B, C):
    Ax, Ay = A
    Bx, By = B
    Cx, Cy = C
    D = 2*(Ax*(By-Cy)+Bx*(Cy-Ay)+Cx*(Ay-By))
    ox = 1/D * ((Ax**2+Ay**2)*(By-Cy)+(Bx**2+By**2)
                * (Cy-Ay)+(Cx**2+Cy**2)*(Ay-By))
    oy = 1/D * ((Ax**2+Ay**2)*(Cx-Bx)+(Bx**2+By**2)
                * (Ax-Cx)+(Cx**2+Cy**2)*(Bx-Ax))
    return (ox, oy)


def BowyerWatson(points):  # O(n^2)
    n = len(points)
    err = 10**-8  # tolerance for 0 i.e. abs(x-y)<err => x =~ y

    # Construct a super-rectangle which completely covers the set of points and
    # initial triangulation consisting of two super-triangles
    x_max, y_max = max(points, key=lambda x: x[0])[
        0], max(points, key=lambda x: x[1])[1]
    x_min, y_min = min(points, key=lambda x: x[0])[
        0], min(points, key=lambda x: x[1])[1]
    a = max(abs(y_max-y_min), abs(x_max-x_min))
    x_max += a
    y_max += a
    x_min -= a
    y_min -= a
    points = points[:] + [(x_min, y_min), (x_min, y_max),
                          (x_max, y_max), (x_max, y_min)]

    superT1, superT2 = (n, n+1, n+2), (n, n+2, n+3)
    triangles = {superT1, superT2}
    edges = {(n, n+1): {superT1}, (n+1, n+2): {superT1}, (n+2, n+3): {superT2},
             (n+3, n): {superT2}, (n+2, n): {superT1, superT2}}

    for p in range(n):
        # Find all triangles such that their circumcircle contains point p. We
        # will call them 'bad' triangles
        badTriangles = set()
        for T in triangles:
            A, B, C = points[T[0]], points[T[1]], points[T[2]]
            d2, r2 = d(points[p], centre(A, B, C)), radius(A, B, C)**2
            if d2 < r2 or abs(d2 - r2) < err:
                badTriangles.add(T)

        # Find the boundary of the polygonal 'hole' which would be created after
        # removing all bad triangles
        polygon = set()
        for T in badTriangles:
            a, b, c = (T[0], T[1]), (T[1], T[2]), (T[2], T[0])
            for e in (a, b, c):
                Ts = edges[e] if edges.get(e) != None else edges[e[::-1]]
                if len((Ts & badTriangles) - {T}) == 0:
                    polygon.add(e)

        # Remove bad triangles
        for T in badTriangles:
            a, b, c = (T[0], T[1]), (T[1], T[2]), (T[2], T[0])
            triangles.remove(T)
            for e in (a, b, c):
                e = e if edges.get(e) != None else e[::-1]
                edges[e].remove(T)
                if len(edges[e]) == 0:
                    del edges[e]

        # Triangulate the interior of the polygonal hole
        for e in polygon:
            T = (p, e[0], e[1])
            triangles.add(T)
            a, b, c = (T[0], T[1]), (T[1], T[2]), (T[2], T[0])
            for e in (a, b, c):
                if edges.get(e) != None:
                    edges[e].add(T)
                elif edges.get(e[::-1]) != None:
                    edges[e[::-1]].add(T)
                else:
                    edges[e] = {T}

    # Remove triangles which contain a vertex from the initial super-triangle
    toRemove = set()
    for T in triangles:
        for p in (T[0], T[1], T[2]):
            if p in (n, n+1, n+2, n+3):
                toRemove.add(T)
    for T in toRemove:
        triangles.remove(T)

    # Compute Voronoi diagram dual to the computed Delaunay triangulation, O(n)
    voronoi = []
    for e in edges:
        Ts = edges[e] & triangles
        if len(Ts) == 2:
            T1, T2 = Ts.pop(), Ts.pop()
        elif len(Ts) == 1:
            T1, T2 = edges[e].pop(), edges[e].pop()
        else:
            T1, T2 = None, None
        if T1 != None and T2 != None:
            A1, B1, C1 = points[T1[0]], points[T1[1]], points[T1[2]]
            A2, B2, C2 = points[T2[0]], points[T2[1]], points[T2[2]]
            voronoi.append([centre(A1, B1, C1), centre(A2, B2, C2)])

    return triangles, voronoi


# Benchmarks
def runtests():
    # Generate N random points limited to a region [a;b]x[a;b]. Function returns
    # list of tuples (x,y) representing cartesian coordinates of points.
    def genRndPoints(N, a, b):
        points = []
        for i in range(N):
            x, y = random.uniform(a, b), random.uniform(a, b)
            points.append((x, y))
        return points

    N = int(input())
    points = genRndPoints(N, -10, 10)
    s = time.time()
    T, V = BowyerWatson(points)
    e = time.time()
    print(e-s)
    return None


runtests()
