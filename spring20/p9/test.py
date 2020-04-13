#!/usr/bin/python

import ast
import os
import re
import sys
import json
import math
import collections
from collections import namedtuple

import nbconvert
import nbformat

PASS = 'PASS'
FAIL_STDERR = 'Program produced an error - please scroll up for more details.'
FAIL_JSON = 'Expected program to print in json format. Make sure the only print statement is a print(json.dumps...)!'
EPSILON = 0.0001

obfuscate1 = "Review"
obfuscate2 = ["id", "username", "asin", "title", "text", "rating", "do_recommend", "num_helpful", "date"]
TEXT_FORMAT = "text"
PNG_FORMAT = "png"
Question = namedtuple("Question", ["number", "weight", "format"])
Review = namedtuple(obfuscate1, obfuscate2)

questions = [
    # stage 1
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
    # stage 2
    Question(number=16, weight=1, format=TEXT_FORMAT),
    Question(number=17, weight=1, format=TEXT_FORMAT),
    Question(number=18, weight=1, format=PNG_FORMAT),
    Question(number=19, weight=1, format=PNG_FORMAT),
    Question(number=20, weight=1, format=TEXT_FORMAT),
    Question(number=21, weight=1, format=PNG_FORMAT),
    Question(number=22, weight=1, format=PNG_FORMAT),
    Question(number=23, weight=1, format=PNG_FORMAT),
    Question(number=24, weight=1, format=PNG_FORMAT),
    Question(number=25, weight=1, format=TEXT_FORMAT),
    Question(number=26, weight=1, format=TEXT_FORMAT),
    Question(number=27, weight=1, format=TEXT_FORMAT),
    Question(number=28, weight=1, format=TEXT_FORMAT),
    Question(number=29, weight=1, format=TEXT_FORMAT),
    Question(number=30, weight=1, format=TEXT_FORMAT),
]
question_nums = set([q.number for q in questions])

