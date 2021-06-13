import matplotlib.pyplot as plt

def add_user_result(results, user_name, user_result):
    user_found = False
    
    for index, result in enumerate(results):
        try:
            if result[0] == user_name:
                user_found = True
                if user_result > float(result[1]):
                    result[1] = user_result
                else:
                    result[1] = float(result[1])
        except:
            to_delete = results.pop(index)
            print('There was problem with following result: ' + str(to_delete) + '. It was removed from the ranking.')

    if not user_found:
        results.append([user_name, user_result])

    return results

def sort_results(results):
    comparision_len = len(results) - 1
    
    if comparision_len < 0:
        return results

    def max_index_result(results_to_sort):
        max_index = 0
        for index, singel_result in enumerate(results_to_sort):
            if singel_result[1] > results_to_sort[max_index][1]:
                max_index = index
        return max_index

    for i in range(comparision_len):
        unsorted_results = results[i:]
        swap_index = max_index_result(unsorted_results)

        if swap_index != 0:
            results[i], results[i + swap_index] = results[i + swap_index], results[i]

    return results

def show_results(results, user_result):
    name = []
    max_x = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    name_position = []
    points = []
    max_y_val = 0

    results_to_show = results[:10]

    for index, result in enumerate(results_to_show):
        if index == 0:
            max_y_val = result[1] + 1.00
        name.append(result[0])
        points.append(result[1])
        name_position.append(max_x[index])

    number_of_position_showed = len(name_position)

    bar_width = 4

    plt.bar(name_position,points,bar_width,color=('r','k','g','b','yellow'))

    text = 'Ranking of top ' + str(number_of_position_showed) +'.\nYour score was ' + str(user_result) + '.'
    x_max_value = number_of_position_showed * 5
    plt.title(text)
    plt.xlabel('Name')
    plt.ylabel('Points')
    plt.xticks(name_position,name)
    plt.axis([0,x_max_value,0,max_y_val])
    plt.minorticks_on()

    plt.show()

def save_and_show_results(id, user_name, user_result):
    file_name = 'ranking-' + str(id) + '.txt'

    results = []
    try:
        read_file = open(file_name,'r')
        reader = read_file.readlines()
        for line in reader:
            row = line.split()
            results.append(row)
        read_file.close()

        results = add_user_result(results, user_name, user_result)

        results = sort_results(results)

    except FileNotFoundError:
        results.append([user_name, user_result])

    write_file = open(file_name,'w')

    for result in results:
        text = str(result[0]) + ' ' + str(result[1]) + '\n'
        write_file.write(text)
    
    write_file.close()

    show_results(results, user_result)
