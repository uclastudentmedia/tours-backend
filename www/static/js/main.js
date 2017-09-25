$(function() {
    console.log(building_list_dict);
    if (!(building_list_dict instanceof Object) ||
        Object.keys(building_list_dict).length === 0) {
        console.log("no building data!");
        return;
    }
    // populate list of buildings
    for (let building_name in building_list_dict) {
        if (typeof building_list_dict[building_name].pois === "undefined") {
            console.log("no pois for " + building_name);
            continue;
        }
        jQuery('<option></option>', {
            text: building_name
        }).appendTo('#building-select');
    }
    $('#start-room').val('');
    $('#end-room').val('');
    $('#start-room').autocomplete({
        source: []
    });
    $('#end-room').autocomplete({
        source: []
    });
    $('#main-form').on('submit', processInputsAndGetImages);
    // the building select should now have the first building, so we can populate the rooms right away
    populateRoomInputs();
    $('#building-select').on('change', populateRoomInputs);
});

function populateRoomInputs() {
    $('#start-room').val('');
    $('#end-room').val('');
    let building_name = $('#building-select').val();
    if (building_name.length === 0) {
        console.log('no building name');
        return;
    }
    let building_object = building_list_dict[building_name];
    console.log(building_object);
    $('#start-room').autocomplete("option", "source", building_object.pois);
    $('#end-room').autocomplete("option", "source", building_object.pois);
}


function isRoomStringValid(roomStr) {
    let building_name = $('#building-select').val();
    if (building_name.length === 0) {
        return false;
    }
    let building_object = building_list_dict[building_name];
    if (building_object.pois.indexOf(roomStr) === -1) {
        console.log("not valid room");
        return false;
    }
    return true;
}

function processInputsAndGetImages(event) {
    event.preventDefault();
    let building_name = $('#building-select').val();
    let start_room = $('#start-room').val();
    let end_room = $('#end-room').val();
    if (building_name.length === 0) {
        return;
    }
    if (start_room.length === 0) {
        return;
    }
    if (!isRoomStringValid(start_room)) {
        return;
    }
    if (end_room.length === 0) {
        return;
    }
    if (!isRoomStringValid(end_room)) {
        return;
    }
    if (start_room === end_room) {
        return;
    }
    let route_api = '/indoor/route/' +
        building_list_dict[building_name].landmark_id + '/' +
        start_room + '/' + end_room;
    console.log(route_api);
    $.ajax(route_api)
        .done(function(data) {
            console.log(data);
            $('#image-container').empty();
            let image_arr = data.images;
            if (!(image_arr instanceof Array) ||
                image_arr.length === 0) {
                console.log("No images received from API");
                return;
            }
            for (let image_url of image_arr) {
                jQuery('<img/>',{
                    src: image_url
                }).appendTo('#image-container');
            }
        })
        .fail(function(err) {
            console.log("API error", err);
        });
}

