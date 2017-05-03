from random import randint

# Generate an example path that includes all the nodes
def generateExampleNetworkData(source, xs, ys, vs, nodes):
    # Define path with node_ids
    example_path = [259, 254, 256, 251, 252, 258, 253, 250, 257]
    reverse_path = example_path[::-1]
    
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
            source.data[xs].append(points_x)
            source.data[ys].append(points_y)
            source.data[vs].append(randint(10,20))
        last = node

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
            source.data[xs].append(points_x)
            source.data[ys].append(points_y)
            source.data[vs].append(randint(10, 20))
        last = node

def generateEventsForNode():
    return randint(0,5)