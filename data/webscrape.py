import json
import requests
try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

class WebScraper:
    def read_link(self, link):
        if "mobalytics" in link:
            self.mobalytics(link)
        else:
            print(":(")

    def mobalytics(self, link):
        link1 = link[:25]
        html = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'}).text
        parsed_html = BeautifulSoup(html, features="html.parser")
        text = parsed_html.find_all("div", {"class": "css-1d45r7t ex6nprs0"})
        final_list = []
        for row in text[0]:
            found = row.find_all(['a'])
            if len(found) > 0:
                link2 = found[0]["href"]
                link_final = link1 + link2
                final_list.append(self.mobalytics2(link_final))
            # break
        with open('comps.json', 'w') as outfile:
            json.dump(final_list, outfile)

    def mobalytics2(self, link):
        html = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'}).text
        parsed_html = BeautifulSoup(html, features="html.parser")
        text = parsed_html.find_all("div", {"class": "enl0bsh14 css-javxkw e31gwcf0"})
        final = []
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
        return self.make_dict(final, early, mid)

    def make_dict(self, final, early, mid):
        return {"final": final, "early": early, "mid": mid}



if __name__ == '__main__':
    w = WebScraper()
    w.read_link("https://app.mobalytics.gg/tft/team-comps")