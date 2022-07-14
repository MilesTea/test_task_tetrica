def task(array):
    """
    Бинарный поиск первого нуля по массиву,
    состоящему из некоторого количества подряд идущих единиц,
    за которыми следует какое-то количество подряд идущих нулей.
    :param array: массив
    :return: индекс найденного элемента
    """
    start = 1
    end = len(array) - 1

    while start <= end:
        mid = (start + end) // 2
        if array[mid] == 0:
            if array[mid - 1] == 1:
                return mid

            else:
                end = mid - 1

        elif array[mid] == 1:
            start = mid + 1

        else:
            return f'Обнаружено некорректное значение на позиции {mid}'

    return 'Не найден'


print(task([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]))
