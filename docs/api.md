# API usage

## Contents
- [Landmarks](#landmarks)
- [Categories](#categories)
- [Tours](#tours)
- [Outdoor Navigation](#outdoor-navigation)
- [Indoor Navigation](#indoor-navigation)

## Landmarks

### Landmark List
Get all information about all of the landmarks
```
GET /api/landmark/
```
Response:
```js
{
    "results": [
        {
            "name": "1310 Law Building",
            "lat": 34.07265053,
            "long": -118.4388012,
            "priority": 612,
            "category_id": null,
            "id": 1,
            // ...
        },
        // ...
    ]
}
```

### Landmark Detail
Get detailed info about one landmark
```
GET /api/landmark/<landmark-id>
```
Response:
```js
{  
   "results":{  
      "category":14,
      "name":"Taco Bell",
      "text_description":"Tacos",
      "lat":34.07024649,
      "long":-118.444103,
      "priority":306,
      "attributes":{  
         "hours":"Monday-Friday 8AM-11PM; Saturday-Sunday 8AM-10PM",
         "phone":"(310) 208-4808",
         "menu":{  
            "Quesarito Box":6.0,
            "Nachos Supreme":2.6
         }
      },
      "images": [
         {
            "original": "/media/photologue/photos/675_1.jpg",
            "thumbnail": "/media/photologue/photos/cache/675_1_thumbnail.jpg",
            "display": "/media/photologue/photos/cache/675_1_display.jpg"
         },
         // ...
      ],
      "image_count":2,
      "indoor_nav": false,
      "id":675
   }
}
```
- `attributes`: a object with arbitrary attributes
- `images`: URLs to various sizes of each image
    - `original`: The full image. Only use if you need high resolution.
    - `display`: A smaller image (400px wide)
    - `thumbnail`: An even smaller image (100px x 75px, cropped to fit)
- `indoor_nav`: if indoor navigation is supported for this landmark

### Landmark Images

> This is deprecated. Use the urls from [landmark detail](#landmark-detail)

Get an image of a landmark

```
GET /images/landmark/<landmark-id>/<img-index>
```
- `img-index`: goes from 1 through `image_count` (from [landmark detail](#landmark-detail))

Response: the image file


## Categories
Get the list of categories
```
GET /api/category/
```
Response:
```js
{  
   "results":[  
      {  
         "sort_order":2,
         "id":1,
         "name":"Parking"
      },
      // ...
    ]
}
```


## Tours
Get the list of premade tours
```
GET /api/tour/
```
Response:
```js
{  
   "results":[  
      {  
         "distance":5.0,
         "name":"South Campus",
         "landmark_ids":[  
            67,
            126,
            548
         ],
         "duration":3600,
         "id":1
      },
      // ...
    ]
}
```

  - `distance`: in miles
  - `duration`: in minutes


## Outdoor Navigation

#### [Server Setup](outdoor.md)

### Turn by Turn
Turn-by-turn directions between 2 points. See [Mapzen turn by turn docs](https://mapzen.com/documentation/mobility/turn-by-turn/api-reference).

### Optimized Route
Get the fastest route to tour a bunch of points. See [Mapzen optimized route docs](https://mapzen.com/documentation/mobility/optimized/api-reference).


## Indoor Navigation

### Building List
List of buildings that have indoor navigation.
```
GET /indoor/building/
```
Response:
```js
{
    "results": [
        {
            "floors": [ "b", "2" ],
            "landmark_id": 31,
            "name": "ackerman"
        },
        // ...
    ]
}
```

Each building in this list will have `"indoor_nav": true` in its
[landmark detail](#landmark-detail).

### Building Detail
List of routeable POIs in a building, organized by floor.
```
GET /indoor/building/<landmark-id>
```
Response:
```js
{
    "results": {
        "pois": {
            "2": [
                "2415",
                "2400E",
                "2400D"
            ],
            "b": [
                "B105"
            ]
        },
        "landmark_id": 31,
        "name": "ackerman"
    }
}
```

### Indoor Routing
Get images showing a route between 2 POIs.
```
GET /indoor/route/<landmark-id>/<start-name>/<end-name>
```

Route from a POI to an exit.
```
GET /indoor/route/<landmark-id>/<start-name>/exit
```

- `<start-name>` and `<end-name>` are names of POIs found in the
  [building detail](#building-detail) page.

Response:
```js
{
    "building": "ackerman",
    "start": "B105",
    "images": [
        "/media/floor_plans/cache/31_b_1247-732_1267-1113.png",
        "/media/floor_plans/cache/31_2_1125-1113_1395-965.png"
    ],
    "landmark_id": 31,
    "end": "2410"
}
```
- `images`: an array of urls to floorplans with the route drawn on them, in order

> TODO: If needed, we can support choosing whether to use stairs or elevators.
