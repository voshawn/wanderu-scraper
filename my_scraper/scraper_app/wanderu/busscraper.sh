#!usr/bin/env bash

# be sure to change both virtualenv directory and scrape/living_social
# directory to where your venv and code is.
source ~/.virtualenvs/busscraper/bin/activate
cd ~/webapps/busscraper
scrapy crawl gotobus