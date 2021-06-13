import csv
import random

import helper
import menu
import ranking

def get_user_name():
    text = 'What is your name? '
    name = input(text)
    while len(name) == 0:
        name = input(text)
    print('Hello', name)
    return name

def check_question_type(value):
    try:
        integer_value = int(value)
        if integer_value < 0 or integer_value > 7:
            return -1
        else:
            return integer_value
    except ValueError:
        return -1

def naviagate(question_index):
    if question_index == 0:
        return 1
    else:
        is_go_forward = helper.provide_boolean_value('Do you want to go forward? Press Y for yes or N if you want to go back. ')
        if is_go_forward:
            return 1
        else:
            return -1

def parse_question_data(data):
    result = 0.00
    question = data[2]
    available_anwsers = eval(data[3])
    correct = eval(data[4])
    shuffle_answer = data[7] == 'True'
    penalty_points = helper.parse_to_float(data[5])

    if shuffle_answer:
        random.shuffle(available_anwsers)
    
    return result, question, available_anwsers, correct, shuffle_answer, penalty_points

def render_single_select(question_data):
    result, question, available_anwsers, correct, shuffle_answer, penalty_points = parse_question_data(question_data)

    if shuffle_answer:
        random.shuffle(available_anwsers)
    
    available_anwser_text = ['\nto choose ' + str(answer) + ' press ' + str(index) for index, answer in enumerate(available_anwsers)]

    print(question, *available_anwser_text)
    answer = input()

    try:
        answer_index = int(answer)
        if available_anwsers[answer_index] == correct[0]:
            result += 1.00
        else:
            result -= float(penalty_points)

    except:
        result -= float(penalty_points)
    
    return result

def render_multiselect(question_data):
    result, question, available_anwsers, correct, shuffle_answer, penalty_points = parse_question_data(question_data)
    
    if shuffle_answer:
        random.shuffle(available_anwsers)

    available_anwser_text = ['\nto choose ' + str(answer) + ' press ' + str(index) for index, answer in enumerate(available_anwsers)]

    print(question, *available_anwser_text)

    answers = []
    
    another_anwser = True
    while another_anwser:
        try:
            answer_index = int(input('Choose index of an answeer to tick. '))
            answer = available_anwsers[answer_index]  
            if answer in answers:
                remove = helper.provide_boolean_value('Do you want to untick already ticked answer? Press Y for yes or N for no. ')
                if remove:
                    answers.remove(answer)
            else:
                answers.append(answer)
            another_anwser = helper.provide_boolean_value('Do you want to tick another answer? Press Y for yes or N for no. ')
        except (ValueError, IndexError):
            another_anwser = helper.provide_boolean_value('Cannot parse answer, do you want to try again to tick answer? Press Y for yes or N for no. ')

    try:
        if len(answers) == len(correct):
            for element in correct:
                if element in correct:
                    continue
                else:
                    correct_len = len(correct)
                    partial_point = 1.00 / correct_len
                    for element in answers:
                        if element in correct:
                            result +=  partial_point
                        else:
                            result -= float(penalty_points)
                    return result

            result += 1.00
        else:
            correct_len = len(correct)
            partial_point = 1.00 / correct_len
            for element in answers:
                if element in correct:
                    result +=  partial_point
                else:
                    result -= float(penalty_points)

    except:
        result -= 0.00
    
    return result

def render_boolean(question_data):
    result, question, available_anwsers, correct, shuffle_answer, penalty_points = parse_question_data(question_data)

    if shuffle_answer:
        random.shuffle(available_anwsers)
    
    available_anwser_text = ['\nto choose ' + str(answer) + ' press ' + str(index) for index, answer in enumerate(available_anwsers)]

    print(question, *available_anwser_text)

    answer = input()

    try:
        answer_index = int(answer)
        if bool(available_anwsers[answer_index]) == bool(correct[0]):
            result += 1.00
        else:
            result -= float(penalty_points)

    except:
        result -= float(penalty_points)
    
    return result

