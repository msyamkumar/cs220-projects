#!/usr/bin/python

import json
import os
import sys
import re, ast, math
from collections import namedtuple, OrderedDict, defaultdict
from bs4 import BeautifulSoup
from datetime import datetime
import nbconvert
import nbformat

try:
    from lint import lint
except ImportError:
    err_msg = """Please download lint.py and place it in this directory for
    the tests to run correctly. If you haven't yet looked at the linting module,
    it is designed to help you improve your code so take a look at:
    https://github.com/msyamkumar/cs220-projects/tree/master/linter"""
    raise FileNotFoundError(err_msg)

ALLOWED_LINT_ERRS = {
  "E0102": "function-redefined",
  "E0115": "non-local and global",
  "E0601": "used-before-assignment",
  "E0602": "undefined-variable",
  "E1102": "not-callable",
  "E1135": "unsupported-membership-test",
  "W0101": "unreachable",
  "W0104": "pointless-statement",
  "W0105": "pointless-string-statement",
  "W0107": "unnecessary-pass",
  "W0143": "comparison-with-callable",
  "W0301": "unnecessary-semicolon",
  "W0311": "bad-indentation",
  "W0401": "wildcard import",
  "W0404": "reimported",
  "W0611": "unused-import",
  "W0613": "unused-argument",
  "W0622": "redefined-builtin",
  "W0631": "undefined-loop-variable",
  "W0702": "bare-except",
  "W0703": "broad-except",
  "R0204": "redefined-variable-type",
  "R1703": "simplifiable-if-statement",
  "R1711": "useless-return",
  "R1714": "consider-using-in",
  "R1716": "chained-comparison",
}

PASS = 'PASS'
FAIL = 'FAIL'
FAIL_STDERR = 'Program produced an error - please scroll up for more details.'
FAIL_JSON = 'Expected program to print in json format. Make sure the only print statement is a print(json.dumps...)!'
REL_EPSILON = 10**(-3)
ABS_EPSILON = 10**(-6)


TEXT_FORMAT = "text"
PNG_FORMAT = "png"
HTML_FORMAT = "html"
Question = namedtuple("Question", ["number", "weight", "format"])

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
    Question(number=21, weight=1, format=TEXT_FORMAT),
    Question(number=22, weight=1, format=TEXT_FORMAT),
    Question(number=23, weight=1, format=TEXT_FORMAT),
    Question(number=24, weight=1, format=TEXT_FORMAT),
    Question(number=25, weight=1, format=HTML_FORMAT),
    Question(number=26, weight=1, format=PNG_FORMAT),
    Question(number=27, weight=1, format=HTML_FORMAT)
]
question_nums = set([q.number for q in questions])

