# Wandering Bot. A primitive tracking bot
## What does it do?

A simple bot that sends requests to a specified website/service
with a provided interval and sends a message if the destination
is not available for some reason.

Persistance is included. Turning off and turning on will load
previously created visit destinations.

## Pre-requirements

1. Create a token for your bot through [@BotFather](https://t.me/BotFather) on Telegram
2. Install [Docker](https://www.docker.com/)
3. Create a `.env` file inside wandering-bot folder.
4. Put this in the created file and substitute `BOT_TOKEN` with yours:
```
MONGO_CONNECT=mongodb://mongo:27017/bot-db
BOT_TOKEN=<your-bot-father-generated-token>
```
5. GNU Make utility. Linux (pre-installed probably), [Windows](https://stackoverflow.com/questions/32127524/how-to-install-and-use-make-in-windows), [Mac](https://formulae.brew.sh/formula/make)

## Usage locally
Full bot:
```
make compdock
```


Only bot without the database:
```
make -i dock
```

## Deployment
**Via only a ssh key** for a private repository

Required secrets:
- `CONN_STRING` - your mongodb connection string
- `DOCKER_USERNAME` - your GitHub username. Used to pull an image from the repository
- `GHCR_TOKEN` - generated personal access token. Can be created in the developer settings on GitHub. Used to pull an image from the private repository. [Create link](https://github.com/settings/tokens). Set read access in for packages.
- `PRIVATE_SSH_KEY` - generated ssh-key. 
- `REMOTE_HOST` - your remote server IP
- `REMOTE_PORT` - ssh port to connect with 
- `REMOTE_USERNAME` - remote server user to connect as via ssh
- `TELEGRAM_TOKEN` - your @BotFather token 


**Additional steps**:
- Add the public part of the generated ssh key (*.pub file) to your remote's `authorized_keys` file in the `.ssh` folder. 
