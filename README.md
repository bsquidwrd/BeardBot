# BeardBot

### Requirements
* Linux (any kernel should be fine)
* git
* Python 3.7 or higher

### Setup
* Clone the repository to your server: `git clone https://github.com/bsquidwrd/BeardBot.git`
* Install the requirements: `pip install -r requirements.txt`
* Setup a MySQL instance and create a database for the bot along with a user that has full permissions to it
* Make your `environment.py` file: `cp environment_example.py environment.py`
* Edit `environment.py` accordingly with your OAUTH token for the Twitch Account for the bot to run as, etc
* Create the Database tables with `python3.7 manage.py migrate` (This also serves a good point to ensure your Database configuration works properly)

### Running
Run the following to run the Twitch Bot portion (responds to commands, etc. Replace `python3.7` with your python executable)
```bash
python3.7 bot.py
```

Run the following to run the Streamlabs portion (logs all the donations/subscriptions/resubscriptions/bits along with point values. Replace `python3.7` with your python executable)
```bash
python3.7 streamlabs.py
```
