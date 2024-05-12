# Question League
A real-time web application, a quiz game that can be played with friends—[try it now.](https://qleague.yahia.tech)

## Features
**Single Player Mode:** The game can be played solo; change the question category as you prefer.   
**Multi Player Mode:** It is also playable with others by creating or joining a room.   
**Authentication:** The progress of logged-in users is saved, with a simple leaderboard for the top 10.   

## Contributing
New ideas and features are encouraged. to integrate with us:
1. Fork the repository into your account.
2. Apply your ideas to the fork.
3. Once everything is ready to integrate, submit a pull request to this repo.
> It would be nice if you shared your thoughts with us in a discussion.

## Install & Run
### Install
To run the project in your machine follow this steps.
> Make sure you have Python 3.8 or higher installed in your machine.  
> To check the current version:
> ```sh
> python3 -V
> ```

* Clone the repository
```sh
git clone https://github.com/yahia-soliman/question-league.git
cd question-league
```

* Create a python virtual env
```sh
python -m venv .venv
source .venv/bin/activate
```

* Install required packages
```sh
pip install -r requirements.txt
```
**At this point the project is ready to be used with SQLite3 you can procced to [Run](#run) the application.**

> If you have MySQL installed and wish to use it istead of SQLite3.   
> We need to install one more package to the .venv
> ```sh
> pip install mysqlclient
> ```
> If any error occured refer to [this installation guide.](https://pypi.org/project/mysqlclient/)

### Run
* To run the application server
```sh
. setup guni
```
* To run a live-server (to reload the web page if a file is modified)
    > Make sure you have [entr](https://eradman.com/entrproject/) installed
```sh
. setup live
```
* To run the tailwindcss transpiler (if you need to modify the UI)
    > Make sure you have [tailwind](https://tailwindcss.com/docs/installation) installed
```sh
. setup twd
```

## License
[Question League](https://qleague.yahia.tech/) is under the [MIT](https://github.com/yahia-soliman/question-league/blob/main/LICENSE) license.   
All question data provided by the API is under the [Creative Commons Attribution-ShareAlike 4.0](https://creativecommons.org/licenses/by-sa/4.0/) International License according to the data source [opentdb.com](https://opentdb.com/api_config.php)
