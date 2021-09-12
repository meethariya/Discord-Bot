# Discord-Bot
A Python Discord Bot working with various APIs and hosted on replit.
Various APIs are used such as [NASA's api](https://api.nasa.gov/index.html#signUp), [trivia API](https://opentdb.com/api_config.php), [quote API](https://zenquotes.io/api/random), [weather API](https://openweathermap.org/api), [Joke API](https://pypi.org/project/jokeapi/) and [Bored API](https://www.boredapi.com/). All are free having certain rate limit/day.
We are required to have an account for some APIs to get a key.

Replit shuts down the server after some time if its not being used. So in order to overcome that along with Discord Bot, A simple Flask API is built and is executed on a different thread simultaneously and is pinged every 5 mins by [uptime robot](https://uptimerobot.com/) to make sure it doesn't shutdown.
