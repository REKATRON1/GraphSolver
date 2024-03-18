from typing import TypeAlias

Vector2: TypeAlias = tuple[float, float]
iVector2: TypeAlias = tuple[int, int]
Vector3: TypeAlias = tuple[float, float, float]
iVector3: TypeAlias = tuple[int, int, int]

Point: TypeAlias = Vector2 | Vector3
Edge: TypeAlias = tuple[Point, Point]
