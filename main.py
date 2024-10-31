from pygeodesy.sphericalNvector import LatLon, meanOf
from dataclasses import dataclass
from typing import List
import math

@dataclass
class Position:
    lat: float
    lon: float
    alt: float

def calculate_direction(ground: Position, balloon: Position):
    """ Calculate and return direction and elevation from groundstation to balloon. """
    ground_location = LatLon(ground.lat, ground.lon, height=ground.alt)
    balloon_location = LatLon(balloon.lat, balloon.lon, height=balloon.alt)

    groundstation_to_balloon = ground_location.initialBearingTo(balloon_location)
    distance_to_balloon = ground_location.distanceTo(balloon_location)
    elevation_angle = math.degrees(math.atan2(balloon.alt - ground.alt, distance_to_balloon))

    return groundstation_to_balloon, elevation_angle

def calculate_swivel(current_direction: float, target_direction: float):
    """ Calculate swivel required to point towards balloon. """
    difference = (target_direction - current_direction + 180) % 360 - 180
    return difference

def main(ground: Position, curr_direction: float, balloon_gps: List[Position]):
    """ Calculate and return the distance, elevation angle, and swivel direction using the average of multiple gps estimates for the balloon. """
    possible_balloon_locations = [LatLon(coord.lat, coord.lon,height=coord.alt) for coord in balloon_gps]
    average_location = meanOf(possible_balloon_locations)

    average_direction, elevation_angle = calculate_direction(
        ground,
        Position(average_location.lat, average_location.lon, average_location.height)
    )
    
    swivel_direction = calculate_swivel(curr_direction, average_direction)

    return average_direction, elevation_angle, swivel_direction

ground_station = Position(lat=37.7749, lon=-122.4194, alt=30)
current_direction = 45

balloon_gps_estimates = [
    Position(lat=37.7849, lon=-122.4294, alt=1000),
    Position(lat=37.7949, lon=-122.4394, alt=1500),
    Position(lat=37.8049, lon=-122.4494, alt=2000)
]

average_direction, elevation_angle, swivel_direction = main(
    ground_station, current_direction, balloon_gps_estimates
)

print(f"Average Direction: {average_direction:.2f} degrees")
print(f"Elevation Angle: {elevation_angle:.2f} degrees")
print(f"Swivel Direction: {swivel_direction:.2f} degrees")
