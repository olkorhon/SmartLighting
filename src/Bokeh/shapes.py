# Size should be normalized
def lineToArrow(points_x, points_y, size):
    # Calculate delta vector
    dx = points_x[1] - points_x[0]
    dy = points_y[1] - points_y[0]

    length = (dx ** 2 + dy ** 2) ** 0.5

    unit_delta_x = dx / length
    unit_delta_y = dy / length

    # Normalize delta vector
    dx = dx * size / length
    dy = dy * size / length

    # Determine tangent vector for delta vector
    tangent_x = dy
    tangent_y = -dx

    unit_tangent_x = unit_delta_y
    unit_tangent_y = -unit_delta_x

    arrow_x = []
    arrow_y = []

    # Add extra points
    arrow_x.append(points_x[0]                                     + unit_delta_x * 50 + unit_tangent_x)
    arrow_x.append(points_x[1] - dx * 2                            - unit_delta_x * 10 + unit_tangent_x)
    arrow_x.append(points_x[1] - tangent_x                - dx * 2 - unit_delta_x * 10 + unit_tangent_x)
    arrow_x.append(points_x[1] + tangent_x / 2 + dx * 1.5 - dx * 2 - unit_delta_x * 10 + unit_tangent_x)
    arrow_x.append(points_x[1] + tangent_x * 2 - dx * 2            - unit_delta_x * 10 + unit_tangent_x)
    arrow_x.append(points_x[1] + tangent_x     - dx * 2            - unit_delta_x * 10 + unit_tangent_x)
    arrow_x.append(points_x[0] + tangent_x                         + unit_delta_x * 50 + unit_tangent_x)

    arrow_y.append(points_y[0]                                     + unit_delta_y * 50 + unit_tangent_y)
    arrow_y.append(points_y[1] - dy * 2                            - unit_delta_y * 10 + unit_tangent_y)
    arrow_y.append(points_y[1] - tangent_y                - dy * 2 - unit_delta_y * 10 + unit_tangent_y)
    arrow_y.append(points_y[1] + tangent_y / 2 + dy * 1.5 - dy * 2 - unit_delta_y * 10 + unit_tangent_y)
    arrow_y.append(points_y[1] + tangent_y * 2 - dy * 2            - unit_delta_y * 10 + unit_tangent_y)
    arrow_y.append(points_y[1] + tangent_y     - dy * 2            - unit_delta_y * 10 + unit_tangent_y)
    arrow_y.append(points_y[0] + tangent_y                         + unit_delta_y * 50 + unit_tangent_y)

    return (arrow_x, arrow_y)


