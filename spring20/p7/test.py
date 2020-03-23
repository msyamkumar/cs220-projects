import ast
import os
import re
import sys
import json
import math
import collections

import nbconvert
import nbformat

PASS = "PASS"
TEXT_FORMAT = "text"

Question = collections.namedtuple("Question", ["number", "weight", "format"])

questions = [
    Question(number=1, weight=1, format=TEXT_FORMAT),
    Question(number=2, weight=1, format=TEXT_FORMAT),
    Question(number=3, weight=1, format=TEXT_FORMAT),
    Question(number=4, weight=1, format=TEXT_FORMAT),
    Question(number=5, weight=1, format=TEXT_FORMAT),
    Question(number=6, weight=1, format=TEXT_FORMAT),
    Question(number=7, weight=1, format=TEXT_FORMAT),
    Question(number=8, weight=1, format=TEXT_FORMAT),
    Question(number=9, weight=1, format=TEXT_FORMAT),
    Question(number=10, weight=1, format=TEXT_FORMAT),
    Question(number=11, weight=1, format=TEXT_FORMAT),
    Question(number=12, weight=1, format=TEXT_FORMAT),
    Question(number=13, weight=1, format=TEXT_FORMAT),
    Question(number=14, weight=1, format=TEXT_FORMAT),
    Question(number=15, weight=1, format=TEXT_FORMAT),
    Question(number=16, weight=1, format=TEXT_FORMAT),
    Question(number=17, weight=1, format=TEXT_FORMAT),
    Question(number=18, weight=1, format=TEXT_FORMAT),
    Question(number=19, weight=1, format=TEXT_FORMAT),
    Question(number=20, weight=1, format=TEXT_FORMAT),
]
question_nums = set([q.number for q in questions])

