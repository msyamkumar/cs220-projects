#!/usr/bin/python

import ast
import os
import re
import sys
import json
import math
import collections
from collections import namedtuple, defaultdict
from bs4 import BeautifulSoup
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

PASS = 'TYPE CHECK PASSED'
FAIL_STDERR = 'Program produced an error - please scroll up for more details.'
EPSILON = 0.0001
QNUMS = 27

question_nums = set(range(1, QNUMS + 1))

expected_json = {
    "1": {'type': -1, 'dtype': bool},
    "2": {'type': -1, 'dtype': bool},
    "3": {'type': 3, 'dtype': list, 'len': 2, 'ele_dtype': bool, 'is_sort': False, 'sort_order': False},
    "4": {'type': 0, 'dtype': str},
    "5": {'type': 3, 'dtype': list, 'len': 2, 'ele_dtype': str, 'is_sort': False, 'sort_order': False},
    "6": {'type': 3, 'dtype': list, 'len': 4, 'ele_dtype': int, 'is_sort': False, 'sort_order': False},
    "7": {'type': 2, 'dtype': float},
    "8": {'type': 4.5, 'dtype': dict, 'len': 1, 'key_dtype': str, 'val_dtype': float},
    "9": {'type': 4, 'dtype': dict, 'keys': ['min', 'max', 'mean'], 'ele_dtypes': [float, float, float]},
    "10": {'type': 2, 'dtype': float},
    "11": {'type': 1, 'dtype': int},
    "12": {'type': 0, 'dtype': str},
    "13": {'type': 3, 'dtype': list, 'len': 9, 'ele_dtype': str, 'is_sort': True, 'sort_order': False},
    "14": {'type': 3, 'dtype': list, 'len': 9, 'ele_dtype': str, 'is_sort': False, 'sort_order': False},
    "15": {'type': 1, 'dtype': int},
    "16": {'type': 4, 'dtype': dict, 'keys': ['name', 'year_start', 'year_end', 'position', 'height', 'weight', 'birth_date', 'college'], 'ele_dtypes': [str, int, int, str, str, int, str, str], 'is_sort': False},
    "17": {'type': 5, 'dtype': list, 'len': 25, 'keys': ['name', 'year_start', 'year_end', 'position', 'height', 'weight', 'birth_date', 'college'], 'ele_dtypes': [str, int, int, str, str, int, str, str], 'is_sort': False},
    "18": {'type': 4, 'dtype': dict, 'keys': ['F-C', 'C-F', 'C', 'G', 'F', 'F-G', 'G-F'], 'ele_dtypes': [float, float, float, float, float, float, float], 'is_sort': False, 'sort_order': False},
    "19": {'type': 3, 'dtype': list, 'len': 3, 'ele_dtype': str, 'is_sort': False, 'sort_order': False},
    "20": {'type': 3, 'dtype': list, 'len': 10, 'ele_dtype': str, 'is_sort': False, 'sort_order': False},
    "21": {'type': 1, 'dtype': int},
    "22": {'type': 2, 'dtype': float},
    "23": {'type': 2, 'dtype': float},
    "24": {'type': 0, 'dtype': str},
    "25": {'type': 7, 'rows': 6, 'col_names': ['continent', 'population']},
    "26": {'type': 6},
    "27": {'type': 7, 'rows': 7, 'col_names': ['country', 'population density']},
}

expected_files = {
    "7": ['cereal.csv'],
    "15": ['player_data.csv'],
    "19": ['netflix_titles.html'],
    "22": [os.path.join('data', 'movies.csv'),
            os.path.join('data', 'users', '1.json'),
            os.path.join('data', 'users', '2.json'),
            os.path.join('data', 'users', '3.json'),
            os.path.join('data', 'users', '4.json'),
            os.path.join('data', 'users', '5.json'),
            os.path.join('data', 'users', '6.json'),
            os.path.join('data', 'users', '7.json'),
            os.path.join('data', 'users', '8.json'),
            os.path.join('data', 'users', '10.json')],
    "24": ['countries.db']
}

def parse_df_html_table(html, question=None):
    soup = BeautifulSoup(html, 'html.parser')

    if question == None:
        tables = soup.find_all('table')
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
    try:
        actual = ast.literal_eval(actual)
    except Exception as e:
        print("COULD NOT PARSE THIS CELL:")
        print(actual)
        raise e

    expected = expected_json[str(qnum)]

    if expected['dtype'] != type(actual):
        return "expected an answer of type %s but found one of type %s" % (expected['dtype'].__name__, type(actual).__name__)
    if expected['type'] == 3:
        if expected['len'] != len(actual):
            return "expected a list with %d elements but found a list with %d elements" % (expected['len'], len(actual))
        for ele in actual:
            if expected['ele_dtype'] != type(ele):
                if not (expected['ele_dtype'] == float and type(ele) == int):
                    return "expected a list of %ss but found a %s in list" % (expected['ele_dtype'].__name__, type(ele).__name__)
        if expected['is_sort'] == True:
            if sorted(actual, reverse=expected['sort_order']) != actual:
                return 'expected a sorted list'
    if expected['type'] == 4:
        if len(expected['keys']) != len(actual):
            return "expected a dictionary with %d key/value pairs but found a dictionary with %d key/value pairs" % (len(expected['keys']), len(actual))
        missing_keys = set(expected['keys']) - set(actual.keys())
        if len(missing_keys) > 0:
            return "missing %d keys such as '%s'" % (len(missing_keys), str(list(missing_keys)[0]))
        for i in range(len(expected['keys'])):
            key = expected['keys'][i]
            val = actual[key]
            if type(val) != expected['ele_dtypes'][i]:
                if not (expected['ele_dtypes'][i] == float and type(val) == int):
                    return 'expected a value of type %s for key "%s" but found a value of type %s' % (expected['ele_dtypes'][i].__name__, str(key), type(val).__name__)
    if expected['type'] == 4.5:
        if expected['len'] != len(actual):
            return "expected a dictionary with %d key/value pairs but found a dictionary with %d key/value pairs" % (expected['len'], len(actual))
        for key in actual:
            if expected['key_dtype'] != type(key):
                return "expected a dictionary with %s keys found a %s key in dictionary" % (expected['key_dtype'].__name__, type(key).__name__)
            if expected['val_dtype'] != type(actual[key]):
                return "expected a dictionary with %s values found a %s value in dictionary" % (expected['val_dtype'].__name__, type(actual[key]).__name__)
    if expected['type'] == 5:
        if expected['len'] != len(actual):
            return "expected a list with %d elements but found a list with %d elements" % (expected['len'], len(actual))
        for ele in actual:
            if len(expected['keys']) != len(ele):
                return "expected a list of dictionaries with %d key/value pairs but found dictionaries with %d key/value pairs" % (expected['len'], len(ele))
            missing_keys = set(expected['keys']) - set(ele.keys())
            if len(missing_keys) > 0:
                return "missing %d keys such as %s" % (len(missing_keys), str(list(missing_keys)[0]))
            for i in range(len(expected['keys'])):
                key = expected['keys'][i]
                val = ele[key]
                if type(val) != expected['ele_dtypes'][i]:
                    if not (expected['ele_dtypes'][i] == float and type(val) == int):
                        return 'expected a value of type %s for key "%s" but found a value of type %s' % (expected['ele_dtypes'][i].__name__, str(key), type(val).__name__)
        if expected['is_sort'] == True:
            for i in range(len(actual) - 1):
                first_ele = actual[i][expected['sort_attr']]
                second_ele = actual[i + 1][expected['sort_attr']]
                if expected['sort_order'] == True:
                    if second_ele > first_ele:
                        return 'expected a list of dictionaries sorted by the attribute "%s"' % (expected['sort_attr'])
                if expected['sort_order'] == False:
                    if second_ele < first_ele:
                        return 'expected a list of dictionaries sorted by the attribute "%s"' % (expected['sort_attr'])

    return PASS

def check_cell_png(qnum, cell):
    for output in cell.get('outputs', []):
        if 'image/png' in output.get('data', {}):
            return PASS
    return 'no plot found'

def diff_df_cells(actual_cells, expected_cells):
    rows = []
    columns = []
    for location in actual_cells:
        if location[0] not in rows:
            rows.append(location[0])
        if location[1] not in columns:
            columns.append(location[1])
    if len(columns) != len(expected_cells['col_names']):
        return 'expected %d columns but found %d' % (len(expected_cells['col_names']), len(columns))
    if columns != expected_cells['col_names']:
        missing_cols = list(set(expected_cells['col_names']) - set(columns))
        return 'expected columns such as "%s"' % (missing_cols[0])
    if len(rows) != expected_cells['rows']:
        return 'expected %d rows but found %d' % (expected_cells['rows'], len(rows))
    return PASS

def check_cell_html(qnum, cell):
    outputs = cell.get('outputs', [])
    if len(outputs) == 0:
        return 'no outputs in an Out[N] cell'
    actual_lines = outputs[0].get('data', {}).get('text/html', [])
    try:
        actual_cells = parse_df_html_table(''.join(actual_lines))
    except Exception as e:
        return ("ERROR! Could not find table in notebook")
    expected_cells = expected_json[qnum]

    return diff_df_cells(actual_cells, expected_cells)

def check_files(qnum):
    if qnum in expected_files:
        expected = expected_files[qnum]
        for file in expected:
            if not os.path.exists(file):
                return 'File %s expected, but not found' % (file)
    return PASS

def check_cell(qnum, cell):
    print('Checking question %s' % qnum)
    file_check = check_files(qnum)
    if file_check != PASS:
        return file_check
    if expected_json[qnum]['type'] <= 5:
        return check_cell_text(qnum, cell)
    elif expected_json[qnum]['type'] == 6:
        return check_cell_png(qnum, cell)
    elif expected_json[qnum]['type'] == 7:
        return check_cell_html(qnum, cell)
    raise Exception("invalid question type")


def grade_answers(cells):
    results = []

    for qnum in question_nums:
        cell = cells.get(qnum, None)
        status = "not found"

        if qnum in cells:
            status = check_cell(str(qnum), cells[qnum])

        row = {"test": qnum, "result": status}
        results.append(row)

    return results


def main():
    # rerun everything
    orig_notebook = 'Final_Exam.ipynb'
    if len(sys.argv) > 2:
        print("Usage: test.py Final_Exam.ipynb")
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

    print("\nSummary:")
    for test in results:
        print("  Test %d: %s" % (test["test"], test["result"]))

    # run linter and check only for allowed errors
    lint_msgs = lint(orig_notebook, verbose=2, show=False)
    lint_msgs = filter(lambda msg: msg.msg_id in ALLOWED_LINT_ERRS, lint_msgs)
    lint_msgs = list(lint_msgs)

    if len(lint_msgs) > 0:
        msg_types = defaultdict(list)
        for msg in lint_msgs:
            msg_types[msg.category].append(msg)
        print("\nLinting Summary:")
        for msg_type, msgs in msg_types.items():
            print('  ' + msg_type.title() + ' Messages:')
            for msg in msgs:
                print('    ' + str(msg))
    else:
        print("\nLinting Summary:")
        print('  No linting errors!')


if __name__ == '__main__':
    main()
