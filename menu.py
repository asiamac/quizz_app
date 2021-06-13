import csv
import sys

import create
import helper
import solve

def get_quiz_options():
    quiz_list_file = open('quiz_list.csv','r')
    reader = csv.reader(quiz_list_file,  delimiter=';')
    header = next(reader)

    quiz_list = {}

    for quiz_index, quiz in enumerate(reader):
        quiz_list[quiz_index] = {}
        for attribute_index, attribute in enumerate(quiz):
            quiz_list[quiz_index][header[attribute_index]] = attribute

    quiz_list_file.close()

    return quiz_list

def create_main_menu_text(options = []):
    options_text = helper.provide_available_options(options)
    return 'What do you want to do:\n- solve the quiz about:' + options_text + '\n- create a new quiz press: C,\n- close app press: Q.\n'
    
def quiz_titles(quizes = []):
    return [quizes[quiz]['name'] for quiz in quizes if quizes[quiz]['name'] != '']

def main_menu():
    quiz_options = get_quiz_options()
    text = create_main_menu_text(quiz_options)

    def choose_option():
        try:
            choice = input(text).split()[0].lower()
            while len(choice) == 0:
                choice = input(text).split()[0].lower()
        except IndexError:
            print('Choose some option.')
            choose_option()

        if choice == 'c':
            titles = quiz_titles(quiz_options)
            create.create_quiz(titles)
        elif choice == 'q':
            sys.exit()
        else:
            try:
                choosen_value= int(choice)
                choosen_quiz = quiz_options[choosen_value]
                solve.solve_quiz(choosen_quiz)
            except (ValueError, KeyError):
                print('There is no such option, try again.')
                choose_option()
    
    choose_option()
