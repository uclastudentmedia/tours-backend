# UCLA Maps backend

UCLA Maps is the mobile app built by UCLA Student Media that helps students navigate their way around campus and discover what's around them; the app is available in the [App Store](https://itunes.apple.com/us/app/ucla-maps/id1284271661) and in [Google Play](https://play.google.com/store/apps/details?id=com.uclastudentmedia.UCLAMaps). 

This backend powers the API that our [apps' frontend](https://github.com/uclastudentmedia/tours-frontend) uses, and the crown jewel of our APIs is **indoor navigation**: the ability to navigate from one room to another in the same building. Given user input of a specific building, a start room, and end room, the API can generate an image (or two, if the rooms are on different floors) of the floor plan(s) with the path from the start to the end room. To see this in action, check out the apps or visit https://tours.bruinmobile.com/.

<img src="https://tours.bruinmobile.com/media/floor_plans/cache/67_5_1079-918_308-803.png" width="510" height="540" alt="Example routing image"/>

### Why build indoor navigation?

We built the indoor navigation API specifically for Boelter Hall and the Math Sciences building, to help alleviate the pain of finding room locations within these two buildings. Even experienced UCLA students have trouble finding their classroom in the winding 9-floor maze of Boelter/MS: which section of the building is my room in? Which entrance do I take? Where are Boelter and MS connected?

### Designing the user experience

Our ideal user experience would have been: given the user's GPS coordinates, whether they're inside or outside the building, provide real-time turn-by-turn navigation details for them to walk towards a destination room. This would have meant knowing the GPS coordinates for all the rooms in a building, and even if that were obtainable, there would've been a bigger problem: there's no cell signal when you're trapped under several floors of concrete, and the WiFi signal is also weak in the depths of Boelter, the Birthplace of the Internet<sup>TM</sup>, so there's no way you're getting accurate GPS location. Then there would also be the issue of determining which floor the user's on, and it turns out phones can determine altitude, but that'd be opening up another can of worms...

So we ended up making something simpler: if the user is currently inside a classroom or nearby one, they could enter that as the start room and enter the destination room that they want, and get an image or two showing the path to take to get to the destination room (this does assume that the user knows how to follow the path shown).

## Implementing the whole thing

Unlike outdoor navigation, which includes services like Google Maps and OpenStreetMap, there's not as much existing libraries and other support for indoor navigation, so we did our best to leverage existing libraries, glue them together, and write our own code when we needed to.

First, we needed to obtain floor plans for Boelter/MS and put that data into some format that would allow us to query it in order to do routing from one room to another: this ended up being a Postgres database with [PostGIS](https://postgis.net/), which lets us represent the rooms and pathways as geogrpahic objects that we can do location queries on. Basically, the rooms/pathways become a huge graph that you can run your favourite shortest-distance algorithm on.

Then, when the user makes an API request for a specific building and start and end room, the server generates the graph of the entire building (luckily, we didn't have that much data), calculates the navigation route, and then uses that route data to generate the image(s) of the floor(s) to show the route.

Let's dive into the development process.

### Getting the data

As you might imagine, there's no public source of all floor plans for the buildings we wanted. Luckily, UPE was generous enough to provide us with a few floor plans with room labels (thanks UPE!), but for the rest of the floors, we walked around the floors looking for a labelled floor plan or just finding a floor layout and manually going around to label all the room numbers.

Since we didn't have a consistent source of floor plan images, there was no good way of automating the process of putting the floor plan data into the database. We thought it might be possible to use computer vision to detect the rooms in the images, but decided it would be too difficult and take too long. So, we ended up loading the images into [QGIS](https://qgis.org/en/site/) and manually tracing all the room locations, from which we could generate a clean looking floor plan image, like the one below from Boelter 4. 

<img src="media/floor_plans/base/67_4.png" width="450" height="540" alt="Boelter 4 floor plan"/>

We also added the walkable areas as paths, a collection of nodes and edges that make up the graph to navigate on. The rooms are added to this graph as one of the nodes in this graph. The graph is shown superimposed on the rooms below:

