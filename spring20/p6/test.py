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
    "1": ['South Africa',
             'Chile',
             'Croatia',
             'Romania',
             'Australia',
             'Morocco',
             'Bulgaria',
             'Moldova',
             'Argentina',
             'Greece',
             'Italy',
             'Slovenia',
             'India',
             'Israel',
             'New Zealand',
             'France',
             'Austria',
             'Canada',
             'Portugal',
             'Hungary',
             'Spain',
             'US',
             'Germany'],
    "2": 39.40787623066104,
    "3": ['Kumeu River', 'Felton Road', 'Spy Valley'],
    "4": ['Rosé',
             'Pinot Noir',
             'Meritage',
             'Cabernet Sauvignon',
             'Lemberger',
             'Nebbiolo',
             'Cabernet Franc',
             'Sangiovese',
             'Zinfandel',
             'Merlot',
             'Aglianico',
             'Blaufränkisch',
             'Bordeaux-style Red Blend'],
    "5": ['Sparkling Blend', 'Chardonnay', 'Pinot Grigio'],
    "6": ['Castelão', 'Red Blend', 'Cabernet Sauvignon', 'Tempranillo', 'Tinta de Toro'],
    "7": ['Cabernet Sauvignon'],
    "8": 123,
    "9": ['Tinta de Toro'],
    "10": ['Gaja'],
    "11": 1.98628003003003,
    "12": 0.2923076923076923,
    "13": ['Grand Pacific'],
    "14": ['Long Neck', 'Essay', 'Robertson Winery', 'KWV'],
    "15": ['Bodega Las Cañitas'],
    "16": ['Cabernet Franc'],
    "17": ['Portuguese White', 'Portuguese Rosé', 'Portuguese Red'],
    "18": 7.6923076923076925,
    "19": 130.0,
    "20": 281.0
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
    with open(orig_notebook) as f:
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
    with open('result.json', 'w') as f:
        f.write(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
