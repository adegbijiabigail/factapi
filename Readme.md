# factapi
<br/>
Since knowledge is power, here's a fun fact api. This is a small project less than ~150 lines of code.
<br>
It works by scraping and parsing posts off of the r/todayilearned subreddit and storing them in a database for them to be randomly queried.
<br>
The api has only one endpoint --> /getrandom
<br>
Example response:
<br/>
{
    "response":"The AI artist 👩‍🎨 DALL-E is named after Disney/pixars WALL-E and Salvador Dali."
}
<br>
To run:
<br>
pip install requirements.txt
python api.py