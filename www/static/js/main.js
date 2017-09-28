$(function() {
    console.log(building_list_dict);
    if (!(building_list_dict instanceof Object) ||
        Object.keys(building_list_dict).length === 0) {
        console.log("no building data!");
        showError("No building data!");
        return;
    }
    /*
    // populate list of buildings
    for (let building_name in building_list_dict) {
        let building = building_list_dict[building_name];
        if (typeof building.pois === "undefined") {
            console.log("no pois for " + building_name);
            continue;
        }
        jQuery('<option></option>', {
            text: building_name
        }).appendTo('#building-select');

        jQuery('<li></li>',{
            text: building_name + ': ' + building.floors.join(', ')
        }).appendTo('#building-list');
    }
    */
    $('#start-form').on('input', validateRoomInput);
    //$('#start-form').on('change', validateRoomInput);
    //$('#start-form').on('focusout', validateRoomInput);
    $('#end-form').on('input', validateRoomInput);
    //$('#end-form').on('change', validateRoomInput);
    //$('#end-form').on('focusout', validateRoomInput);
    $('#start-room').val('');
    $('#end-room').val('');
    $('#start-room').autocomplete({
        source: [],
        select: function(event, ui) {
            $('#start-form').removeClass('has-error');
            $('#start-form').addClass('has-success');
            if ($('input[name=navigation-type]:checked').val() === 'find-a-room') {
                $('#end-room').val(ui.item.value);
            }
        }
    });
    $('#start-room').on('input', function() {
        if ($('input[name=navigation-type]:checked').val() === 'find-a-room') {
            $('#end-room').val($('#start-room').val());
        }
    });
    $('#end-room').autocomplete({
        source: [],
        select: function() {
            $('#end-form').removeClass('has-error');
            $('#end-form').addClass('has-success');
        }
    });
    $('#main-form').on('submit', processInputsAndGetImages);
    // the building select should now have the first building, so we can populate the rooms right away
    populateRoomInputs();
    $('#building-select').on('change', populateRoomInputs);
    hideError();

    $('input[name=navigation-type]').change(function() {
        let endFormDisplayStyle = 'inline-block';
        if (this.value === "find-a-room") {
            endFormDisplayStyle = 'none';
            $('#end-room').val($('#start-room').val());
        }
        $('#end-form').css('display', endFormDisplayStyle);
    });

    // need this because Firefox saves the last checked value
    $('#room-to-room').prop('checked', true);
});

function populateRoomInputs() {
    $('#start-room').val('');
    $('#end-room').val('');
    $('#start-form').removeClass('has-error has-success');
    $('#end-form').removeClass('has-error has-success');
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

function validateRoomInput() {
    let room = $(this).children('input').val();
    $(this).removeClass('has-error has-success');
    if (room.length === 0) {
        return;
    }
    if (!isRoomStringValid(room)) {
        $(this).addClass('has-error');
    }
    $(this).addClass('has-success');
    $('#loading-msg').addClass('hidden');
}

function isBuildingStringValid(buildingStr) {
    return building_list_dict.hasOwnProperty(buildingStr);
}

function isRoomStringValid(roomStr) {
    let building_name = $('#building-select').val();
    if (!isBuildingStringValid(building_name)) {
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
    if (!isBuildingStringValid(building_name)) {
        showError('Invalid building name');
        return;
    }
    if (start_room.length === 0) {
        showError('No start room selected');
        return;
    }
    if (!isRoomStringValid(start_room)) {
        showError('Invalid start room');
        return;
    }
    if (end_room.length === 0) {
        showError('No end room selected');
        return;
    }
    if (!isRoomStringValid(end_room)) {
        showError('Invalid end room');
        return;
    }
    let route_api = '/indoor/route/' +
        building_list_dict[building_name].landmark_id + '/' +
        start_room + '/' + end_room;
    console.log(route_api);
    $('#loading-msg').removeClass('hidden alert-success').addClass('alert-info').text('Loading...');
    $.ajax(route_api)
        .done(function(data) {
            console.log(data);
            hideError();
            $('#image-container').empty();
            let image_arr = data.images;
            if (!(image_arr instanceof Array) ||
                image_arr.length === 0) {
                console.log("No images received from API");
                $('#loading-msg').addClass('hidden');
                showError("No images");
                return;
            }
            for (let image of image_arr) {
                let container = $('<div></div>').appendTo('#image-container');
                jQuery('<h3></h3>', {
                    text: data.building + ', Floor ' + image.floor
                }).appendTo(container);
                let a_tag = jQuery('<a></a>', {
                    href: image.url,
                    target: '_blank'
                }).appendTo(container);
                jQuery('<img/>',{
                    src: image.url
                }).appendTo(a_tag);
            }
            $('#loading-msg').removeClass('alert-info').addClass('alert-success').text('Done.');
        })
        .fail(function(err) {
            console.log("API error", err);
            $('#loading-msg').addClass('hidden');
            showError(err.statusText);
        });
}

function showError(error_msg) {
    $('#error-msg').removeClass('hidden').text(error_msg);
}

function hideError() {
    $('#error-msg').addClass('hidden').text('');
}
