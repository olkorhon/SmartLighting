updateHour = """
    state.data.hour[0] = cb_obj.value;
    console.log(state.data.day + ':' + state.data.hour);

     // Always update energy savings
    var postfix = '_' + state.data.hour[0] + state.data.day[0]
    energy_source.data.savings_shown = energy_source.data['savings' + postfix];
    energy_source.trigger('change');

    if (state.data.active.indexOf(1) > -1) {
        heat_source.data.image = heat_source.data['image' + postfix];
        heat_source.trigger('change');
    }
    else {
        heat_source.data.image = heat_source.data.image_empty;
        heat_source.trigger('change');
    }

    // Update network if it is active
    if (state.data.active.indexOf(2) > -1) {
        console.log('Updating arrow network');
        arrow_source.data.x_shown = arrow_source.data['x' + postfix];
        arrow_source.data.y_shown = arrow_source.data['y' + postfix];
        arrow_source.data.size_shown = arrow_source.data['size' + postfix];
        arrow_source.data.color_shown = arrow_source.data['color' + postfix];
        arrow_source.data.alpha_shown = arrow_source.data['alpha' + postfix];
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

updateDay = """
    state.data.day[0] = cb_obj.value;
    console.log(state.data.day + ':' + state.data.hour);

    // Always update energy savings
    var postfix = '_' + state.data.hour[0] + state.data.day[0]
    energy_source.data.savings_shown = energy_source.data['savings' + postfix];
    energy_source.trigger('change');

    // Update heatmap if it is active
    if (state.data.active.indexOf(1) > -1) {
        console.log('Updating heatmap');
        heat_source.data.image = heat_source.data['image' + postfix];
        heat_source.trigger('change');
    }
    else {
        heat_source.data.image = heat_source.data.image_empty;
        heat_source.trigger('change');
    }

    // Update network if it is active
    if (state.data.active.indexOf(2) > -1) {
        console.log('Updating arrow network');
        arrow_source.data.x_shown = arrow_source.data['x' + postfix];
        arrow_source.data.y_shown = arrow_source.data['y' + postfix];
        arrow_source.data.size_shown = arrow_source.data['size' + postfix];
        arrow_source.data.color_shown = arrow_source.data['color' + postfix];
        arrow_source.data.alpha_shown = arrow_source.data['alpha' + postfix];
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

updateToggles = """
    state.data.active = cb_obj.active;
    var postfix = '_' + state.data.hour[0] + state.data.day[0]

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

    if (state.data.active.indexOf(1) > -1) {
        heat_source.data.image = heat_source.data['image' + postfix];
        heat_source.trigger('change');
    }
    else {
        heat_source.data.image = heat_source.data.image_empty;
        heat_source.trigger('change');
    }

    if (state.data.active.indexOf(2) > -1) {
        arrow_source.data.x_shown = arrow_source.data['x' + postfix];
        arrow_source.data.y_shown = arrow_source.data['y' + postfix];
        arrow_source.data.size_shown = arrow_source.data['size' + postfix];
        arrow_source.data.color_shown = arrow_source.data['color' + postfix];
        arrow_source.data.alpha_shown = arrow_source.data['alpha' + postfix];
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