expected_json = {
    "1": sorted(os.listdir("data"), reverse = True),
    "2": sorted([os.path.join('data','sample_reviews.csv'),
            os.path.join('data','sample_reviews.json'),
            os.path.join('data','review5.csv'),
            os.path.join('data','review5.json'),
            os.path.join('data','review4.csv'),
            os.path.join('data','review4.json'),
            os.path.join('data','review3.csv'),
            os.path.join('data','review3.json'),
            os.path.join('data','review2.csv'),
            os.path.join('data','review2.json'),
            os.path.join('data','review1.csv'),
            os.path.join('data','review1.json'),
            os.path.join('data','products.json')], reverse=True),
    "3": sorted([os.path.join('data','review1.json'),
             os.path.join('data','review2.json'),
             os.path.join('data','review3.json'),
             os.path.join('data','review4.json'),
             os.path.join('data','review5.json'),
             os.path.join('data','sample_reviews.json'),
            os.path.join('data','products.json')], reverse=True),
    "4": sorted([os.path.join('data','review1.csv'),
             os.path.join('data','review1.json'),
             os.path.join('data','review2.csv'),
             os.path.join('data','review2.json'),
             os.path.join('data','review3.csv'),
             os.path.join('data','review3.json'),
             os.path.join('data','review4.csv'),
             os.path.join('data','review4.json'),
             os.path.join('data','review5.csv'),
             os.path.join('data','review5.json')], reverse=True),
    "5": {'B00QFQRELG': 'Amazon 9W PowerFast Official OEM USB Charger and Power Adapter for Fire Tablets and Kindle eReaders',
            'B00ZV9PXP2': 'All-New Kindle E-reader - Black, 6" Glare-Free Touchscreen Display, Wi-Fi - Includes Special Offers',
            'B01BH83OOM': 'Amazon Tap Smart Assistant Alexa enabled (black) Brand New',
            'B0751RGYJV': 'Amazon Echo (2nd Generation) Smart Assistant Oak Finish Priority Shipping',
            'B00IOY8XWQ': 'Kindle Voyage E-reader, 6 High-Resolution Display (300 ppi) with Adaptive Built-in Light, PagePress Sensors, Wi-Fi - Includes Special Offers',
            'B0752151W6': 'All-new Echo (2nd Generation) with improved sound, powered by Dolby, and a new design Walnut Finish',
            'B018Y226XO': 'Fire Kids Edition Tablet, 7 Display, Wi-Fi, 16 GB, Pink Kid-Proof Case',
            'B01ACEKAJY': 'All-New Fire HD 8 Tablet, 8 HD Display, Wi-Fi, 32 GB - Includes Special Offers, Black',
            'B01AHB9CYG': 'All-New Fire HD 8 Tablet, 8 HD Display, Wi-Fi, 32 GB - Includes Special Offers, Magenta',
            'B01AHB9CN2': 'All-New Fire HD 8 Tablet, 8 HD Display, Wi-Fi, 16 GB - Includes Special Offers, Magenta',
            'B00VINDBJK': 'Kindle Oasis E-reader with Leather Charging Cover - Merlot, 6 High-Resolution Display (300 ppi), Wi-Fi - Includes Special Offers',
            'B01AHB9C1E': 'Fire HD 8 Tablet with Alexa, 8 HD Display, 32 GB, Tangerine - with Special Offers',
            'B018Y229OU': 'Fire Tablet, 7 Display, Wi-Fi, 8 GB - Includes Special Offers, Magenta'},
    "6": 'I would recommend this product. It works great and ver compact.',
    "7": 'Loveeeeeeeee........................................',
    "8": 'review2.csv',
    "9": {'46663': ['Dmh1589', 'B018Y229OU'],
             '36363': ['Shoot2thril', 'B018Y229OU'],
             '15763': ['Barbara', 'B018Y229OU'],
             '5463': ['Elec8', 'B018Y229OU'],
             '54066': ['Silvrblur', 'B018Y229OU'],
             '33466': ['Trish', 'B018Y229OU'],
             '40869': ['airbear', 'B018Y229OU'],
             '30569': ['lorphe', 'B018Y229OU'],
             '89472': ['felix', 'B018Y229OU'],
             '48272': ['Bull99', 'B018Y229OU']},
    "10": [Review(id=46663, username='Dmh1589', asin='B018Y229OU', title='Nice for kids', text='Easy to use. Memory fills up fast though. Battery life is decent.', rating=4, do_recommend=True, num_helpful=0, date='2016-12-23'),
             Review(id=36363, username='Shoot2thril', asin='B018Y229OU', title='Great tablet', text='Great tablet for the price. I already have 3 followers including the hd.', rating=5, do_recommend=True, num_helpful=0, date='2016-12-23'),
             Review(id=15763, username='Barbara', asin='B018Y229OU', title='Great tablet', text='Excellent tablet. Love the size. Fits perfectly in my purse. I would recommend this tablet.', rating=5, do_recommend=True, num_helpful=0, date='2016-12-23'),
             Review(id=5463, username='Elec8', asin='B018Y229OU', title='Great budget tablet', text='Great tablet for kids. Good for Netflix and YouTube.', rating=5, do_recommend=True, num_helpful=0, date='2016-12-23'),
             Review(id=54066, username='Silvrblur', asin='B018Y229OU', title='Great tablet for the price.', text='I bought this tablet for my 9 year old nephew and he loves it. It is easy to setup and very user friendly. Picked up a case for protection.Buy far the best bang for your buck for an entry level tablet.', rating=5, do_recommend=True, num_helpful=0, date='2016-12-23'),
             Review(id=33466, username='Trish', asin='B018Y229OU', title='Love it', text='My sister in law is in love with this. Best gift ever for her', rating=5, do_recommend=True, num_helpful=0, date='2016-12-23'),
             Review(id=40869, username='airbear', asin='B018Y229OU', title='Love it', text='Love it so much. So easy to use even for my little kids.', rating=5, do_recommend=True, num_helpful=0, date='2016-12-23'),
             Review(id=30569, username='lorphe', asin='B018Y229OU', title='Stand Amazon Tablet', text='Works well for the money. Got it from Black Friday deal. User friendly', rating=4, do_recommend=True, num_helpful=0, date='2016-12-23'),
             Review(id=89472, username='felix', asin='B018Y229OU', title='great ipad', text='i brought this for my kids and no regret. Make sure you buy a case protector along with it.', rating=5, do_recommend=True, num_helpful=0, date='2016-12-23'),
             Review(id=48272, username='Bull99', asin='B018Y229OU', title='Works great', text='This tablet is so compact and fit in my purse. It works very well.', rating=5, do_recommend=True, num_helpful=0, date='2016-12-23')],
    "11": [Review(id=46663, username='Dmh1589', asin='B018Y229OU', title='Nice for kids', text='Easy to use. Memory fills up fast though. Battery life is decent.', rating=4, do_recommend=True, num_helpful=0, date='2016-12-23'),
             Review(id=36363, username='Shoot2thril', asin='B018Y229OU', title='Great tablet', text='Great tablet for the price. I already have 3 followers including the hd.', rating=5, do_recommend=True, num_helpful=0, date='2016-12-23'),
             Review(id=15763, username='Barbara', asin='B018Y229OU', title='Great tablet', text='Excellent tablet. Love the size. Fits perfectly in my purse. I would recommend this tablet.', rating=5, do_recommend=True, num_helpful=0, date='2016-12-23'),
             Review(id=5463, username='Elec8', asin='B018Y229OU', title='Great budget tablet', text='Great tablet for kids. Good for Netflix and YouTube.', rating=5, do_recommend=True, num_helpful=0, date='2016-12-23'),
             Review(id=54066, username='Silvrblur', asin='B018Y229OU', title='Great tablet for the price.', text='I bought this tablet for my 9 year old nephew and he loves it. It is easy to setup and very user friendly. Picked up a case for protection.Buy far the best bang for your buck for an entry level tablet.', rating=5, do_recommend=True, num_helpful=0, date='2016-12-23'),
             Review(id=33466, username='Trish', asin='B018Y229OU', title='Love it', text='My sister in law is in love with this. Best gift ever for her', rating=5, do_recommend=True, num_helpful=0, date='2016-12-23'),
             Review(id=40869, username='airbear', asin='B018Y229OU', title='Love it', text='Love it so much. So easy to use even for my little kids.', rating=5, do_recommend=True, num_helpful=0, date='2016-12-23'),
             Review(id=30569, username='lorphe', asin='B018Y229OU', title='Stand Amazon Tablet', text='Works well for the money. Got it from Black Friday deal. User friendly', rating=4, do_recommend=True, num_helpful=0, date='2016-12-23'),
             Review(id=89472, username='felix', asin='B018Y229OU', title='great ipad', text='i brought this for my kids and no regret. Make sure you buy a case protector along with it.', rating=5, do_recommend=True, num_helpful=0, date='2016-12-23'),
             Review(id=48272, username='Bull99', asin='B018Y229OU', title='Works great', text='This tablet is so compact and fit in my purse. It works very well.', rating=5, do_recommend=True, num_helpful=0, date='2016-12-23')],
    "12": [Review(id=25136, username='Angrydagg', asin='B018Y229OU', title='Nice features for the price.', text='For the price this tables does everything I need. so far.', rating=4, do_recommend=True, num_helpful=0, date='2015-12-30'),
             Review(id=84039, username='Appman2015', asin='B018Y229OU', title='Great for xmas', text='So far I have bought three of these of tablets and they love it', rating=4, do_recommend=True, num_helpful=1, date='2015-12-30'),
             Review(id=22239, username='SuzieQ', asin='B018Y229OU', title='great for pre teens', text='i am glad i got them for my grand children they r enjoying them', rating=5, do_recommend=True, num_helpful=0, date='2015-12-31'),
             Review(id=70842, username='Gracie', asin='B018Y229OU', title='Great kindle', text='Purchase was good. Very easy to set up and use. Clear screen. Easy to charge. Would like more storage.', rating=5, do_recommend=True, num_helpful=0, date='2015-12-31'),
             Review(id=60542, username='Jeremyjeepster', asin='B018Y229OU', title='Good entry level tablet reader.', text='His is a very economical entry level tablet. Great for kids or for first time users.', rating=4, do_recommend=True, num_helpful=0, date='2015-12-31'),
             Review(id=9042, username='kinglowe78', asin='B018Y229OU', title='Good Deal', text='Real good deal. Nice present for those who want a tablet', rating=4, do_recommend=True, num_helpful=1, date='2016-01-01'),
             Review(id=98845, username='jamal', asin='B018Y229OU', title='good basic', text='Good gift for basic Internet use browsing emails .', rating=3, do_recommend=True, num_helpful=1, date='2016-01-01'),
             Review(id=88545, username='Abc1', asin='B018Y229OU', title='Lots of apps to play with', text='This is a good beginning tablet. Works well and has lots of preloaded apps to start you off.', rating=4, do_recommend=True, num_helpful=2, date='2016-01-01'),
             Review(id=47345, username='4Thrifty', asin='B018Y229OU', title='Great tablet', text='Well priced. Easy to operate. Fast and efficient. Great product.', rating=4, do_recommend=False, num_helpful=0, date='2016-01-02'),
             Review(id=54748, username='Sandycat19', asin='B018Y229OU', title='Good product fair price', text='Good for little ones who are just getting started on apps.', rating=5, do_recommend=True, num_helpful=0, date='2016-01-02')],
    "13": Review(id=25401, username='Brody16', asin='B018Y229OU', title='Wonderful for our grandsons', text='Love the ease of using them for our grandsons and they enjoyed them for Christmas', rating=1, do_recommend=True, num_helpful=0, date='2017-01-06'),
    "14": Review(id=78626, username='Mijenx', asin='B01AHB9CN2', title='Ended up returning', text='I bought this tablet for my 4 year old daughter. Too many advertisements. I would rather pay more and not have a single ad.', rating=1, do_recommend=False, num_helpful=2, date='2016-11-25'),
    "15": [Review(id=29325, username='zerofighterblue', asin='B018Y229OU', title='cant live without', text='have a kindle with a broken screen. bought originally for 99.00. now regular price is 49.99 and were on sale black Friday for 34.99. got 2 more.', rating=5, do_recommend=True, num_helpful=1, date='2015-12-10'),
             Review(id=96947, username='zedog83', asin='B01AHB9CN2', title='Great for kids', text='Bought this for our 6 year old daughter and she uses it daily. She enjoys watching movies on it and playing learning games. So far it has been very durable and battery life has been great.', rating=5, do_recommend=True, num_helpful=0, date='2017-01-18'),
             Review(id=77499, username='zcraig7', asin='B018Y229OU', title='Awesome picture quality', text='I bought two of these for black friday and the kids love them', rating=5, do_recommend=True, num_helpful=0, date='2016-01-04'),
             Review(id=48890, username='zarm7', asin='B018Y229OU', title='This is a nice tablet', text='I bought it for reading books. And it works very well for that purpose.', rating=4, do_recommend=True, num_helpful=0, date='2016-09-02'),
             Review(id=84641, username='zabintenn', asin='B018Y229OU', title='Good tablet', text='I bought this tablet as a gift for my granddaughter to play games on. It is very easy for her to use and it is just the right size.', rating=4, do_recommend=True, num_helpful=0, date='2016-12-15'),
             Review(id=15839, username='zRoyals', asin='B01AHB9CN2', title='One of the best', text='Easy to use and elegant in design. Perfect Gift for Kids.', rating=5, do_recommend=True, num_helpful=0, date='2016-12-07'),
             Review(id=48019, username='yuty', asin='B01AHB9CN2', title='Terrifico', text='Great tablet for the price point....especially if you are big Amazon user.Expandable memory is a great feature.', rating=5, do_recommend=True, num_helpful=0, date='2017-01-07'),
             Review(id=63046, username='yuri', asin='B018Y229OU', title='great and cheap', text='Easy to use. Durable great material very happy with it.', rating=4, do_recommend=True, num_helpful=0, date='2016-01-08'),
             Review(id=37258, username='yroc', asin='B018Y229OU', title='excellent bargain', text='Excellent bargain and works for all purposes that a tablet is needed for.', rating=5, do_recommend=True, num_helpful=0, date='2015-12-28'),
             Review(id=64466, username='yosi', asin='B018Y226XO', title='great', text='great table for kids and parents control great gre', rating=5, do_recommend=True, num_helpful=0, date='2016-12-19')],
    "16": {'Missy': 4,
             '1234': 4,
             'Mike': 4,
             'Susan': 4,
             'Dave': 4,
             'Manny': 3,
             'Michael': 3,
             'Susie': 3,
             'Bill': 3,
             'James': 3,
             'Lisa': 3,
             'Kathy': 3,
             'paul': 3,
             'steve': 3,
             'John': 3,
             'Angie': 3,
             'Richard': 3,
             'Steve': 3,
             'Bubba': 3,
             'Chris': 3,
             'Grandma': 3,
             'Frank': 3},
    "17": {'Stuartc': 8,
             'Earthdog': 27,
             'Ellen': 10,
             'Rodge': 6,
             'Karch': 5,
             'FrankW': 5,
             'Kime': 5,
             'Mark': 5,
             '1Briansapp': 5,
             'trouble': 5,
             'Raza': 5},
    "20": {'Amazon 9W PowerFast Official OEM USB Charger and Power Adapter for Fire Tablets and Kindle eReaders': 4.7272727272727275,
             'Amazon Tap Smart Assistant Alexa enabled (black) Brand New': 4.6909090909090905,
             'All-New Kindle E-reader - Black, 6" Glare-Free Touchscreen Display, Wi-Fi - Includes Special Offers': 4.590163934426229,
             'Amazon Echo (2nd Generation) Smart Assistant Oak Finish Priority Shipping': 5.0,
             'Kindle Voyage E-reader, 6 High-Resolution Display (300 ppi) with Adaptive Built-in Light, PagePress Sensors, Wi-Fi - Includes Special Offers': 4.666666666666667,
             'All-new Echo (2nd Generation) with improved sound, powered by Dolby, and a new design Walnut Finish': 5.0,
             'Fire Kids Edition Tablet, 7 Display, Wi-Fi, 16 GB, Pink Kid-Proof Case': 4.603448275862069,
             'All-New Fire HD 8 Tablet, 8 HD Display, Wi-Fi, 32 GB - Includes Special Offers, Black': 4.583333333333333,
             'All-New Fire HD 8 Tablet, 8 HD Display, Wi-Fi, 32 GB - Includes Special Offers, Magenta': 4.574468085106383,
             'All-New Fire HD 8 Tablet, 8 HD Display, Wi-Fi, 16 GB - Includes Special Offers, Magenta': 4.6,
             'Kindle Oasis E-reader with Leather Charging Cover - Merlot, 6 High-Resolution Display (300 ppi), Wi-Fi - Includes Special Offers': 4.866666666666666,
             'Fire HD 8 Tablet with Alexa, 8 HD Display, 32 GB, Tangerine - with Special Offers': 3.8333333333333335,
             'Fire Tablet, 7 Display, Wi-Fi, 8 GB - Includes Special Offers, Magenta': 4.506039150354019},
    "25": [os.path.join('broken_file', 'rating4', 'very_helpful', 'very_helpful.json')],
    "26": sorted([os.path.join('broken_file', 'rating5', 'helpful', 'helpful.json'),
            os.path.join('broken_file', 'rating5', 'others.json')], reverse=True),
    "27": sorted([os.path.join('broken_file', 'rating5', 'others.json'),
            os.path.join('broken_file', 'rating5', 'helpful', 'helpful.json'),
            os.path.join('broken_file', 'rating4', 'very_helpful', 'very_helpful.json'),
            os.path.join('broken_file', 'rating4', 'others', 'short', 'short.json'),
            os.path.join('broken_file', 'rating4', 'others', 'others', 'others.json'),
            os.path.join('broken_file', 'rating4', 'not_helpful.json'),
            os.path.join('broken_file', 'rating3', 'others', 'others.json'),
            os.path.join('broken_file', 'rating3', 'long', 'long.json'),
            os.path.join('broken_file', 'others.json')], reverse=True),
    "28": 1,
    "29": 4995,
    "30": -0.03940707945194257,
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
    new_notebook = 'cs-301-test.ipynb'

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
    #jbn = [11,12,13,14,15,16,20]
    jbn = [10,11,12,13,14,15,20]
    if qnum in jbn:
        actual = (eval(compile(ast.parse(actual, mode='eval'), '', 'eval')))
    else:
        try:
            actual = ast.literal_eval(actual)
        except Exception as e:
            print("COULD NOT PARSE THIS CELL:")
            print(actual)
            raise e
    expected = expected_json[str(qnum)]

    expected_mismatch = False

    if type(expected) != type(actual):
        return "expected an answer of type %s but found one of type %s" % (type(expected), type(actual))
    elif type(expected) == float:
        if not math.isclose(actual, expected, rel_tol=1e-06, abs_tol=1e-06):
            expected_mismatch = True
    elif type(expected) == list:
        try:
            extra = set(actual) - set(expected)
            missing = set(expected) - set(actual)
            if missing:
                return "missing %d entries in list, such as: %s" % (len(missing), repr(list(missing)[0]))
            elif extra:
                return "found %d unexpected entries, such as: %s" % (len(extra), repr(list(extra)[0]))
            elif len(actual) != len(expected):
                return "expected %d entries in the list but found %d" % (len(expected), len(actual))
            elif sorted(actual) == sorted(expected) and actual != expected:
                return "list not sorted"
            else:
                for i,(a,e) in enumerate(zip(actual, expected)):
                    if a != e:
                        return "found %s at position %d but expected %s" % (str(a), i, str(e))
        except TypeError:
            # this happens when the list contains dicts.  Just do a simple comparison
            if actual != expected:
                return "expected %s" % repr(expected)
    elif type(expected) == dict:
        expected_keys = list(expected.keys())
        actual_keys = list(actual.keys())
        extra = set(actual_keys) - set(expected_keys)
        missing = set(expected_keys) - set(actual_keys)
        if missing:
            return "missing %d key(s) in dictionary, such as: %s" % (len(missing), repr(list(missing)[0]))
        elif extra:
            return "found %d unexpected key(s), such as: %s" % (len(extra), repr(list(extra)[0]))
        elif len(actual_keys) != len(expected_keys):
            return "expected %d key/value pairs in the dictionary but found %d" % (len(expected), len(actual))
        else:
            for key in expected:
                val = expected[key]
                if type(val) == float:
                    try:
                        if not math.isclose(actual[key], val, rel_tol=1e-06, abs_tol=1e-06):
                            return "found value {} for key {} but expected {}".format(actual[key], key, val)
                    except:
                        # this happens if actual[key] is not a number.
                        return "found value {} for key {} but expected {}".format(actual[key], key, val)
                else:
                    if val != actual[key]:
                        return "found value {} for key {} but expected {}".format(actual[key], key, val)
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
    results['score'] = 150.0 * passing / total

    print("\nSummary:")
    for test in results["tests"]:
        print("  Test %d: %s" % (test["test"], test["result"]))

    print('\nTOTAL SCORE: %.1f/150.0' % results['score'])
    with open('result.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