expected_json = {
    "1": True,
    "2": False,
    "3": [False, True],
    "4": 'netID5678_econ',
    "5": ['John', 'Martha'],
    "6": [2, 3, 4, 1],
    "7": 17.0,
    "8": {'All-Bran with Extra Fiber': 93.704912},
    "9": {'min': 0.0, 'max': 5.0, 'mean': 1.0129870129870129},
    "10": 8.783882783882785,
    "11": 77,
    "12": 'Shredded Wheat spoon size',
    "13": ['Almond Delight',
             'Clusters',
             "Cracklin' Oat Bran",
             'Fruit & Fibre Dates; Walnuts; and Oats',
             'Life',
             'Muesli Raisins; Peaches; & Pecans',
             'Mueslix Crispy Blend',
             'Oatmeal Raisin Crisp',
             'Raisin Nut Bran'],
    "14": ["Shredded Wheat'n'Bran",
             'Shredded Wheat spoon size',
             'Shredded Wheat',
             'Cream of Wheat (Quick)',
             'Puffed Wheat',
             'Nutri-grain Wheat',
             'Frosted Mini-Wheat',
             'Wheat Chex',
             'Crispy Wheat & Raisins'],
    "15": 4213,
    "16": {'name': 'Michael Jordan',
             'year_start': 1985,
             'year_end': 2003,
             'position': 'G-F',
             'height': '6-6',
             'weight': 195,
             'birth_date': 'February 17, 1963',
             'college': 'University of North Carolina'},
    "17": [{'name': 'Cory Blackwell',
              'year_start': 1985,
              'year_end': 1985,
              'position': 'F',
              'height': '6-6',
              'weight': 210,
              'birth_date': 'March 27, 1963',
              'college': 'University of Wisconsin'},
             {'name': 'Paul Cloyd',
              'year_start': 1950,
              'year_end': 1950,
              'position': 'G-F',
              'height': '6-2',
              'weight': 180,
              'birth_date': 'June 13, 1920',
              'college': 'University of Wisconsin'},
             {'name': 'Bobby Cook',
              'year_start': 1950,
              'year_end': 1950,
              'position': 'G-F',
              'height': '5-10',
              'weight': 155,
              'birth_date': 'April 1, 1923',
              'college': 'University of Wisconsin'},
             {'name': 'Sam Dekker',
              'year_start': 2016,
              'year_end': 2018,
              'position': 'F',
              'height': '6-9',
              'weight': 230,
              'birth_date': 'May 6, 1994',
              'college': 'University of Wisconsin'},
             {'name': 'Duje Dukan',
              'year_start': 2016,
              'year_end': 2016,
              'position': 'F',
              'height': '6-9',
              'weight': 220,
              'birth_date': 'December 4, 1991',
              'college': 'University of Wisconsin'},
             {'name': 'Gene Englund',
              'year_start': 1950,
              'year_end': 1950,
              'position': 'F-C',
              'height': '6-5',
              'weight': 205,
              'birth_date': 'October 21, 1917',
              'college': 'University of Wisconsin'},
             {'name': 'Michael Finley',
              'year_start': 1996,
              'year_end': 2010,
              'position': 'G-F',
              'height': '6-7',
              'weight': 215,
              'birth_date': 'March 6, 1973',
              'college': 'University of Wisconsin'},
             {'name': 'Paul Grant',
              'year_start': 1999,
              'year_end': 2004,
              'position': 'C',
              'height': '7-0',
              'weight': 245,
              'birth_date': 'January 6, 1974',
              'college': 'University of Wisconsin'},
             {'name': 'Claude Gregory',
              'year_start': 1986,
              'year_end': 1988,
              'position': 'F',
              'height': '6-8',
              'weight': 205,
              'birth_date': 'December 26, 1958',
              'college': 'University of Wisconsin'},
             {'name': 'Devin Harris',
              'year_start': 2005,
              'year_end': 2018,
              'position': 'G',
              'height': '6-3',
              'weight': 192,
              'birth_date': 'February 27, 1983',
              'college': 'University of Wisconsin'},
             {'name': 'Al Henry',
              'year_start': 1971,
              'year_end': 1972,
              'position': 'C',
              'height': '6-9',
              'weight': 190,
              'birth_date': 'February 9, 1949',
              'college': 'University of Wisconsin'},
             {'name': 'Doug Holcomb',
              'year_start': 1949,
              'year_end': 1949,
              'position': 'F',
              'height': '6-4',
              'weight': 200,
              'birth_date': 'February 9, 1925',
              'college': 'University of Wisconsin'},
             {'name': 'Kim Hughes',
              'year_start': 1976,
              'year_end': 1981,
              'position': 'C',
              'height': '6-11',
              'weight': 220,
              'birth_date': 'June 4, 1952',
              'college': 'University of Wisconsin'},
             {'name': 'Frank Kaminsky',
              'year_start': 2016,
              'year_end': 2018,
              'position': 'F-C',
              'height': '7-0',
              'weight': 242,
              'birth_date': 'April 4, 1993',
              'college': 'University of Wisconsin'},
             {'name': 'Marcus Landry',
              'year_start': 2010,
              'year_end': 2010,
              'position': 'F',
              'height': '6-7',
              'weight': 230,
              'birth_date': 'November 1, 1985',
              'college': 'University of Wisconsin'},
             {'name': 'Walt Lautenbach',
              'year_start': 1950,
              'year_end': 1950,
              'position': 'G-F',
              'height': '6-2',
              'weight': 185,
              'birth_date': 'November 17, 1922',
              'college': 'University of Wisconsin'},
             {'name': 'Jon Leuer',
              'year_start': 2012,
              'year_end': 2018,
              'position': 'F',
              'height': '6-10',
              'weight': 228,
              'birth_date': 'May 14, 1989',
              'college': 'University of Wisconsin'},
             {'name': 'Wes Matthews',
              'year_start': 1981,
              'year_end': 1990,
              'position': 'G',
              'height': '6-1',
              'weight': 170,
              'birth_date': 'August 24, 1959',
              'college': 'University of Wisconsin'},
             {'name': 'Kirk Penney',
              'year_start': 2004,
              'year_end': 2005,
              'position': 'G',
              'height': '6-5',
              'weight': 220,
              'birth_date': 'November 23, 1980',
              'college': 'University of Wisconsin'},
             {'name': 'Don Rehfeldt',
              'year_start': 1951,
              'year_end': 1952,
              'position': 'F',
              'height': '6-7',
              'weight': 210,
              'birth_date': 'January 7, 1927',
              'college': 'University of Wisconsin'},
             {'name': 'Scott Roth',
              'year_start': 1988,
              'year_end': 1990,
              'position': 'F',
              'height': '6-8',
              'weight': 212,
              'birth_date': 'June 3, 1963',
              'college': 'University of Wisconsin'},
             {'name': 'Dick Schulz',
              'year_start': 1947,
              'year_end': 1950,
              'position': 'F-G',
              'height': '6-2',
              'weight': 192,
              'birth_date': 'January 3, 1917',
              'college': 'University of Wisconsin'},
             {'name': 'Glen Selbo',
              'year_start': 1950,
              'year_end': 1950,
              'position': 'G-F',
              'height': '6-3',
              'weight': 196,
              'birth_date': 'March 29, 1926',
              'college': 'University of Wisconsin'},
             {'name': 'Greg Stiemsma',
              'year_start': 2012,
              'year_end': 2015,
              'position': 'C',
              'height': '6-11',
              'weight': 260,
              'birth_date': 'September 26, 1985',
              'college': 'University of Wisconsin'},
             {'name': 'Alando Tucker',
              'year_start': 2008,
              'year_end': 2010,
              'position': 'F',
              'height': '6-6',
              'weight': 205,
              'birth_date': 'February 11, 1984',
              'college': 'University of Wisconsin'}],
    "18": {'F-C': 222.91944444444445,
             'C-F': 228.25615763546799,
             'C': 242.2192118226601,
             'G': 186.82811459027315,
             'F': 217.98585690515807,
             'F-G': 202.60487804878048,
             'G-F': 197.01785714285714},
    "19": ['Norm of the North: King Sized Adventure',
             'Jandino: Whatever it Takes',
             'Transformers Prime'],
    "20": ['Transformers Prime',
             'Transformers: Robots in Disguise',
             'Apaches',
             'Fire Chasers',
             'Castle of Stars',
             'First and Last',
             "Archibald's Next Big Thing",
             'The Spy',
             'No Tomorrow',
             'Frequency'],
    "21": 55,
    "22": 4.333333333333333,
    "23": 3.0,
    "24": 'Windhoek'
}