# JSON and plaintext values
expected_json = {
    "1": 'A. Hložek',
    "2": 'L. Messi',
    "3": 'Neymar Jr',
    "4": 'LW',
    "5": ['FC Barcelona', 'Juventus', 'Paris Saint-Germain', 'Atlético Madrid', 'Real Madrid'],
    "6": ['A. Abdallah', 'A. Abdellaoui', 'A. Abdennour', 'A. Abdi', 'A. Abdu', 'A. Abedzadeh'],
    "7": 9456.942772732247,
    "8": 66.24499398183609,
    "9": 2036,
    "10": 1146,
    "11": 'CB',
    "12": {'ID': '183277',
             'Name': 'E. Hazard',
             'Age': 28,
             'Nationality': 'Belgium',
             'Overall': 91,
             'Club': 'Real Madrid',
             'Position': 'LW',
             'Value': '€90M',
             'Wage': '€470K',
             'Preferred Foot': 'Right',
             'Jersey Number': '7',
             'Height': "5'9",
             'Weight': '163lbs'},
    "13": {'ID': '209331',
             'Name': 'M. Salah',
             'Age': 27,
             'Nationality': 'Egypt',
             'Overall': 90,
             'Club': 'Liverpool',
             'Position': 'RW',
             'Value': '€80.5M',
             'Wage': '€240K',
             'Preferred Foot': 'Left',
             'Jersey Number': '11',
             'Height': "5'9",
             'Weight': '157lbs'},
    "14": {'ID': '195864',
             'Name': 'P. Pogba',
             'Age': 26,
             'Nationality': 'France',
             'Overall': 88,
             'Club': 'Manchester United',
             'Position': 'CM',
             'Value': '€72.5M',
             'Wage': '€250K',
             'Preferred Foot': 'Right',
             'Jersey Number': '6',
             'Height': "6'3",
             'Weight': '185lbs'},
    "15": {'ID': '177003',
             'Name': 'L. Modrić',
             'Age': 33,
             'Nationality': 'Croatia',
             'Overall': 90,
             'Club': 'Real Madrid',
             'Position': 'CM',
             'Value': '€45M',
             'Wage': '€340K',
             'Preferred Foot': 'Right',
             'Jersey Number': '10',
             'Height': "5'8",
             'Weight': '146lbs'},
    "16": {'Left': 4318, 'Right': 13960},
    "17": {'Argentina': 886,
             'Portugal': 344,
             'Brazil': 824,
             'Slovenia': 61,
             'Belgium': 268,
             'Germany': 1216,
             'Netherlands': 416,
             'Croatia': 126,
             'Egypt': 30,
             'France': 984,
             'Senegal': 127,
             'England': 1667,
             'Spain': 1035,
             'Italy': 732,
             'Uruguay': 164,
             'Poland': 324,
             'Denmark': 345,
             'Gabon': 16,
             'Korea Republic': 322,
             'Costa Rica': 30,
             'Slovakia': 54,
             'Bosnia Herzegovina': 66,
             'Serbia': 139,
             'Scotland': 277,
             'Hungary': 35,
             'Switzerland': 229,
             'Greece': 96,
             'Austria': 319,
             'Morocco': 94,
             'Sweden': 358,
             'Wales': 117,
             'Colombia': 591,
             'Czech Republic': 102,
             'Chile': 370,
             'Algeria': 50,
             'Ivory Coast': 105,
             'Togo': 13,
             'Norway': 350,
             'Mexico': 340,
             'Iceland': 46,
             'Finland': 72,
             'Jamaica': 29,
             'Albania': 43,
             'Guinea': 35,
             'Cameroon': 78,
             'Ghana': 130,
             'Montenegro': 33,
             'Ukraine': 69,
             'Russia': 81,
             'DR Congo': 54,
             'Central African Rep.': 4,
             'Venezuela': 66,
             'Nigeria': 126,
             'Armenia': 8,
             'Israel': 16,
             'Ecuador': 53,
             'Paraguay': 80,
             'Australia': 196,
             'Turkey': 294,
             'Romania': 287,
             'Japan': 453,
             'Mali': 55,
             'United States': 347,
             'Kosovo': 40,
             'Dominican Republic': 4,
             'Tanzania': 4,
             'China PR': 373,
             'Northern Ireland': 81,
             'Republic of Ireland': 348,
             'Tunisia': 35,
             'Cape Verde': 20,
             'FYR Macedonia': 20,
             'Burkina Faso': 16,
             'Kenya': 7,
             'Angola': 16,
             'South Africa': 72,
             'Peru': 35,
             'Syria': 4,
             'Gambia': 22,
             'New Zealand': 35,
             'Equatorial Guinea': 6,
             'Zimbabwe': 12,
             'Georgia': 25,
             'Canada': 61,
             'Estonia': 6,
             'Benin': 15,
             'Bulgaria': 41,
             'Mozambique': 4,
             'Honduras': 13,
             'Guinea Bissau': 21,
             'Iran': 15,
             'Philippines': 2,
             'Cyprus': 11,
             'Madagascar': 8,
             'Uzbekistan': 3,
             'Moldova': 12,
             'Cuba': 4,
             'Sierra Leone': 10,
             'Curacao': 16,
             'Zambia': 10,
             'Congo': 18,
             'Bolivia': 23,
             'Comoros': 9,
             'Iraq': 5,
             'Chad': 1,
             'Lithuania': 10,
             'Saudi Arabia': 310,
             'Panama': 12,
             'Libya': 4,
             'Bahrain': 1,
             'St Kitts Nevis': 4,
             'New Caledonia': 2,
             'Luxembourg': 9,
             'Trinidad & Tobago': 6,
             'Thailand': 4,
             'United Arab Emirates': 22,
             'Eritrea': 1,
             'Korea DPR': 4,
             'El Salvador': 4,
             'Azerbaijan': 6,
             'Latvia': 6,
             'Montserrat': 3,
             'Puerto Rico': 1,
             'Bermuda': 3,
             'São Tomé & Príncipe': 1,
             'Antigua & Barbuda': 7,
             'Burundi': 4,
             'Kazakhstan': 2,
             'Liberia': 1,
             'Guyana': 4,
             'Haiti': 7,
             'Jordan': 1,
             'Faroe Islands': 5,
             'Mauritania': 5,
             'Namibia': 2,
             'Rwanda': 2,
             'Uganda': 3,
             'Hong Kong': 1,
             'Chinese Taipei': 1,
             'Belize': 1,
             'Palestine': 4,
             'Mauritius': 1,
             'Guam': 1,
             'Suriname': 2,
             'Lebanon': 3,
             'Guatemala': 2,
             'Sudan': 3,
             'Liechtenstein': 2,
             'Grenada': 2,
             'St Lucia': 1,
             'Afghanistan': 2,
             'Ethiopia': 1,
             'Barbados': 1,
             'India': 23,
             'Malta': 2,
             'Niger': 3,
             'Vietnam': 1,
             'Malawi': 1,
             'Gibraltar': 1,
             'Macau': 1,
             'South Sudan': 1,
             'Indonesia': 1},
    "18": {'Argentina': 69.11851015801355,
             'Portugal': 70.51453488372093,
             'Brazil': 71.1614077669903,
             'Slovenia': 68.70491803278688,
             'Belgium': 68.43283582089552,
             'Germany': 65.93914473684211,
             'Netherlands': 68.14903846153847,
             'Croatia': 69.78571428571429,
             'Egypt': 70.1,
             'France': 67.41666666666667,
             'Senegal': 68.64566929133858,
             'England': 63.251949610077986,
             'Spain': 69.9536231884058,
             'Italy': 67.65710382513662,
             'Uruguay': 71.64634146341463,
             'Poland': 63.49074074074074,
             'Denmark': 63.68115942028985,
             'Gabon': 70.6875,
             'Korea Republic': 63.683229813664596,
             'Costa Rica': 68.23333333333333,
             'Slovakia': 69.31481481481481,
             'Bosnia Herzegovina': 68.87878787878788,
             'Serbia': 69.48920863309353,
             'Scotland': 64.75090252707581,
             'Hungary': 69.68571428571428,
             'Switzerland': 64.8471615720524,
             'Greece': 69.39583333333333,
             'Austria': 65.59561128526646,
             'Morocco': 69.69148936170212,
             'Sweden': 63.79050279329609,
             'Wales': 64.6923076923077,
             'Colombia': 65.67851099830796,
             'Czech Republic': 70.31372549019608,
             'Chile': 64.80540540540541,
             'Algeria': 71.38,
             'Ivory Coast': 69.0,
             'Togo': 69.38461538461539,
             'Norway': 63.02857142857143,
             'Mexico': 65.80882352941177,
             'Iceland': 67.28260869565217,
             'Finland': 63.81944444444444,
             'Jamaica': 66.6896551724138,
             'Albania': 66.4186046511628,
             'Guinea': 68.8,
             'Cameroon': 68.33333333333333,
             'Ghana': 66.97692307692307,
             'Montenegro': 66.36363636363636,
             'Ukraine': 69.8695652173913,
             'Russia': 69.33333333333333,
             'DR Congo': 68.4074074074074,
             'Central African Rep.': 70.5,
             'Venezuela': 67.07575757575758,
             'Nigeria': 67.15079365079364,
             'Armenia': 69.375,
             'Israel': 71.125,
             'Ecuador': 70.49056603773585,
             'Paraguay': 69.7875,
             'Australia': 62.58163265306123,
             'Turkey': 66.06802721088435,
             'Romania': 63.70383275261324,
             'Japan': 63.69094922737307,
             'Mali': 67.50909090909092,
             'United States': 64.53025936599424,
             'Kosovo': 66.625,
             'Dominican Republic': 67.5,
             'Tanzania': 63.25,
             'China PR': 59.48525469168901,
             'Northern Ireland': 63.79012345679013,
             'Republic of Ireland': 61.00574712643678,
             'Tunisia': 68.25714285714285,
             'Cape Verde': 70.5,
             'FYR Macedonia': 68.7,
             'Burkina Faso': 66.4375,
             'Kenya': 65.28571428571429,
             'Angola': 69.375,
             'South Africa': 67.72222222222223,
             'Peru': 69.74285714285715,
             'Syria': 70.25,
             'Gambia': 65.31818181818181,
             'New Zealand': 64.17142857142858,
             'Equatorial Guinea': 69.0,
             'Zimbabwe': 67.25,
             'Georgia': 69.04,
             'Canada': 63.91803278688525,
             'Estonia': 66.33333333333333,
             'Benin': 67.66666666666667,
             'Bulgaria': 63.46341463414634,
             'Mozambique': 73.25,
             'Honduras': 68.38461538461539,
             'Guinea Bissau': 67.38095238095238,
             'Iran': 69.0,
             'Philippines': 69.0,
             'Cyprus': 61.72727272727273,
             'Madagascar': 70.25,
             'Uzbekistan': 67.66666666666667,
             'Moldova': 65.0,
             'Cuba': 67.25,
             'Sierra Leone': 63.0,
             'Curacao': 66.0,
             'Zambia': 67.1,
             'Congo': 65.44444444444444,
             'Bolivia': 66.04347826086956,
             'Comoros': 65.22222222222223,
             'Iraq': 67.6,
             'Chad': 73.0,
             'Lithuania': 63.4,
             'Saudi Arabia': 60.92903225806452,
             'Panama': 66.0,
             'Libya': 71.0,
             'Bahrain': 72.0,
             'St Kitts Nevis': 62.75,
             'New Caledonia': 67.5,
             'Luxembourg': 65.66666666666667,
             'Trinidad & Tobago': 65.83333333333333,
             'Thailand': 64.0,
             'United Arab Emirates': 62.86363636363637,
             'Eritrea': 71.0,
             'Korea DPR': 65.75,
             'El Salvador': 67.25,
             'Azerbaijan': 62.833333333333336,
             'Latvia': 61.666666666666664,
             'Montserrat': 66.0,
             'Puerto Rico': 70.0,
             'Bermuda': 63.666666666666664,
             'São Tomé & Príncipe': 70.0,
             'Antigua & Barbuda': 59.42857142857143,
             'Burundi': 63.75,
             'Kazakhstan': 68.0,
             'Liberia': 69.0,
             'Guyana': 63.5,
             'Haiti': 63.285714285714285,
             'Jordan': 68.0,
             'Faroe Islands': 61.4,
             'Mauritania': 65.2,
             'Namibia': 67.0,
             'Rwanda': 64.0,
             'Uganda': 66.0,
             'Hong Kong': 67.0,
             'Chinese Taipei': 66.0,
             'Belize': 66.0,
             'Palestine': 62.0,
             'Mauritius': 66.0,
             'Guam': 66.0,
             'Suriname': 66.0,
             'Lebanon': 64.0,
             'Guatemala': 65.5,
             'Sudan': 62.666666666666664,
             'Liechtenstein': 62.0,
             'Grenada': 60.5,
             'St Lucia': 64.0,
             'Afghanistan': 62.0,
             'Ethiopia': 64.0,
             'Barbados': 64.0,
             'India': 60.0,
             'Malta': 60.0,
             'Niger': 57.0,
             'Vietnam': 62.0,
             'Malawi': 62.0,
             'Gibraltar': 62.0,
             'Macau': 61.0,
             'South Sudan': 59.0,
             'Indonesia': 56.0},
    "19": 'Mozambique',
    "20": 'FC Bayern München',
}

