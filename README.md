# UCLA Maps backend

UCLA Maps is the mobile app built by UCLA Student Media that helps students navigate their way around campus and discover what's around them; the app is available in the [App Store](https://itunes.apple.com/us/app/ucla-maps/id1284271661) and in [Google Play](https://play.google.com/store/apps/details?id=com.uclastudentmedia.UCLAMaps). 

This backend powers the API that our [apps' frontend](https://github.com/uclastudentmedia/tours-frontend) uses, and the crown jewel of our APIs is **indoor navigation**: the ability to navigate from one room to another in the same building. Given user input of a specific building, a start room, and end room, the API can generate an image (or two, if the rooms are on different floors) of the floor plan(s) with the path from the start to the end room. To see this in action, check out the apps or visit https://tours.bruinmobile.com/.

<img src="https://tours.bruinmobile.com/media/floor_plans/cache/67_5_1079-918_308-803.png" width="510" height="540"/>

### Why build indoor navigation?

We built the indoor navigation API specifically for Boelter Hall and the Math Sciences building, to help alleviate the pain of finding room locations within these two buildings. Even experienced UCLA students have trouble finding their classroom in the winding 9-floor maze of Boelter/MS: which section of the building is my room in? Which entrance do I take? Where are Boelter and MS connected?

### How we designed it

Our ideal user experience would have been: given the user's GPS coordinates, whether they're inside or outside the building, provide real-time turn-by-turn navigation details for them to walk towards a destination room. This would have meant knowing the GPS coordinates for all the rooms in a building, and even if that were obtainable, there would've been a bigger problem: there's no cell signal when you're trapped under several floors of concrete, and the WiFi signal is also weak in the depths of Boelter, the Birthplace of the Internet<sup>TM</sup>, so there's no way you're getting accurate GPS location.

