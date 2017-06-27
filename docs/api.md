# API usage

## Contents
- [Landmarks](#landmarks)
- [Categories](#categories)
- [Tours](#tours)
- [Outdoor Navigation](#outdoor-navigation)

## Landmarks

### Landmark List
Basic info about all of the landmarks
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
			"id": 1
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
      "image_count":2,
      "id":675
   }
}
```
- `attributes`: a object with arbitrary attributes

### Landmark Images
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
         "category_id":1001,
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


## Outdoor Navigation

### Turn by Turn
Turn-by-turn directions between 2 points. See [Mapzen turn by turn docs](https://mapzen.com/documentation/mobility/turn-by-turn/api-reference).

### Optimized Route
Get the fastest route to tour a bunch of points. See [Mapzen optimized route docs](https://mapzen.com/documentation/mobility/optimized/api-reference).
