# Size should be normalized
def lineToArrow(data, i, xs, ys, vs):
    # Calculate delta vector
    delta_x = data[xs][i][1] - data[xs][i][0]
    delta_y = data[ys][i][1] - data[ys][i][0]

    length = (delta_x ** 2 + delta_y ** 2) ** 0.5

    # Normalize delta vector
    delta_x = delta_x * data[vs][i] / length
    delta_y = delta_y * data[vs][i] / length

    # Determine tangent vector for delta vector
    tangent_x = delta_y
    tangent_y = -delta_x

    # Add extra points
    data[xs][i].append(data[xs][i][1] - tangent_x - delta_x * 2)
    data[xs][i].append(data[xs][i][1] + tangent_x / 2 + delta_x * 1.5 - delta_x * 2)
    data[xs][i].append(data[xs][i][1] + tangent_x * 2 - delta_x * 2)
    data[xs][i].append(data[xs][i][1] + tangent_x - delta_x * 2)
    data[xs][i].append(data[xs][i][0] + tangent_x + delta_x / data[vs][i] * 40)
    data[xs][i][1] -= delta_x * 2
    data[xs][i][0] += delta_x / data[vs][i] * 40

    data[ys][i].append(data[ys][i][1] - tangent_y - delta_y * 2)
    data[ys][i].append(data[ys][i][1] + tangent_y / 2 + delta_y * 1.5 - delta_y * 2)
    data[ys][i].append(data[ys][i][1] + tangent_y * 2 - delta_y * 2)
    data[ys][i].append(data[ys][i][1] + tangent_y - delta_y * 2)
    data[ys][i].append(data[ys][i][0] + tangent_y + delta_y / data[vs][i] * 40)
    data[ys][i][1] -= delta_y * 2
    data[ys][i][0] += delta_y / data[vs][i] * 40
