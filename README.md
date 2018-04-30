# UCLA Maps backend

UCLA Maps is the mobile app built by UCLA Student Media that helps students navigate their way around campus and discover what's around them; the app is available in the [App Store](https://itunes.apple.com/us/app/ucla-maps/id1284271661) and in [Google Play](https://play.google.com/store/apps/details?id=com.uclastudentmedia.UCLAMaps). 

This backend powers the API that our [apps' frontend](https://github.com/uclastudentmedia/tours-frontend) uses, and the crown jewel of our APIs is **indoor navigation**: the ability to navigate from one room to another in the same building. Given user input of a specific building, a start room, and end room, the API can generate an image (or two, if the rooms are on different floors) of the floor plan(s) with the path from the start to the end room. To see this in action, check out the apps or visit https://tours.bruinmobile.com/.



### Why build indoor navigation?

We built the indoor navigation API specifically for Boelter Hall and the Math Sciences building, to help alleviate the pain of finding room locations within these two buildings. Even experienced UCLA students have trouble finding their classroom in the winding 9-floor maze of Boelter/MS: which section of the building is my room in? Which entrance do I take? Where are Boelter and MS connected?

### How we designed it

