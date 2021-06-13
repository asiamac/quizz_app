import csv
import uuid
import helper

import import_quiz

question_types = {
    0: { 'name': 'single choice', 'min_correct_answers': 1, 'max_correct_answers': 1 },
    1: { 'name': 'multiple choice', 'min_correct_answers': 2, 'max_correct_answers': -1 },
    2: { 'name': 'true/false' },
    3: { 'name': 'short answer' },
    4: { 'name': 'choice from the list', 'min_correct_answers': 1, 'max_correct_answers': -1 },
    5: { 'name': 'filling in words' },
    6: { 'name': 'sort items', 'min_correct_answers': -1, 'max_correct_answers': -1 },
    7: { 'name': 'matching elements' }
}

def new_quiz_title(used_titles):
    quiz_title = input('Provide name of your quiz ')

    while quiz_title == '':
        quiz_title = input('Provide name of your quiz ')

    if quiz_title in used_titles:
        text = 'Title already exists, do you want to duplicate it? Press Y for yes or N for no. '
        duplicate_title = input(text).split()[0].lower()
        while duplicate_title[0] != 'n' and duplicate_title[0] != 'y':
            duplicate_title = input(text).split()[0].lower()

        if duplicate_title[0] == 'n':
            return new_quiz_title(used_titles)
        else:
            return quiz_title
    else:
        return quiz_title

def create_question_with_answer_selection(type):
    answer_options = []
    correct_answer = []
    while True:
        single_option = input('Provide answer ')
        answer_options.append(single_option)
        another_anwser = helper.provide_boolean_value('Do you want to add another option answer? Press Y for yes or N for no. ')
        if not another_anwser:
            break


    correct_answer_text = 'Provide index of correct_answer: ' + str(answer_options) + '.'

    len_answer_options = len(answer_options)

    max_iterations = question_types[type]['max_correct_answers'] if question_types[type]['max_correct_answers'] >= 0 else len_answer_options
    min_iterations = question_types[type]['min_correct_answers'] if question_types[type]['min_correct_answers'] >= 0 else len_answer_options
    
    for i in range(max_iterations):
        correct_answer_index = helper.provide_positive_int_value(correct_answer_text, len_answer_options)
        while correct_answer_index >= len_answer_options or correct_answer_index in correct_answer:
            correct_answer_index = helper.provide_positive_int_value(correct_answer_text, len_answer_options)
        correct_answer.append(answer_options[correct_answer_index])

        if i >= min_iterations - 1 and i < max_iterations - 1:
            another_correct_anwser = helper.provide_boolean_value('Do you want to add another correct answer? Press Y for yes or N for no. ')
            if not another_correct_anwser:
                break
    
    return answer_options, correct_answer

def create_boolean_question():
    answer_options = []
    correct_answer = []

    answer_options = [True, False]
    is_true_correct = helper.provide_boolean_value('Is true correct answer? Press Y for yes or N for no. ')
    correct_answer.append(is_true_correct)

    return answer_options, correct_answer

def create_short_answer_question():
    correct_answer = []
    short_answer = input('Provide correct answer ')
    correct_answer.append(short_answer)

    return correct_answer

def create_filling_words():
    answer_options = []
    correct_answer = []
    
    input_before_gap = input('Provide text before gap ')
    input_after_gap = input('Provide text after gap ')
    answer_options.append(input_before_gap)
    answer_options.append(input_after_gap)
    gap_answer = input('Provide correct answer ')
    correct_answer.append(gap_answer)

    return answer_options, correct_answer

def create_matching_task():
    answer_options = []
    correct_answer = []

    left_column = []
    while True:
        single_option = input('Provide single option answer to left column: ')
        left_column.append(single_option)
        another_anwser = helper.provide_boolean_value('Do you want to add another position to left column? Press Y for yes or N for no. ')
        if not another_anwser:
            break

    right_column = []

    len_left_column = len(left_column)

    for _i in range(len_left_column):
        single_option = input('Provide single option answer to right column: ')
        right_column.append(single_option)

    answer_options.append(left_column)
    answer_options.append(right_column)

    for i in range(len_left_column):
        correct_answer_text = 'Provide index of correct right column answer corresponding to element of index of ' + str(left_column[i]) + ' in left column : ' + str(answer_options[1]) + '. '
        correct_answer_index = helper.provide_positive_int_value(correct_answer_text, len_left_column)
        while correct_answer_index >= len_left_column or correct_answer_index in correct_answer:
            correct_answer_index = helper.provide_positive_int_value(correct_answer_text, len_left_column)
        answer_item = [left_column[i], right_column[correct_answer_index]]
        correct_answer.append(answer_item)

    return answer_options, correct_answer

def get_question_patameters():
    options_text = helper.provide_available_options(question_types)
    if options_text ==  None:
        print('It is not possible to create quiz now, try again later.')
    else:
        text = 'What type of question do you want to create:' + options_text + '.'
        question_type = helper.provide_positive_int_value(text, 8)
        while question_type > 7:
            question_type = helper.provide_positive_int_value(text, 8)

        question = input('Provide question: ')
        answer_options = []
        correct_answer = []

        if question_type in (0, 1, 4, 6):
            answer_options, correct_answer = create_question_with_answer_selection(question_type)

        if question_type == 2:
            answer_options, correct_answer =create_boolean_question()

        if question_type == 3:
            correct_answer = create_short_answer_question()

        if question_type == 5:
            answer_options, correct_answer = create_filling_words()        

        if question_type == 7:
            answer_options, correct_answer = create_matching_task()

        return question_type, question, answer_options, correct_answer

def create_new_question():
    id = uuid.uuid4()
    question_type, question, answer_options, correct_answer = get_question_patameters()
    penalty_points = helper.provide_float_value('Should there be penalty points? If yes provide float value between 0 and 1, if no type anything else. ')
    time_limit = helper.provide_positive_int_value('Should there be time limit? If yes provide positivie integer value, if no type anything else. ')
    has_shuffled_answers = helper.provide_boolean_value('Should answers in quiz be shuffled? Press Y for yes or N for no. ')
    return id, question_type, question, answer_options, correct_answer, penalty_points, time_limit, has_shuffled_answers

def create_quiz_manually(id):
    quiz_questions_file = open(id + '.csv','w',newline='\n')
    csv_write_question = csv.writer(quiz_questions_file, delimiter = ';', lineterminator='\n')
    csv_write_question.writerow(['id','question_type','question','answer_options','correct_answer','penalty_points','time_limit','has_shuffle_answers'])
    
    while True:
        csv_write_question.writerow(create_new_question())
        another_question = helper.provide_boolean_value('Do you want to add another question? Press Y for yes or N for no. ')
        if not another_question:
            break

    quiz_questions_file.close()

def create_quiz(existing_quiz_titles):
    id = str(uuid.uuid4())
    title = new_quiz_title(existing_quiz_titles)
    has_shuffled_questions = helper.provide_boolean_value('Should questions in quiz be shuffled? Press Y for yes or N for no. ')
    can_go_back = helper.provide_boolean_value('Can go back to questions in quiz? Press Y for yes or N for no. ')

    quiz_list_file = open('quiz_list.csv','a',newline='\n')
    csv_writer = csv.writer(quiz_list_file, delimiter = ';', lineterminator='\n')
    csv_writer.writerow([id, title, has_shuffled_questions, can_go_back])
    quiz_list_file.close()

    is_create_manually = helper.provide_boolean_value('Do you want to create quiz manually? Press Y for yes or N if you want to import ready questions file. ')

    if is_create_manually:
        create_quiz_manually(id)
    else:
        import_quiz.import_quiz(id)
