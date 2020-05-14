## Setup instructions
Some instructions might be missing here as I did the setup long time ago. Please add more steps if you do the setup again

```
sudo apt-get install docker git

git clone https://github.com/msyamkumar/cs220-projects.git
cd cs301-projects/dockerGrader

sudo docker build -t grader .
pip install -r requirements.txt
```
 

~/.aws/credentials should include

```
[cs301ta]
aws_access_key_id = ask_tyler
aws_secret_access_key = ask_tyler
```
 

## Running Autograder
* Before running this command on any project, I would run it with '-s' flag to make sure everything is okay.
* '-o' override flag is mostly for the case when test.py changes after test results have been uploaded
```
sudo python dockerUtil.py p1 ? -ff main.ipynb -c
```



## Running Autograder for all projects
```
sudo sh grader-daemon.sh
```


## Running Autograder every hour
```
sudo watch -n 3600 'now=$(date +"%Y-%m-%d-%H:%M:%S"); sh grader-daemon.sh > "logs/$now.txt" 2>&1'
```
Setting up cron job would be better. I had issues with using sudo on department maching in a cron job, so I simply used `watch` command which I leave running in a tmux tab.