def parse_df_html_table(html, question=None):
    soup = BeautifulSoup(html, 'html.parser')

    if question == None:
        tables = soup.find_all('table')
        assert(len(tables) == 1)
        table = tables[0]
    else:
        # find a table that looks like this:
        # <table data-question="6"> ...
        table = soup.find('table', {"data-question": str(question)})

    rows = []
    for tr in table.find_all('tr'):
        rows.append([])
        for cell in tr.find_all(['td', 'th']):
            rows[-1].append(cell.get_text())

    cells = {}
    for r in range(1, len(rows)):
        for c in range(1, len(rows[0])):
            rname = rows[r][0]
            cname = rows[0][c]
            cells[(rname,cname)] = rows[r][c]
    return cells

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
    with open(new_notebook,encoding='utf-8') as f:
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
#    actual_lines = outputs[0].get('data', {}).get('text/plain', [])
    actual_lines = None
    for out in outputs:
        lines = out.get('data', {}).get('text/plain', [])
        if lines:
            actual_lines = lines
            break
    if actual_lines == None:
        return 'no Out[N] output found for cell (note: printing the output does not work)'
    actual = ''.join(actual_lines)
    try:
        actual = ast.literal_eval(actual)
    except Exception as e:
        print("COULD NOT PARSE THIS CELL:")
        print(actual)
        raise e
    expected = expected_json[str(qnum)]

    expected_mismatch = False

    if type(expected) != type(actual):
        return FAIL
    elif type(expected) == float:
        if not math.isclose(actual, expected, rel_tol=REL_EPSILON, abs_tol=ABS_EPSILON):
            expected_mismatch = True
    elif type(expected) == dict:
        for key in expected:
            if key not in actual:
                return FAIL
            if type(expected[key]) == float:
                if not math.isclose(actual[key], expected[key], rel_tol=REL_EPSILON, abs_tol=ABS_EPSILON):
                    expected_mismatch = True
            else:
                if actual[key] != expected[key]:
                    expected_mismatch = True
    elif type(expected) == list:
        if len(expected) != len(actual):
            return FAIL
        for i in range(len(expected)):
            if type(expected[i]) == float:
                if not math.isclose(actual[i], expected[i], rel_tol=REL_EPSILON, abs_tol=ABS_EPSILON):
                    expected_mismatch = True
            elif type(expected[i]) == dict:
                for key in expected[i]:
                    if key not in actual[i]:
                        return FAIL
                    if type(expected[i][key]) == float:
                        if not math.isclose(actual[i][key], expected[i][key], rel_tol=REL_EPSILON, abs_tol=ABS_EPSILON):
                            expected_mismatch = True
                    else:
                        if actual[i][key] != expected[i][key]:
                            expected_mismatch = True
            else:
                if actual[i] != expected[i]:
                    expected_mismatch = True
    else:
        if expected != actual:
            expected_mismatch = True

    if expected_mismatch:
        return FAIL

    return PASS


