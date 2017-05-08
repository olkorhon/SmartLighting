from random import randint

# Generate an example path that includes all the nodes
def generateExampleNetworkData(xs, ys, vs, nodes, data=None):
    # Create empty container for data
    if data == None:
        data = {xs:[], ys:[], vs:[]}
    else:
        # Define arrays that are not already in the dictionary
        if xs not in data:
            data[xs] = []

        if ys not in data:
            data[ys] = []

        if vs not in data:
            data[vs] = []

    # Define path with node_ids
    example_path = [259, 254, 256, 251, 252, 258, 253, 250, 257]
    
     # Make example lines
    last = None
    for node in example_path:
        if last != None:
            points_x = []
            points_y = []
            points_x.append(nodes[last].pos_x)
            points_x.append(nodes[node].pos_x)
            points_y.append(207 - nodes[last].pos_y)
            points_y.append(207 - nodes[node].pos_y)

            data[xs].append(points_x)
            data[ys].append(points_y)
            data[vs].append(randint(10,20))
        last = node

    return data

    # Reverse list
    last = None
    for node in reverse_path:
        if last != None:
            points_x = []
            points_y = []
            points_x.append(nodes[last].pos_x)
            points_x.append(nodes[node].pos_x)
            points_y.append(207 - nodes[last].pos_y)
            points_y.append(207 - nodes[node].pos_y)

            data[xs].append(points_x)
            data[ys].append(points_y)
            data[vs].append(randint(10, 20))
        last = node

    return data


def generateSavingData():
    return [randint(5, 90) for i in range(24)]


def generateEventsForNode():
    return randint(0,5)