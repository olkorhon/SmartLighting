# Size should be normalized
def lineToArrow(points_x, points_y, size):
    # Calculate delta vector
    delta_x = points_x[1] - points_x[0]
    delta_y = points_y[1] - points_y[0]

    length = (delta_x ** 2 + delta_y ** 2) ** 0.5

    # Normalize delta vector
    delta_x = delta_x * size / length
    delta_y = delta_y * size / length

    # Determine tangent vector for delta vector
    tangent_x = delta_y
    tangent_y = -delta_x

    arrow_x = []
    arrow_y = []

    # Add extra points
    arrow_x.append(points_x[0] + delta_x / size * 40)
    arrow_x.append(points_x[1] - delta_x * 2)
    arrow_x.append(points_x[1] - tangent_x - delta_x * 2)
    arrow_x.append(points_x[1] + tangent_x / 2 + delta_x * 1.5 - delta_x * 2)
    arrow_x.append(points_x[1] + tangent_x * 2 - delta_x * 2)
    arrow_x.append(points_x[1] + tangent_x - delta_x * 2)
    arrow_x.append(points_x[0] + tangent_x + delta_x / size * 40)

    arrow_y.append(points_y[0] + delta_y / size * 40)
    arrow_y.append(points_y[1] - delta_y * 2)
    arrow_y.append(points_y[1] - tangent_y - delta_y * 2)
    arrow_y.append(points_y[1] + tangent_y / 2 + delta_y * 1.5 - delta_y * 2)
    arrow_y.append(points_y[1] + tangent_y * 2 - delta_y * 2)
    arrow_y.append(points_y[1] + tangent_y - delta_y * 2)
    arrow_y.append(points_y[0] + tangent_y + delta_y / size * 40)

    return (arrow_x, arrow_y)


