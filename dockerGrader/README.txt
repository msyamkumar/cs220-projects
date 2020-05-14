## Setup instructions
(Some instructions might be missing as I did the setup long time ago)

```
sudo apt-get install docker git

git clone https://github.com/msyamkumar/cs220-projects.git
cd cs301-projects/dockerGrader

sudo docker build -t grader .
```
 

~/.aws/credentials should include

```
[cs301ta]
aws_access_key_id = ask_tyler
aws_secret_access_key = ask_tyler
```
 


pip install -r requirements.txt

## Running Autograder
```
sudo python dockerUtil.py p1 ? -ff main.ipynb -c
```

## Running Autograder for all projects

