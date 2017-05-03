updateHour = """
    console.log(state.data.day + ':' + state.data.hour);
    state.data.hour[0] = cb_obj.value;

    if (state.data.active.indexOf(1) > -1) {
        var path = 'image_' + cb_obj.value.toString() + state.data.day[0];
        source.data.image = source.data[path];
    }
    else {
        source.data.image = source.data.image_empty;
    }

    source.trigger('change');
"""

updateDay = """
    console.log(state.data.day + ':' + state.data.hour);
    state.data.day[0] = cb_obj.value;

    if (state.data.active.indexOf(1) > -1) {
        var path = 'image_' + state.data.hour[0] + cb_obj.value.toString();
        source.data.image = source.data[path];
    }
    else {
        source.data.image = source.data.image_empty;
    }
    source.trigger('change');
"""

updateToggles = """
    state.data.active = cb_obj.active;

    if (cb_obj.active.indexOf(0) > -1) {
        node_source.data.x_shown = node_source.data.x;
        node_source.data.y_shown = node_source.data.y;
        node_source.data.id_shown = node_source.data.id;
        node_source.trigger('change');
    }
    else {
        node_source.data.x_shown = [];
        node_source.data.y_shown = [];
        node_source.data.id_shown = [];
        node_source.trigger('change');
    }

    if (cb_obj.active.indexOf(1) > -1) {
        var path = 'image_' + state.data.hour[0] + state.data.day[0];
        image_source.data.image = image_source.data[path];
        image_source.trigger('change');
    }
    else {
        image_source.data.image = image_source.data.image_empty;
        image_source.trigger('change');
    }

    if (cb_obj.active.indexOf(2) > -1) {
        arrow_source.data.x_shown = arrow_source.data.x;
        arrow_source.data.y_shown = arrow_source.data.y;
        arrow_source.data.size_shown = arrow_source.data.size;
        arrow_source.data.color_shown = arrow_source.data.color;
        arrow_source.data.alpha_shown = arrow_source.data.alpha;
        arrow_source.trigger('change');
    }
    else {
        arrow_source.data.x_shown = [];
        arrow_source.data.y_shown = [];
        arrow_source.data.size_shown = [];
        arrow_source.data.color_shown = [];
        arrow_source.data.alpha_shown = [];
        arrow_source.trigger('change');
    }
"""