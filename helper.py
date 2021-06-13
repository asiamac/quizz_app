def provide_available_options(options = []):
    options_text = ''
    try:
        for key in options:
            name = options[key]['name'] if options[key]['name'] != '' else 'SUPRISE' 
            options_text += '\n  * ' + name + ' press: ' + str(key) + ','
        return options_text
    except TypeError:
        return None

def provide_boolean_value(text):
    try:
        value = input(text).split()[0].lower()
        while value[0] != 'n' and value[0] != 'y':
            value = input(text).split()[0].lower()
        
        return value[0] == 'y'
    except IndexError:
        print('There is no such option, try again.')
        return provide_boolean_value(text)


def provide_float_value(text):
    try:
        float_value = float(input(text))
        if float_value <= 0 or float_value > 1:
            return 0
        else:
            return float_value
    except ValueError:
        return 0

def provide_positive_int_value(text = '', error_value = 0):
    try:
        integer_value = int(input(text))
        if integer_value < 0:
            return error_value
        else:
            return integer_value
    except ValueError:
        return error_value

def parse_to_float(value):
    try:
        eval_value = eval(value)
        float_value = float(eval_value)
        if float_value > 0.00:
            return float_value
        else:
            return 0.00

    except:
        return 0.00