def render_short_answer(question_data):
    result, question, available_anwsers, correct, shuffle_answer, penalty_points = parse_question_data(question_data)
    
    print(question)
    answer = input('Give an answer')

    try:
        if correct[0].lower() == answer.lower():
            result += 1.00
        else:
            result -= penalty_points

    except:
        result -= penalty_points
    
    return result

def render_list_options(question_data):
    result, question, available_anwsers, correct, shuffle_answer, penalty_points = parse_question_data(question_data)
    if shuffle_answer:
        random.shuffle(available_anwsers)
    
    available_anwser_text = ['\nto choose ' + str(answer) + ' press ' + str(index) for index, answer in enumerate(available_anwsers)]

    print(question, *available_anwser_text)

    answers = []
    
    another_anwser = True
    while another_anwser:
        try:
            answer_index = int(input('Choose index of an answeer to add to the list. '))
            answer = available_anwsers[answer_index]  
            if answer in answers:
                remove = helper.provide_boolean_value('Do you want to remove item already added to the list? Press Y for yes or N for no. ')
                if remove:
                    answers.remove(answer)
            else:
                answers.append(answer)
            another_anwser = helper.provide_boolean_value('Do you want to add another item to the list? Press Y for yes or N for no. ')
        except (ValueError, IndexError):
            another_anwser = helper.provide_boolean_value('Cannot parse choice, do you want to try again to add item to a list? Press Y for yes or N for no. ')

    try:
        if len(answers) == len(correct):
            for element in correct:
                if element in correct:
                    continue
                else:
                    correct_len = len(correct)
                    partial_point = 1.00 / correct_len
                    for element in answers:
                        if element in correct:
                            result +=  partial_point
                        else:
                            result -= float(penalty_points)
                    return result

            result += 1.00
        else:
            correct_len = len(correct)
            partial_point = 1.00 / correct_len
            for element in answers:
                if element in correct:
                    result +=  partial_point
                else:
                    result -= float(penalty_points)

    except:
        result -= 0.00
    
    return result

def render_filling_words(question_data):
    result, question, available_anwsers, correct, shuffle_answer, penalty_points = parse_question_data(question_data)

    text =  available_anwsers[0] + ' ... ' + available_anwsers[1]
    answer = input(text)

    try:
        if correct[0].lower() == answer.lower():
            result += 1.00
        else:
            result -= penalty_points

    except:
        result -= penalty_points
    
    return result

def render_sorting(question_data):
    result, question, available_anwsers, correct, shuffle_answer, penalty_points = parse_question_data(question_data)

    if shuffle_answer:
        random.shuffle(available_anwsers)
    
    available_anwser_text = ['\nto choose ' + str(answer) + ' press ' + str(index) for index, answer in enumerate(available_anwsers)]

    print(question, *available_anwser_text)

    answers = []

    len_available_answers = len(available_anwsers)

    i = 0
    for _i in range(len_available_answers):
        answers.append('...')
    
    while i < len_available_answers:
        try:
            text = 'Choose index of element to put it in index of ' + str(i) + ' position '
            print('Your current sorted order is:')
            print(* answers)
            answer_index = int(input(text))
            answer = available_anwsers[answer_index]  
            if answer in answers:
                remove = helper.provide_boolean_value('Do you want to remove answer from previous postion and put in new one? Press Y for yes or N for no. ')
                if remove:
                    index = answers.index(answer)
                    answers[index] = '...'
                    answers[i] = answer

            else:
                answers[i] = answer

            if i > 0:
                is_go_forward = helper.provide_boolean_value('Do you want to go forward? Press Y for yes or N if you want to go back. ')
                if is_go_forward:
                    i += 1
                else:
                    i -= 1
            else:
                i += 1
        except (ValueError, IndexError):
            stay = helper.provide_boolean_value('Cannot parse answer, do you want to try again? Press Y for yes or N for no. ')
            if not stay:
                i +=1

    try:
        partial_point = 1.00 / len(correct)
        for index, element in enumerate(answers):
            if element == correct[index]:
                result += partial_point
            else:
                result -= penalty_points
        return result

    except:
        result -= 0.00
    
    return result

