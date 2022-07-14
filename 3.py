def appearance(intervals):
    start_lesson = intervals['lesson'][0]
    end_lesson = intervals['lesson'][1]

    tutor_data_len = len(intervals['tutor'])
    pupil_data_len = len(intervals['pupil'])

    shared_time = 0

    start_shared, end_shared = 0, 0
    i_tutor, i_pupil = 1, 1
    while i_tutor < tutor_data_len and i_pupil < pupil_data_len:
        # Расчёт временных промежутков
        start_tutor = max(intervals['tutor'][i_tutor-1], end_shared)
        start_pupil = max(intervals['pupil'][i_pupil-1], end_shared)
        end_tutor = intervals['tutor'][i_tutor]
        end_pupil = intervals['pupil'][i_pupil]

        # Проверка на случай дублирующих промежутков
        if start_tutor < end_shared:
            start_tutor = end_shared
        if start_pupil < end_shared:
            start_pupil = end_shared
        if end_tutor == start_tutor:
            i_tutor += 2
            continue
        if end_pupil == start_pupil:
            i_pupil += 2
            continue

        # Сравнение временных промежутков
        if end_tutor < start_lesson or end_tutor < start_pupil:
            i_tutor += 2
            continue
        if end_pupil < start_lesson or end_pupil < start_tutor:
            i_pupil += 2
            continue
        if start_tutor > end_lesson or start_pupil > end_lesson:
            break

        # Подсчёт общего промежутка
        start_shared, end_shared = max(start_tutor, start_lesson, start_pupil), min(end_tutor, end_lesson, end_pupil)
        shared_time += end_shared - start_shared

        # Подбор новых промежутков
        if end_tutor <= end_shared:
            i_tutor += 2
        if end_pupil <= end_shared:
            i_pupil += 2
        if end_shared == end_lesson:
            break
    return shared_time


tests = [
    {'data': {'lesson': [1594663200, 1594666800],
              'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
              'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
     },
    {'data': {'lesson': [1594702800, 1594706400],
              'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150,
                        1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480,
                        1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503,
                        1594706524, 1594706524, 1594706579, 1594706641],
              'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
     'answer': 3577
     },
    {'data': {'lesson': [1594692000, 1594695600],
              'pupil': [1594692033, 1594696347],
              'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
     'answer': 3565
     },
]


if __name__ == '__main__':
    for i, test in enumerate(tests):
        test_answer = appearance(test['data'])
        assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
