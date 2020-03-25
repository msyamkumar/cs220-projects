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
PNG_FORMAT = "png"

Question = collections.namedtuple("Question", ["number", "weight", "format"])

questions = [
    #stage 1
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
    #stage 2
    Question(number=21, weight=1, format=TEXT_FORMAT),
    Question(number=22, weight=1, format=TEXT_FORMAT),
    Question(number=23, weight=1, format=TEXT_FORMAT),
    Question(number=24, weight=1, format=TEXT_FORMAT),
    Question(number=25, weight=1, format=TEXT_FORMAT),
    Question(number=26, weight=1, format=TEXT_FORMAT),
    Question(number=27, weight=1, format=TEXT_FORMAT),
    Question(number=28, weight=1, format=PNG_FORMAT),
    Question(number=29, weight=1, format=PNG_FORMAT),
    Question(number=30, weight=1, format=PNG_FORMAT),
    Question(number=31, weight=1, format=PNG_FORMAT),
    Question(number=32, weight=1, format=TEXT_FORMAT),
    Question(number=33, weight=1, format=TEXT_FORMAT),
    Question(number=34, weight=1, format=TEXT_FORMAT),
    Question(number=35, weight=1, format=TEXT_FORMAT),
    Question(number=36, weight=1, format=TEXT_FORMAT),
    Question(number=37, weight=1, format=TEXT_FORMAT),
    Question(number=38, weight=1, format=TEXT_FORMAT),
    Question(number=39, weight=1, format=TEXT_FORMAT),
    Question(number=40, weight=1, format=TEXT_FORMAT),
]

question_nums = set([q.number for q in questions])