# find a comment something like this: #q10
def extract_question_num(cell):
    for line in cell.get('source', []):
        line = line.strip().replace(' ', '').lower()
        m = re.match(r'\#q(\d+)', line)
        if m:
            return int(m.group(1))
    return None


# rerun notebook and return parsed JSON
def rerun_notebook(orig_notebook):
    new_notebook = 'cs-220-test.ipynb'

    # re-execute it from the beginning
    with open(orig_notebook, encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=nbformat.NO_CONVERT)
    ep = nbconvert.preprocessors.ExecutePreprocessor(timeout=120, kernel_name='python3')
    try:
        out = ep.preprocess(nb, {'metadata': {'path': os.getcwd()}})
    except nbconvert.preprocessors.CellExecutionError:
        out = None
        msg = 'Error executing the notebook "%s".\n\n' % orig_notebook
        msg += 'See notebook "%s" for the traceback.' % new_notebook
        print(msg)
        raise
    finally:
        with open(new_notebook, mode='w', encoding='utf-8') as f:
            nbformat.write(nb, f)

    # Note: Here we are saving and reloading, this isn't needed but can help student's debug

    # parse notebook
    with open(new_notebook, encoding='utf-8') as f:
        nb = json.load(f)
    return nb


def normalize_json(orig):
    try:
        return json.dumps(json.loads(orig.strip("'")), indent=2, sort_keys=True)
    except:
        return 'not JSON'


