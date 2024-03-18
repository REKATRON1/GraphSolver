import random

def generate_random_point(max_coords: tuple, min_coords: tuple=None) -> tuple:
    if min_coords == None:
        return tuple([random.random()*m for m in max_coords])
    return tuple([random.random()*(ma-mi)+mi for mi, ma in zip(min_coords, max_coords)])

def generate_random_points(amount: int, max_coords: tuple, min_coords: tuple=None) -> list[tuple]:
    return [generate_random_point(max_coords, min_coords=min_coords) for _ in range(amount)]