# JSON and plaintext values
expected_json = {
    "1": {'nm0000131': 'John Cusack',
        'nm0000154': 'Mel Gibson',
        'nm0000163': 'Dustin Hoffman',
        'nm0000418': 'Danny Glover',
        'nm0000432': 'Gene Hackman',
        'nm0000997': 'Gary Busey',
        'nm0001149': 'Richard Donner',
        'nm0001219': 'Gary Fleder',
        'nm0752751': 'Mitchell Ryan',
        'tt0313542': 'Runaway Jury',
        'tt0093409': 'Lethal Weapon'},
    "2": 'Gary Fleder',
    "3": ['John Cusack',
        'Mel Gibson',
        'Dustin Hoffman',
        'Danny Glover',
        'Gene Hackman',
        'Gary Busey',
        'Richard Donner',
        'Gary Fleder',
        'Mitchell Ryan'],
    "4": ['nm0000154', 'nm0000418'],
    "5":[{'title': 'tt0313542',
        'year': 2003,
        'rating': 7.1,
        'directors': ['nm0001219'],
        'actors': ['nm0000131', 'nm0000432', 'nm0000163'],
        'genres': ['Crime', 'Drama', 'Thriller']},
        {'title': 'tt0093409',
        'year': 1987,
        'rating': 7.6,
        'directors': ['nm0001149'],
        'actors': ['nm0000154', 'nm0000418', 'nm0000997', 'nm0752751'],
        'genres': ['Action', 'Crime', 'Thriller']}],
    "6":4,
    "7":'nm0000131',
    "8":'Lethal Weapon',
    "9":['John Cusack', 'Gene Hackman', 'Dustin Hoffman'],
    "10":['Richard Donner'],
    "11": [{'title': 'Fortitude and Glory: Angelo Dundee and His Fighters',
          'year': 2012,
          'rating': 7.2,
          'directors': ['Chris Tasara'],
          'actors': ['Angelo Dundee', 'George Foreman', 'Freddie Roach'],
          'genres': ['Sport']},
         {'title': 'Ivanhoe',
          'year': 1952,
          'rating': 6.8,
          'directors': ['Richard Thorpe'],
          'actors': ['Robert Taylor', 'George Sanders'],
          'genres': ['Adventure', 'Drama', 'History']},
         {'title': 'The Great Gatsby',
          'year': 1949,
          'rating': 6.6,
          'directors': ['Elliott Nugent'],
          'actors': ['Alan Ladd', 'Macdonald Carey'],
          'genres': ['Drama']}],
    "12": [{'title': 'The Big Wedding',
          'year': 2013,
          'rating': 5.6,
          'directors': ['Justin Zackham'],
          'actors': ['Robert De Niro'],
          'genres': ['Comedy', 'Drama', 'Romance']},
         {'title': 'The Affair of the Necklace',
          'year': 2001,
          'rating': 6.1,
          'directors': ['Charles Shyer'],
          'actors': ['Simon Baker', 'Jonathan Pryce', 'Adrien Brody'],
          'genres': ['Drama', 'History', 'Romance']}],
    "13": [{'title': 'Redskin',
          'year': 1929,
          'rating': 7.0,
          'directors': ['Victor Schertzinger'],
          'actors': ['Richard Dix', 'Tully Marshall', 'George Regas'],
          'genres': ['Adventure', 'Drama', 'Western']},
         {'title': 'The Girl in the Show',
          'year': 1929,
          'rating': 6.5,
          'directors': ['Edgar Selwyn'],
          'actors': ['Raymond Hackett', 'Edward J. Nugent'],
          'genres': ['Comedy']},
         {'title': 'Atlantic',
          'year': 1929,
          'rating': 5.5,
          'directors': ['Ewald André Dupont'],
          'actors': ['Franklin Dyall', 'John Stuart'],
          'genres': ['Drama']}],
    "14": [{'title': 'Arizona',
          'year': 1931,
          'rating': 6.0,
          'directors': ['George B. Seitz'],
          'actors': ['John Wayne', 'Forrest Stanley'],
          'genres': ['Drama', 'Romance']},
         {'title': 'City Lights',
          'year': 1931,
          'rating': 8.5,
          'directors': ['Charles Chaplin'],
          'actors': ['Charles Chaplin', 'Harry Myers'],
          'genres': ['Comedy', 'Drama', 'Romance']},
         {'title': 'The Range Feud',
          'year': 1931,
          'rating': 5.8,
          'directors': ['D. Ross Lederman'],
          'actors': ['Buck Jones', 'John Wayne', 'Edward LeSaint'],
          'genres': ['Mystery', 'Western']}],
    "15": 2605,
    "16": 18,
    "17": 'Zorba the Greek',
    "18": 6.401659528907912,
    "19": 'The Godfather',
    "20": 'Shoulder Arms',
    "21": {'short': [{'title': 'A', 'year': 2018, 'style': 'short', 'genres': ['g1']},
          {'title': 'C', 'year': 2019, 'style': 'short', 'genres': ['g3']}],
         'long': [{'title': 'B', 'year': 2018, 'style': 'long', 'genres': ['g2']},
          {'title': 'D', 'year': 2019, 'style': 'long', 'genres': ['g1', 'g2', 'g3']}]},
    "22": {2018: [{'title': 'A', 'year': 2018, 'style': 'short', 'genres': ['g1']},
          {'title': 'B', 'year': 2018, 'style': 'long', 'genres': ['g2']}],
         2019: [{'title': 'C', 'year': 2019, 'style': 'short', 'genres': ['g3']},
          {'title': 'D', 'year': 2019, 'style': 'long', 'genres': ['g1', 'g2', 'g3']}]},
    "23": {'g1': [{'title': 'A', 'year': 2018, 'style': 'short', 'genres': ['g1']},
          {'title': 'D', 'year': 2019, 'style': 'long', 'genres': ['g1', 'g2', 'g3']}],
         'g2': [{'title': 'B', 'year': 2018, 'style': 'long', 'genres': ['g2']},
          {'title': 'D', 'year': 2019, 'style': 'long', 'genres': ['g1', 'g2', 'g3']}],
         'g3': [{'title': 'C', 'year': 2019, 'style': 'short', 'genres': ['g3']},
          {'title': 'D', 'year': 2019, 'style': 'long', 'genres': ['g1', 'g2', 'g3']}]},
    "24": {'Crime': [{'title': 'Runaway Jury',
           'year': 2003,
           'rating': 7.1,
           'directors': ['Gary Fleder'],
           'actors': ['John Cusack', 'Gene Hackman', 'Dustin Hoffman'],
           'genres': ['Crime', 'Drama', 'Thriller']},
          {'title': 'Lethal Weapon',
           'year': 1987,
           'rating': 7.6,
           'directors': ['Richard Donner'],
           'actors': ['Mel Gibson', 'Danny Glover', 'Gary Busey', 'Mitchell Ryan'],
           'genres': ['Action', 'Crime', 'Thriller']}],
         'Drama': [{'title': 'Runaway Jury',
           'year': 2003,
           'rating': 7.1,
           'directors': ['Gary Fleder'],
           'actors': ['John Cusack', 'Gene Hackman', 'Dustin Hoffman'],
           'genres': ['Crime', 'Drama', 'Thriller']}],
         'Thriller': [{'title': 'Runaway Jury',
           'year': 2003,
           'rating': 7.1,
           'directors': ['Gary Fleder'],
           'actors': ['John Cusack', 'Gene Hackman', 'Dustin Hoffman'],
           'genres': ['Crime', 'Drama', 'Thriller']},
          {'title': 'Lethal Weapon',
           'year': 1987,
           'rating': 7.6,
           'directors': ['Richard Donner'],
           'actors': ['Mel Gibson', 'Danny Glover', 'Gary Busey', 'Mitchell Ryan'],
           'genres': ['Action', 'Crime', 'Thriller']}],
         'Action': [{'title': 'Lethal Weapon',
           'year': 1987,
           'rating': 7.6,
           'directors': ['Richard Donner'],
           'actors': ['Mel Gibson', 'Danny Glover', 'Gary Busey', 'Mitchell Ryan'],
           'genres': ['Action', 'Crime', 'Thriller']}]},
    "25": 2,
    "26": 1247,
    "27": {'Comedy': 485,
            'Drama': 1094,
            'Romance': 352,
            'History': 73,
            'Family': 85,
            'Mystery': 121,
            'Thriller': 250,
            'Action': 299,
            'Crime': 357,
            'Adventure': 283,
            'Western': 226,
            'Music': 38,
            'Animation': 45,
            'Sport': 48,
            'Fantasy': 59,
            'War': 99,
            'Sci-Fi': 69,
            'Horror': 85},
    "32": {'Robert De Niro': 49,
            'Kurt Russell': 50,
            'John Wayne': 46,
            'Mickey Rooney': 75,
            'Robert Mitchum': 51,
            'Henry Fonda': 46,
            'Glenn Ford': 52,
            'Jeff Bridges': 48,
            'James Caan': 52,
            'Anthony Quinn': 61,
            'Marlon Brando': 49,
            'Tony Curtis': 45,
            'Ernest Borgnine': 47,
            'Rod Steiger': 45,
            'George Burns': 60,
            'Bruce Dern': 45,
            'Dean Stockwell': 53},
    "33": {'Howard Hawks': 42,
             'Charles Chaplin': 34,
             'J. Lee Thompson': 28,
             'Henry Hathaway': 36,
             'John Ford': 25,
             'Stanley Kubrick': 46,
             'Taylor Hackford': 32,
             'Cecil B. DeMille': 30,
             'Lee H. Katzin': 30,
             'John Sturges': 25,
             'Richard Fleischer': 32,
             'Don Siegel': 27,
             'Sidney Lumet': 33,
             'George Sherman': 33,
             'John Huston': 30,
             'Burt Kennedy': 25,
             'William A. Graham': 25,
             'Richard Thorpe': 29,
             'Robert Siodmak': 30,
             'Eldar Ryazanov': 31,
             'Martin Ritt': 32},
    "34": [{'name': 'Mickey Rooney', 'span': 75},
            {'name': 'Anthony Quinn', 'span': 61},
            {'name': 'George Burns', 'span': 60},
            {'name': 'Dean Stockwell', 'span': 53},
            {'name': 'Glenn Ford', 'span': 52},
            {'name': 'James Caan', 'span': 52},
            {'name': 'Robert Mitchum', 'span': 51},
            {'name': 'Kurt Russell', 'span': 50},
            {'name': 'Robert De Niro', 'span': 49},
            {'name': 'Marlon Brando', 'span': 49}],
    "35": [{'name': 'Stanley Kubrick', 'span': 46},
            {'name': 'Howard Hawks', 'span': 42},
            {'name': 'Henry Hathaway', 'span': 36},
            {'name': 'Charles Chaplin', 'span': 34},
            {'name': 'Sidney Lumet', 'span': 33},
            {'name': 'George Sherman', 'span': 33},
            {'name': 'Taylor Hackford', 'span': 32},
            {'name': 'Richard Fleischer', 'span': 32},
            {'name': 'Martin Ritt', 'span': 32},
            {'name': 'Eldar Ryazanov', 'span': 31},
            {'name': 'Cecil B. DeMille', 'span': 30},
            {'name': 'Lee H. Katzin', 'span': 30},
            {'name': 'John Huston', 'span': 30},
            {'name': 'Robert Siodmak', 'span': 30},
            {'name': 'Richard Thorpe', 'span': 29},
            {'name': 'J. Lee Thompson', 'span': 28},
            {'name': 'Don Siegel', 'span': 27},
            {'name': 'John Ford', 'span': 25},
            {'name': 'John Sturges', 'span': 25},
            {'name': 'Burt Kennedy', 'span': 25},
            {'name': 'William A. Graham', 'span': 25}],
    "36": [{'name': 'Heath Ledger', 'rating': 9.0, 'count': 1},
            {'name': 'John Fiedler', 'rating': 8.9, 'count': 1},
            {'name': 'Aldo Giuffrè', 'rating': 8.9, 'count': 1},
            {'name': 'Steven Williams', 'rating': 8.8, 'count': 1},
            {'name': 'Daniel Roebuck', 'rating': 8.8, 'count': 1},
            {'name': 'Joseph Gordon-Levitt', 'rating': 8.8, 'count': 1},
            {'name': 'Miyu Irino', 'rating': 8.6, 'count': 1},
            {'name': 'Andrew Kevin Walker', 'rating': 8.6, 'count': 1},
            {'name': 'Ken Watanabe', 'rating': 8.55, 'count': 2}],
    "37": [{'name': 'James Marlowe', 'rating': 8.8, 'count': 1},
            {'name': 'Kirk Wise', 'rating': 8.6, 'count': 1},
            {'name': 'David Fincher', 'rating': 8.6, 'count': 1},
            {'name': 'Christopher Nolan', 'rating': 8.5, 'count': 9},
            {'name': 'Leonid Gayday', 'rating': 8.4, 'count': 5},
            {'name': 'Adrian Molina', 'rating': 8.4, 'count': 1},
            {'name': 'Stanley Kubrick', 'rating': 8.3, 'count': 11},
            {'name': 'Sergio Leone', 'rating': 8.3, 'count': 7},
            {'name': 'Satyajit Ray', 'rating': 8.2, 'count': 9},
            {'name': 'Moustapha Akkad', 'rating': 8.2, 'count': 1},
            {'name': 'Andrew Grieve', 'rating': 8.2, 'count': 6},
            {'name': 'Danny Boyle', 'rating': 8.2, 'count': 1}],
    "38": [{'name': 'Henry Bergman', 'rating': 8.2, 'count': 5},
            {'name': 'Ioan Gruffudd', 'rating': 8.2, 'count': 6},
            {'name': 'Robert Lindsay', 'rating': 8.2, 'count': 6},
            {'name': 'Charles Chaplin', 'rating': 8.15, 'count': 10},
            {'name': 'Bradley Cooper', 'rating': 7.3, 'count': 5},
            {'name': 'Joe Pesci', 'rating': 7.2, 'count': 7},
            {'name': 'Robin Williams', 'rating': 7.2, 'count': 5},
            {'name': 'Kirk Douglas', 'rating': 7.15, 'count': 12},
            {'name': 'Ward Bond', 'rating': 7.1, 'count': 10},
            {'name': 'Gregory Peck', 'rating': 7.1, 'count': 5},
            {'name': 'Tom Hanks', 'rating': 7.1, 'count': 6},
            {'name': 'Al Pacino', 'rating': 7.05, 'count': 8},
            {'name': 'Ben Johnson', 'rating': 7.05, 'count': 6},
            {'name': 'Charles Coburn', 'rating': 7.0, 'count': 9}],
    "39": [{'name': 'Henry Fonda', 'rating': 6.9, 'count': 77},
            {'name': 'Mickey Rooney', 'rating': 6.7, 'count': 82},
            {'name': 'Anthony Quinn', 'rating': 6.7, 'count': 79},
            {'name': 'Brian Donlevy', 'rating': 6.7, 'count': 47},
            {'name': 'Robert Mitchum', 'rating': 6.65, 'count': 74},
            {'name': 'Glenn Ford', 'rating': 6.6, 'count': 74},
            {'name': 'George Sanders', 'rating': 6.6, 'count': 74},
            {'name': 'Robert De Niro', 'rating': 6.55, 'count': 74},
            {'name': 'Randolph Scott', 'rating': 6.5, 'count': 76},
            {'name': 'Jeff Bridges', 'rating': 6.5, 'count': 59},
            {'name': 'Ned Beatty', 'rating': 6.45, 'count': 50},
            {'name': 'Kurt Russell', 'rating': 6.4, 'count': 46},
            {'name': 'John Wayne', 'rating': 6.4, 'count': 130},
            {'name': 'John Cusack', 'rating': 6.4, 'count': 52},
            {'name': 'Danny Glover', 'rating': 6.4, 'count': 51},
            {'name': 'Dennis Quaid', 'rating': 6.35, 'count': 60}],
    "40": [{'name': 'Christopher Nolan', 'rating': 8.5, 'count': 9},
            {'name': 'Stanley Kubrick', 'rating': 8.3, 'count': 11},
            {'name': 'Satyajit Ray', 'rating': 8.2, 'count': 9},
            {'name': 'Charles Chaplin', 'rating': 8.1, 'count': 11},
            {'name': 'Hayao Miyazaki', 'rating': 8.1, 'count': 9},
            {'name': 'Martin Scorsese', 'rating': 8.0, 'count': 8},
            {'name': 'John Ford', 'rating': 7.3, 'count': 21},
            {'name': 'Fritz Lang', 'rating': 7.2, 'count': 9}],
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

    # TODO: remove this hack!!!
    if qnum in [34, 35]:
        # check they did some reasonable sorting
        for i in range(1, len(actual)):
            try:
                a = actual[i-1]["span"]
                b = actual[i]["span"]
                if a < b:
                    return "bad sort: found a span of {} before a span of {}".format(a, b)
            except KeyError:
                return "expected {}".format(expected)

    # TODO: remove this hack!!!
    if qnum in [36, 37, 38, 39, 40]:
        # check they did some reasonable sorting
        for i in range(1, len(actual)):
            try:
                a = actual[i-1]["rating"]
                b = actual[i]["rating"]
                if a < b:
                    return "bad sort: found a rating of {} before a rating of {}".format(a, b)
            except KeyError:
                return "expected {}".format(expected)

    if type(expected) != type(actual):
        return "expected an answer of type %s but found one of type %s" % (type(expected), type(actual))
    elif type(expected) == float:
        if not math.isclose(actual, expected, rel_tol=1e-06, abs_tol=1e-06):
            expected_mismatch = True
    elif type(expected) == list:
        try:
            extra = set(actual) - set(expected)
            missing = set(expected) - set(actual)
            if extra:
                return "found unexpected entry in list: %s" % repr(list(extra)[0])
            elif missing:
                return "missing %d entries list, such as: %s" % (len(missing), repr(list(missing)[0]))
            elif len(actual) != len(expected):
                return "expected %d entries in the list but found %d" % (len(expected), len(actual))
        except TypeError:
            # this happens when the list contains dicts.
            if actual != expected:
                # TODO: remove this hack!!!
                if qnum in [5, 11, 12, 13, 14, 34, 35, 36, 37, 38, 39, 40]:
                    if len(actual) != len(expected):
                        return "expected %d entries in the list but found %d" % (len(expected), len(actual))
                    try:
                        # check the numbers are reasonably close.
                        for i in range(0, len(expected)):
                            found = False
                            for j in range(0, len(actual)):
                                if actual[j]['name'] == expected[i]['name']:
                                    found = True
                                    for key in expected[i]:
                                        val = expected[i][key]
                                        if type(val) == float:
                                            if not math.isclose(actual[j][key], val, rel_tol=1e-06, abs_tol=1e-06):
                                                return "found {} in cell {} but expected {}".format(actual[j], qnum, expected[i])
                                        else:
                                            if not actual[j][key] == val:
                                                return "found {} in cell {} but expected {}".format(actual[j], qnum, expected[i])
                            if not found:
                                return "missing entries such as {}".format(expected[i])
                    except KeyError:
                        # this happpens if answer is not in the correct format
                        return "expected {}".format(expected)

    else:
        if expected != actual:
            expected_mismatch = True

    if expected_mismatch:
        return "found {} in cell {} but expected {}".format(actual, qnum, expected)

    return PASS

def check_cell_png(qnum, cell):
    for output in cell.get('outputs', []):
        if 'image/png' in output.get('data', {}):
            return PASS
    return 'no plot found'


def check_cell(question, cell):
    print('Checking question %d' % question.number)
    if question.format == TEXT_FORMAT:
        return check_cell_text(question.number, cell)
    elif question.format == PNG_FORMAT:
        return check_cell_png(question.number, cell)
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