def check_cell_text(qnum, cell):
    outputs = cell.get('outputs', [])
    if len(outputs) == 0:
        return 'no outputs in an Out[N] cell'
    actual_lines = None
    for out in outputs:
        lines = out.get('data', {}).get('text/plain', [])
        if lines:
            actual_lines = lines
            break
    if actual_lines == None:
        return 'no Out[N] output found for cell (note: printing the output does not work)'
    actual = ''.join(actual_lines)
    actual = ast.literal_eval(actual)
    expected = expected_json[str(qnum)]

    expected_mismatch = False

    if type(expected) != type(actual):
        return "expected an answer of type %s but found one of type %s" % (type(expected), type(actual))
    elif type(expected) == float:
        if not math.isclose(actual, expected, rel_tol=1e-06, abs_tol=1e-06):
            expected_mismatch = True
    elif type(expected) == list:
        extra = set(actual) - set(expected)
        missing = set(expected) - set(actual)
        if extra:
            return "found unexpected entry in list: %s" % repr(list(extra)[0])
        elif missing:
            return "missing %d entries list, such as: %s" % (len(missing), repr(list(missing)[0]))
        elif len(actual) != len(expected):
            return "expected %d entries in the list but found %d" % (len(expected), len(actual))
    else:
        if expected != actual:
            expected_mismatch = True

    if expected_mismatch:
        return "found {} in cell {} but expected {}".format(actual, qnum, expected)

    return PASS


