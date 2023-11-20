# Setup

You'll want to set up the environment using the following:
```
make install
make venv
```
If you don't have redis, pull using homebrew:
```
brew tap redis-stack/redis-stack
brew install redis-stack
```
Then you'll need to create your SQS queues. Go to AWS console and create at least 3 queues: one URL frontier, one worker queue, one prioritizer queue.
Set the queue URLs and your AWS region in the config.py.
You'll also want to set up your OpenPageRank API key.
Go to https://www.domcop.com/openpagerank/auth/signup and sign up.
Set the API key in the config.py.
Then, we can set up our cache and run the app!
```
make cache
make run
```
To run test cases, run
```
make tests
```
To reset your environment, run
```
make clean
```
