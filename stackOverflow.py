from selenium import webdriver
from bs4 import BeautifulSoup
driver = webdriver.Chrome()

from stackapi import StackAPI
import time
import json

# takes in a stack overflow question link
def scrape_post(link):
    driver.get(link)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # find the title
    title = soup.find('a', class_='question-hyperlink')
    if title:
        title = "TITLE: " + title.get_text() + '\n'
        print(title)
    else:
        title = ""

    # find the question text
    # question = soup.find('div', class_="s-prose js-post-body")
    # if question:
    #     question = "QUESTION" + question.get_text() + "\n"
    #     print(question)
    # else:
    #     question = ""

    # find the top answer
    answer = ""
    top_answer = soup.find("div", class_="answer js-answer accepted-answer js-accepted-answer")
    if top_answer:
        answer = top_answer.find("div", class_="s-prose js-post-body")
        answer = "ANSWER: " + answer.get_text() + "\n"

    # result = title + question + answer
    result = title + answer
    return result

def get_top_links():
    SLEEP = 1
    MAX_LINKS = 5000
    SITE = StackAPI('stackoverflow')
    count = 0
    has_next = True
    links = []

    while has_next and count <= MAX_LINKS:
        questions = SITE.fetch('questions', sort='votes')
        items = questions["items"]
        new_links = [i['link'] for i in items if i["is_answered"] == True and i['link'] != ""]
        count += len(new_links)
        links += new_links
        has_next = questions["has_more"]
        print("retrieved a batch of links")
        time.sleep(SLEEP)

    with open('links.json', 'w') as json_file:
        json.dump(links, json_file, indent=4)
    return links

if __name__ == "__main__":
    get_top_links()