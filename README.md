## About

<img align="right" width="80" src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Telegram_logo.svg/768px-Telegram_logo.svg.png">

<img align="right" width="80" src="https://i.imgur.com/2HA4SrW.png?1">

This is a [telegram bot](https://t.me/au_appartment_bot), that takes all incoming messages in the email box and resends them to the telegram chat of my appartment, where I live.

The project is designed to reduce information noise and allow residents to not miss any important announcement. The use of paper is also reduced, which is good for ecology.

## Usage

Copy `config.dev.yml` to `config.prod.yml` and change variables inside. Then install required dependencies:

```bash
sudo pip install --upgrade -r requirements.txt
```

To add a task to cron run `crontab -e`, then add the line:

```
*/30 * * * *   cd /home/xamgore/au-appartment-bot/ && ./main.py
```
