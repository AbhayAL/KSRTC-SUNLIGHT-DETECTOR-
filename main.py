from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from astral import LocationInfo
from astral.sun import sun
from datetime import datetime
import math

def get_location(prompt):
    geolocator = Nominatim(user_agent="sunlight_detector")
    location_name = input(f"{prompt}: ")
    location = geolocator.geocode(location_name)
    if location:
        print(f"Location detected: {location.address}")
        return location.latitude, location.longitude, location_name
    else:
        print("Location not found. Please try again.")
        return get_location(prompt)

def calculate_direction(start, end):
    """
    Calculate the bearing (direction) from start to end locations.
    """
    lat1, lon1 = math.radians(start[0]), math.radians(start[1])
    lat2, lon2 = math.radians(end[0]), math.radians(end[1])

    d_lon = lon2 - lon1
    x = math.sin(d_lon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(d_lon))
    initial_bearing = math.atan2(x, y)
    bearing = (math.degrees(initial_bearing) + 360) % 360
    return bearing

def get_sun_position(latitude, longitude, city_name):
    loc = LocationInfo(city_name, "Unknown", "UTC", latitude, longitude)
    current_time = datetime.now()
    s = sun(loc.observer, date=current_time, tzinfo=current_time.tzinfo)

    azimuth = s['azimuth']
    elevation = s['elevation']
    return azimuth, elevation

def decide_seat(sun_azimuth, route_bearing):
    """
    Determine the best side to sit based on sun azimuth and route direction.
    """
    relative_sun_position = (sun_azimuth - route_bearing + 360) % 360

    if 90 <= relative_sun_position <= 270:
        return "right"
    else:
        return "left"

def main():
    print("Enter your trip details:")
    start = get_location("Enter the starting location")
    end = get_location("Enter the destination location")

    route_bearing = calculate_direction((start[0], start[1]), (end[0], end[1]))
    sun_azimuth, _ = get_sun_position(start[0], start[1], start[2])

    print(f"\nRoute bearing: {route_bearing:.2f}°")
    print(f"Sun azimuth: {sun_azimuth:.2f}°")

    ideal_side = decide_seat(sun_azimuth, route_bearing)
    print(f"\nIdeal side to sit: {ideal_side.capitalize()} (to avoid sunlight).")

if __name__ == "__main__":
    main()
