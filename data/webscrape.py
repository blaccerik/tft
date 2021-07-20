import json
import time

import requests
import urllib.request
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

class WebScraper:

    def read_link(self, link):
        if "mobalytics" in link:
            self.mobalytics(link)
        elif "tftactics" in link:
            self.tftactics(link)
        else:
            print(":(")

    def mobalytics(self, link):
        link1 = link[:25]
        html = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'}).text
        parsed_html = BeautifulSoup(html, features="html.parser")
        text = parsed_html.find_all("div", {"class": "m-1onxboh ex6nprs2"})
        final_list = []
        print(text)
        for row in text[0]:
            found = row.find_all(['a'])
            if len(found) > 0:
                link2 = found[0]["href"]
                link_final = link1 + link2
                final_list.append(self.mobalytics2(link_final))
        with open('comps_moba.json', 'w') as outfile:
            json.dump(final_list, outfile)

    def mobalytics2(self, link):
        html = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'}).text
        parsed_html = BeautifulSoup(html, features="html.parser")
        text = parsed_html.find_all("div", {"class": "enl0bsh0 m-17wd5gd e31gwcf1"})
        final = []
        # champions
        for row in text[0]:
            found = row.find_all(['a'])[0]["href"]
            name = found[15:]
            final.append(name)
        early = []
        for row in text[1]:
            found = row.find_all(['a'])[0]["href"]
            name = found[15:]
            early.append(name)
        mid = []
        for row in text[2]:
            found = row.find_all(['a'])[0]["href"]
            name = found[15:]
            mid.append(name)
        order = []

        # item order
        text = parsed_html.find("div", {"class": "m-1o7d3sk e3an59i3"})  # .find_all('img', alt=True)
        for row in text:
            item = row.find('img')["alt"]
            order.append(item)

        # items
        text = parsed_html.find_all("p", {"class": "m-1ycn726 elh7uow4"})
        all_items = []
        # print(text)
        for row in text:
            item = row.text
            all_items.append(item)

        text = parsed_html.find("div", {"class": "e1ez9x2v0 m-560ppy e83jq8m4"})
        options = []
        # print(text)
        if text is not None:
            text2 = text.find_all('img', alt=True)
            for row in text2:
                name = row["alt"]
                options.append(name)

        name = parsed_html.find("h1", {"class": "m-1sdlayj euxbs4g3"}).text

        letter = parsed_html.find("div", {"class": "enl0bsh6 m-1j9xggc e4kvc91"}).find('img')["alt"]
        # print(letter)

        # print(final, early, mid)
        # print(order, all_items)
        dicta = {}
        dicta["name"] = name
        dicta["early"] = early
        dicta["final"] = final
        dicta["mid"] = mid
        dicta["item order"] = order
        dicta["all items"] = all_items
        dicta["options"] = options
        dicta["letter"] = letter
        return dicta

    def tftactics(self, link):
        # cookies = dict(cookies_are='working')
        # r = requests.get(link, cookies=cookies)
        # print(r.text)

        # s = requests.Session()
        #
        # html = s.get(link).text
        # print(html)
        # text = parsed_html.find_all("div", {"class": "col-12 col-lg-9 main"})
        # using selenium as normal request wont work

        # html = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'}).text
        # parsed_html = BeautifulSoup(html, features="html.parser")
        # text = parsed_html.find_all("div", {"class": "col-12 col-lg-9 main"})
        # print(text)

        driver = webdriver.Firefox()
        driver.get(link)
        WebDriverWait(driver, 17)
        driver.find_element_by_class_name("cmpboxbtns").find_element_by_id("cmpwelcomebtnyes").click()
        # WebDriverWait(driver, 5)
        time.sleep(10)

        # tt = driver.find_element_by_class_name("sidenav")
        # print(tt)
        # ttt = tt.find_elements_by_class_name("sidenav-link")
        # print(ttt)
        # ttt[1].click()
        # tt.find("div", {"class": "sidenav-link"}).click()
        # button.click()
        # time.sleep(0.5)
        time.sleep(0.5)

        a = driver.find_elements_by_class_name("team-portrait")
        for b in a:
            c = b.find_element_by_class_name("team-more")
            c.click()
            time.sleep(0.1)
        html = driver.page_source
        parsed_html = BeautifulSoup(html, features="html.parser")
        text = parsed_html.find_all("div", {"class": "team-portrait"})

        final_list = []

        for i in text:

            dicta = {}

            some_list = []
            name = i.find("div", {"class": "team-name"}).text
            dicta["name"] = name

            # main comp
            chars = i.find("div", {"class": "team-characters"}).find_all('img', alt=True)
            for char in chars:
                some_object = char["alt"].lower()
                some_list.append(some_object)
            dicta["final"] = some_list

            # early
            exp = i.find("div", {"class": "team-expanded"})
            exp_list = exp.find("div", {"class": "team-expanded-list"}).find_all('img', alt=True)
            some_list = []
            for champ in exp_list:
                name2 = champ["alt"].lower()
                some_list.append(name2)
            dicta["early"] = some_list

            # items prio
            exp_items = exp.find("div", {"class": "team-expanded-group items"}).find_all('img', alt=True)
            some_list = []
            for more_opt2 in exp_items:
                some_list.append(more_opt2["alt"].lower())
            dicta["item order"] = some_list

            # more opt
            more_opt = exp.find("div", {"class": "team-expanded-group options"}).find_all('img', alt=True)
            some_list = []
            for more_opt2 in more_opt:
                some_list.append(more_opt2["alt"].lower())
            dicta["options"] = some_list
            final_list.append(dicta)
        with open('comps_tactics.json', 'w') as outfile:
            json.dump(final_list, outfile)
        driver.quit()





if __name__ == '__main__':
    w = WebScraper()
    w.read_link("https://app.mobalytics.gg/tft/team-comps")
    # w.read_link("https://tftactics.gg/tierlist/team-comps")