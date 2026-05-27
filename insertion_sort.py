def insertion_sort(productos):
    productos_ordenados = productos.copy()

    for i in range(1, len(productos_ordenados)):
        actual = productos_ordenados[i]
        j = i - 1

        while j >= 0 and productos_ordenados[j].fecha_vencimiento > actual.fecha_vencimiento:
            productos_ordenados[j + 1] = productos_ordenados[j]
            j -= 1

        productos_ordenados[j + 1] = actual

    return productos_ordenados