def check_cell(question, cell):
    print('Checking question %d' % question.number)
    if question.format == TEXT_FORMAT:
        return check_cell_text(question.number, cell)

    raise Exception("invalid question type")


def grade_answers(cells):
    results = {'score':0, 'tests': []}

    for question in questions:
        cell = cells.get(question.number, None)
        status = "not found"

        if question.number in cells:
            status = check_cell(question, cells[question.number])

        row = {"test": question.number, "result": status, "weight": question.weight}
        results['tests'].append(row)

    return results


def main():
    # rerun everything
    orig_notebook = 'main.ipynb'
    if len(sys.argv) > 2:
        print("Usage: test.py main.ipynb")
        return
    elif len(sys.argv) == 2:
        orig_notebook = sys.argv[1]
    nb = rerun_notebook(orig_notebook)

    # extract cells that have answers
    answer_cells = {}
    for cell in nb['cells']:
        q = extract_question_num(cell)
        if q == None:
            continue
        if not q in question_nums:
            print('no question %d' % q)
            continue
        answer_cells[q] = cell

    # do grading on extracted answers and produce results.json
    results = grade_answers(answer_cells)
    passing = sum(t['weight'] for t in results['tests'] if t['result'] == PASS)
    total = sum(t['weight'] for t in results['tests'])
    results['score'] = 100.0 * passing / total

    print("\nSummary:")
    for test in results["tests"]:
        print("  Test %d: %s" % (test["test"], test["result"]))

    print('\nTOTAL SCORE: %.2f%%' % results['score'])
    with open('result.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
