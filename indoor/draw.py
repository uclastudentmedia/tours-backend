from django.conf import settings
from django.http import Http404
from PIL import Image, ImageDraw, ImageFont
import os

from .models import RoomPolygon, Floor, Building, POI


def clear_cache():
    # TODO: only delete x oldest files
    directory = os.path.join(settings.MEDIA_ROOT, "floor_plans/cache/")
    for filename in os.listdir(directory):
        if filename.endswith(".png"):
            path = os.path.join(directory, filename)
            os.unlink(path)


def get_floor_plan_path(landmark_id, floor_name):
    directory = "floor_plans/base/"
    filename = str(landmark_id) + "_" + floor_name + ".png"
    return os.path.join(settings.MEDIA_ROOT, directory, filename)


def _get_route_image_relpath(landmark_id, floor_name, start_coords, end_coords):
    directory = "floor_plans/cache/"

    start_x, start_y = start_coords
    end_x, end_y = end_coords

    filename = "{id}_{floor}_{sx}-{sy}_{ex}-{ey}.png".format(
        id=landmark_id, floor=floor_name,
        sx=start_x, sy=(-start_y), ex=end_x, ey=(-end_y))

    return os.path.join(directory, filename)


def get_route_image_path(landmark_id, floor_name, start_coords, end_coords):
    relpath = _get_route_image_relpath(landmark_id, floor_name,
                                       start_coords, end_coords)
    return os.path.join(settings.MEDIA_ROOT, relpath)


def get_route_image_url(landmark_id, floor_name, start_coords, end_coords):
    relpath = _get_route_image_relpath(landmark_id, floor_name,
                                       start_coords, end_coords)
    return os.path.join(settings.MEDIA_URL, relpath)


def draw_route_image(landmark_id, floor_name, path, start_name, end_name):
    # TODO: probably clean up etc.

    # check if image is cached
    cache_image_path = get_route_image_path(landmark_id, floor_name,
                                            path[0], path[-1])
    if os.path.isfile(cache_image_path):
        # touch the cached file
        os.utime(cache_image_path, None)
        return

    # image is not cached, draw it

    building = Building.objects.get(landmark__id=landmark_id)
    floor = Floor.objects.get(name=floor_name, building=building)
    start = POI.objects.get(name=start_name, floor__building=building)
    end = POI.objects.get(name=end_name, floor__building=building)

    base_image_path = get_floor_plan_path(landmark_id, floor.name)
    try:
        image = Image.open(base_image_path)
    except IOError as e:
        raise Http404(e)
    draw = ImageDraw.Draw(image)

    # fill in rooms
    if start.floor == floor and start.type == "room":
        start_room_data = RoomPolygon.objects.get(name=start_name, floor=floor)
        start_border = start_room_data.geom.coords
        # room only has one polygon since we're using PolygonField
        start_border = [(n[0], -n[1]) for n in start_border[0]]
        draw.polygon(start_border, fill=(255, 114, 114, 255))
    if end.floor == floor and end.type == "room":
        end_room_data = RoomPolygon.objects.get(name=end_name, floor=floor)
        end_border = end_room_data.geom.coords
        # room only has one polygon since we're using PolygonField
        end_border = [(n[0], -n[1]) for n in end_border[0]]
        draw.polygon(end_border, fill=(255, 114, 114, 255))

    # draw lines
    line_fill = (0, 113, 188, 255)
    path = [(n[0], -n[1]) for n in path]
    for i in range(0, len(path)-1):
        draw.line((path[i], path[i+1]), fill=line_fill, width=10)

    # draw circles at intersections
    rad = 5
    for (x,y) in path:
        draw.ellipse([x - rad, y - rad, x + rad, y + rad], fill=line_fill)

    # draw text centered in room
    font = ImageFont.truetype(os.path.join(settings.MEDIA_ROOT,
        "fonts/Roboto-Bold.ttf"), 20)
    if start.floor == floor and start.type == "room":
        start_centroid = start_room_data.geom.centroid
        text_width, text_height = draw.textsize(start_name, font=font)
        start_coords = (start_centroid.x - text_width / 2,
                -start_centroid.y - text_height / 2)
        draw.text(start_coords, start_name, font=font, fill=(0, 188, 169, 255))
    if end.floor == floor and end.type == "room":
        end_centroid = end_room_data.geom.centroid
        text_width, text_height = draw.textsize(end_name, font=font)
        end_coords = (end_centroid.x - text_width / 2,
                -end_centroid.y - text_height / 2)
        draw.text(end_coords, end_name, font=font, fill=(0, 188, 169, 255))

    # save modified image
    image.save(cache_image_path, "PNG")
