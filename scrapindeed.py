from datetime import datetime
import requests
from bs4 import BeautifulSoup
import csv
from time import sleep

url = 'https://ae.indeed.com/jobs?q={}&l={}&fromage=7'


def make_url(position, location):
    return url.format(position, location)


def extractData(card):
    try:
        jobtitle = card.find('h2', 'jobTitle').find_next(
            'span').find_next('span').get('title')
    except AttributeError:
        jobtitle = 'ew'
    try:
        companyName = card.find('span', 'companyName').text
    except AttributeError:
        companyName = ''
    try:
        snippet = card.find('div', 'job-snippet').ul.findAll('li')
        specs = ','.join([item.text.strip() for item in snippet if str(item)])
    except AttributeError:
        specs = ''
    try:
        rating = card.find('span', 'ratingNumber').get('aria-label')
    except AttributeError:
        rating = ''
    try:
        rating = card.find('span', 'ratingNumber').get('aria-label')
    except AttributeError:
        rating = ''
    jobUrl = 'https://ae.indeed.com' + card.get('href')

    data = (jobtitle, companyName, rating, specs, jobUrl)
    return data


def main(position, location):
    jobs = []
    url = make_url(position, location)
    """ fetch & parse """
    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        listing = soup.find_all('a', 'result')
        for item in listing:
            job = extractData(item)
            jobs.append(job)

        try:
            nextp = soup.find('a', {'aria-label': 'Next'}).get('href')
            url = 'https://ae.indeed.com' + nextp
            sleep(1)
        except AttributeError:
            break

    with open('results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['jobtitle', 'companyName', 'rating', 'specs'])
        writer.writerows(jobs)


main('software developer', 'dubai')
