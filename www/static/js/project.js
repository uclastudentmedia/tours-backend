function toTitleCase(str)
{
    return str.replace(/\w\S*/g,
            function(txt){
                return txt.charAt(0).toUpperCase() +
                txt.substr(1).toLowerCase();
            });
}

$(function() {
    console.log(building_list_arr);
    if (!(building_list_arr instanceof Array) ||
        building_list_arr.length === 0) {
        console.log("no building data!");
        return;
    }
    // populate list of buildings
    for (let idx = 0; idx < building_list_arr.length; idx++) {
        let building_name = toTitleCase(building_list_arr[idx].name);
        jQuery('<option></option>', {
            text: building_name
        }).appendTo('#building-select');
    }
});

$('#building-select').on('change', function() {
    $('#start-room').empty();
    $('#end-room').empty();
    let building_name = $(this).val().toLowerCase();
    if (!building_name) {
        console.log('no building name');
        return;
    }
    // TODO: consider changing the array to a map instead
    let building_object = building_list_arr.filter(building => building.name.toLowerCase() == building_name);
    if (!building_object.length) {
        console.log('did not find building', building_object);
        return;
    }
    building_object = building_object[0];
    console.log(building_object);
    for (let poi of building_object.pois) {
        let option = jQuery('<option></option>', {
            text: poi
        });
        let option2 = option;
        option.appendTo('#start-room');
        option.clone().appendTo('#end-room');
    }
});