def render_matching(question_data):
    result, question, available_anwsers, correct, shuffle_answer, penalty_points = parse_question_data(question_data)
    first_column = available_anwsers[0]
    second_column = available_anwsers[1]
    user_result = result
 
    if shuffle_answer:
        random.shuffle(first_column)
        random.shuffle(second_column)
    
    available_anwser_text = ['\nto choose ' + str(answer) + ' press ' + str(index) for index, answer in enumerate(second_column)]

    print(question, *first_column, 'with', *available_anwser_text)

    answers = []

    len_available_answers = len(second_column)

    i = 0
    for _i in range(len_available_answers):
        answers.append('...')
    
    while i < len_available_answers:
        try:
            text = 'Choose index of element to put match it to ' + first_column[i] + ' element '
            print('Your current matched element is: ')
            matched_elements = [str(i) + ' ' + first_column[i] + ' ' + answers[i] for i in range(len_available_answers)]
            print(*matched_elements)
            answer_index = int(input(text))
            answer = second_column[answer_index]  
            if answer in answers:
                remove = helper.provide_boolean_value('Do you want to remove item from previous match and put in new one? Press Y for yes or N for no. ')
                if remove:
                    index = answers.index(answer)
                    answers[index] = '...'
                    answers[i] = answer

            else:
                answers[i] = answer

            if i > 0:
                is_go_forward = helper.provide_boolean_value('Do you want to go forward? Press Y for yes or N if you want to go back. ')
                if is_go_forward:
                    i += 1
                else:
                    i -= 1
            else:
                i += 1
        except (ValueError, IndexError):
            stay = helper.provide_boolean_value('Cannot parse answer, do you want to try again? Press Y for yes or N for no. ')
            if not stay:
                i +=1

    try:
        partial_point = 1.00 / len(correct)
        for element in correct:
            left_correct = element[0]
            right_correct = element[1]
            index_to_check = first_column.index(left_correct)
            if right_correct == answers[index_to_check]:
                user_result += partial_point
            else:
                user_result -= penalty_points
        return user_result

    except:
        user_result -= 0.00
    
    return user_result

def write_result_to_file(id, user_name, result):
    file_name = 'ranking-' + str(id) + '.txt'
    file = open(file_name, 'a')
    ranking_row = user_name + ':' + str(result)
    file.write(str(ranking_row))
    file.close()

def solve_quiz(quiz_data):
    user_name = get_user_name()
    id = quiz_data['id']
    name = quiz_data['name']
    shuffle_questions = quiz_data['shuffle_questions'] == 'True'
    can_go_back = quiz_data['can_go_back'] == 'True'
    result = [0.00]

    question_data = []
    try:
        read_file = open(id + '.csv','r')
    except FileNotFoundError:
        print('Error: file not found')
        return menu.main_menu()

    reader = csv.reader(read_file,  delimiter=';')
    header = next(reader)

    for row in reader:
        question_data.append(row)
    read_file.close()

    if shuffle_questions:
        random.shuffle(question_data)

    questions_len = len(question_data)
    index = 0

    for _i in range(1,questions_len):
        result.append(0.00)

    while index < questions_len:
        current_question = question_data[index]
        type =  check_question_type(current_question[1])
        if type == 0:
            result[index] += render_single_select(current_question)
        elif type == 1:
            result[index] += render_multiselect(current_question)
        elif type == 2:
            result[index] += render_boolean(current_question)
        elif type == 3:
            result[index] += render_short_answer(current_question)
        elif type == 4:
            result[index] += render_list_options(current_question)
        elif type == 5:
            result[index] += render_filling_words(current_question)
        elif type == 6:
            result[index] += render_sorting(current_question)
        elif type == 7:
            result[index] += render_matching(current_question)
        
        if can_go_back:            
            index += naviagate(index)
        else:
            index += 1
                
    result = sum(map(float,result))
    ranking.save_and_show_results(id, user_name, result)
    print(user_name, result)
