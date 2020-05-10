#!/bin/sh

#Adapted from https://stackoverflow.com/questions/3258243

cd $(dirname "$0")

UPSTREAM=${1:-'@{u}'}
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse "$UPSTREAM")
BASE=$(git merge-base @ "$UPSTREAM")

PY=~/miniconda3/envs/cs220grading/bin/python3

run_grader() {
    export PYTHONDONTWRITEBYTECODE=1
    export AWS_SHARED_CREDENTIALS_FILE="~/.aws/credentials"

    echo "Running Auto-grader\n"

    echo "\n\nAuto-grader for p1:"
    sudo $PY dockerUtil.py p1 ? -ff main.ipynb -c

    echo "\n\nAuto-grader for p2:"
    sudo $PY dockerUtil.py p2 ? -ff main.ipynb -c

    echo "\n\nAuto-grader for p3:"
    sudo $PY dockerUtil.py p3 ? -ff main.ipynb -c

    echo "\n\nAuto-grader for p4:"
    sudo $PY dockerUtil.py p4 ? -ff main.ipynb -c

    echo "\n\nAuto-grader for p5:"
    sudo $PY dockerUtil.py p5 ? -ff main.ipynb -c

    echo "\n\nAuto-grader for p6:"
    sudo $PY dockerUtil.py p6 ? -ff main.ipynb -c

    echo "\n\nAuto-grader for p7:"
    sudo $PY dockerUtil.py p7 ? -ff main.ipynb -c

    echo "\n\nAuto-grader for p8:"
    sudo $PY dockerUtil.py p8 ? -ff main.ipynb -c

    echo "\n\nAuto-grader for p9:"
    sudo $PY dockerUtil.py p9 ? -ff main.ipynb -c -x *.zip

    echo "\n\nAuto-grader for p10:"
    sudo $PY dockerUtil.py p10 ? -ff main.ipynb -c -x *.json

    echo "\n\nAuto-grader for Final:"
    sudo $PY dockerUtil.py final ? -ff Final_Exam.ipynb 
}

ntpdate -s time.nist.gov
git fetch

if [ $LOCAL = $REMOTE ]; then
    echo "Up-to-date"
    run_grader
elif [ $LOCAL = $BASE ]; then
    echo "Need to pull"
    git pull
    run_grader
elif [ $REMOTE = $BASE ]; then
    echo "Need to push"
else
    echo "Diverged"
fi
