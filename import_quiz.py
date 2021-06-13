import csv

def import_quiz(id):
    print('CSV file needed with header: id, question_type, question, answer_options, correct_answer, penalty_points, time_limit, has_shuffled_answers')
    file_path = input('Provide file path with extension: ')
    temp_data = []
    read_file = open(file_path,'r')
    reader = csv.reader(read_file,  delimiter=';')
    for row in reader:
        temp_data.append(row)
    read_file.close()

    quiz_questions_file = open(id + '.csv','w',newline='\n')
    csv_write_question = csv.writer(quiz_questions_file, delimiter = ';', lineterminator='\n')
    for temp_row in temp_data:
        csv_write_question.writerow(temp_row)
    
    quiz_questions_file.close()
    