def diff_df_cells(actual_cells, expected_cells):
    actual_keys = set(actual_cells.keys())
    expected_keys = set(expected_cells.keys())
    missing_keys = expected_keys - actual_keys
    extra_keys = actual_keys - expected_keys
    if len(missing_keys) > 1:
        location = list(missing_keys)[0]
        return FAIL
    if len(extra_keys) > 1:
        location = list(extra_keys)[0]
        return "extra values in column {} at index {}".format(location[1], location[0])
    for location, expected in expected_cells.items():
        location_name = "column {} at index {}".format(location[1], location[0])
        actual = actual_cells.get(location, None)
        try:
            actual_float = float(actual)
            expected_float = float(expected)
            if not math.isclose(actual_float, expected_float, rel_tol=REL_EPSILON, abs_tol=ABS_EPSILON):
                return FAIL
        except Exception as e:
            if actual != expected:
                return FAIL
    return PASS

def check_cell_html(qnum, cell):
    outputs = cell.get('outputs', [])
    if len(outputs) == 0:
        return FAIL
    actual_lines = outputs[0].get('data', {}).get('text/html', [])
    try:
        actual_cells = parse_df_html_table(''.join(actual_lines))
    except Exception as e:
        print("ERROR!  Could not find table in notebook")
        raise e

    try:
        with open('expected.html') as f:
            expected_cells = parse_df_html_table(f.read(), qnum)
    except Exception as e:
        print("ERROR!  Could not find table in expected.html")
        raise e

    return diff_df_cells(actual_cells, expected_cells)

def check_cell_png(qnum, cell):
    if qnum == 21:
        print('here')
        print(cell)
    for output in cell.get('outputs', []):
        if qnum == 21:
            print(output.get('data', {}).keys())
        if 'image/png' in output.get('data', {}):
            return PASS
    return FAIL


def check_cell(question, cell):
    print('Checking question %d' % question.number)
    if question.format == TEXT_FORMAT:
        return check_cell_text(question.number, cell)
    elif question.format == PNG_FORMAT:
        return check_cell_png(question.number, cell)
    elif question.format == HTML_FORMAT:
        return check_cell_html(question.number,cell)
    raise Exception("invalid question type")


def grade_answers(cells):
    results = {'score':0, 'tests': [], 'lint': [], "date":datetime.now().strftime("%m/%d/%Y")}

    for question in questions:
        cell = cells.get(question.number, None)
        status = "not found"

        if question.number in cells:
            # does it match the expected output?
            status = check_cell(question, cells[question.number])

        row = {"test": question.number, "result": status, "weight": question.weight}
        results['tests'].append(row)

    return results


def main():
    # rerun everything
    orig_notebook = 'Final_Exam.ipynb'
    if len(sys.argv) > 2:
        print("Usage: test.py Final_Exam.ipynb")
        return
    elif len(sys.argv) == 2:
        orig_notebook = sys.argv[1]

    # make sure directories are properly setup
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

    lint_msgs = lint(orig_notebook, verbose=2, show=False)
    lint_msgs = filter(lambda msg: msg.msg_id in ALLOWED_LINT_ERRS, lint_msgs)
    lint_msgs = list(lint_msgs)
    results["lint"] = [str(l) for l in lint_msgs]

    functionality_score =  passing
    linting_score = min(27., min(1.0, len(lint_msgs)*(0.2)))
    results['score'] = round(max(functionality_score - linting_score, 0.0), 2)

    print("\nSummary:")
    for test in results["tests"]:
        print("  Question %d: %s" % (test["test"], test["result"]))

    if len(lint_msgs) > 0:
        print("\n %d linting errors" % (len(lint_msgs)))

    print('\nTOTAL SCORE: %.2f/14.85' % results['score'])
    with open('result.json', 'w') as f:
        f.write(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
