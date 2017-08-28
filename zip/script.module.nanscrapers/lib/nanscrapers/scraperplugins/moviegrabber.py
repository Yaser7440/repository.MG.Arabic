import re
import requests
import xbmc
import urllib
from ..scraper import Scraper
from BeautifulSoup import BeautifulSoup as BS
import urlparse

session = requests.Session()


class moviegrabber(Scraper):
    domains = ['https://moviegrabber.tv/']
    name = "moviegrabber"
    sources = []

    def __init__(self):
        self.base_link = 'https://moviegrabber.tv/'
        self.sources = []

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            search_id = urllib.quote_plus(title.lower())
            start_url = self.base_link+'search/?id=' + search_id
            html = BS(session.get(start_url, verify=False).content)
            thumbnails = html.findAll("div", attrs={"class": "thumbnail"})
            for thumbnail in thumbnails:
                link_title = thumbnail.find("p").text
                if not (title in link_title and year in link_title):
                    continue
                url = thumbnail.find("a")["href"]
                movie_link = self.base_link + url
                html2 = BS(session.get(movie_link, verify=False).content)
                scripts = html2.findAll("script")
                for script in scripts:
                    match = re.findall(
                        '\[?{?"id": "(.*?)".*?"title": "(.*?)"',
                        script.text,
                        re.DOTALL)
                    if not match:
                        continue
                    match2 = re.findall(
                        'showid.attr\("value", (\d+)',
                        script.text,
                        re.DOTALL)
                    if not match2:
                        continue
                    match3 = re.findall(
                        'var csrf = .*?value="(.*?)"',
                        script.text,
                        re.DOTALL)
                    if not match3:
                        continue
                    csrf = match3[0]
                    showid = match2[0]
                    for i, _ in enumerate(match):
                        epid = match[i][0]
                        epname = match[i][1].replace("\\u00a0", " ")
                        quality = re.findall("\[(.*?)\]", epname)
                        if not quality:
                            quality = "unknown"
                        else:
                            quality = quality[0]

                        data = {
                            "epid": epid,
                            "showid": showid,
                            "epname": epname,
                            "foo": "%s (%s)" % (title, year),
                            "csrfmiddlewaretoken": csrf
                        }
                        headers = {"Referer": movie_link}
                        links_html = BS(session.post(self.base_link + "link/",
                                                     data=data,
                                                     verify=False,
                                                     headers=headers).text)
                        list_group_items = links_html.findAll(
                            "a",
                            attrs={"class": "list-group-item"})
                        link_set = set()
                        for list_group_item in list_group_items:
                            link = list_group_item["href"]
                            play_link = self.base_link + link[1:]
                            link_set.add(play_link)
                        for url2 in link_set:
                            html3 = session.get(url2, verify=False).text
                            match2 = re.findall('.*?<source src="(.*?)"',
                                                html3)
                            if match2:
                                for link in match2:
                                    # get base host (ex. www.google.com)
                                    loc = urlparse.urlparse(link).netloc
                                    loc_fragment = loc.split(".")[1:-1]
                                    source_base = str.join(".",
                                                           loc_fragment)
                                    if "google" in source_base:
                                        source_base = "google video"
                                    link = link.replace('&amp;', "&")
                                    self.sources.append(
                                        {'source': source_base,
                                         'quality': quality,
                                         'scraper': self.name,
                                         'url': link,
                                         'direct': True})
                return self.sources
        except Exception, argument:
            return self.sources

    def scrape_episode(self,title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            search_id = urllib.quote_plus(title.lower())
            start_url = self.base_link+'search/?id=' + search_id
            html = BS(session.get(start_url, verify=False).content)
            thumbnails = html.findAll("div", attrs={"class": "thumbnail"})
            for thumbnail in thumbnails:
                link_title = thumbnail.find("p").text
                if not title in link_title:
                    continue
                url = thumbnail.find("a")["href"]
                movie_link = self.base_link + url
                html2 = BS(session.get(movie_link, verify=False).content)                
                caption = html2.findAll("div", attrs={"class":"caption"})[0]
                link_year = re.findall("Year: (\d+)", str(caption.contents[1].text))[0]
                if link_year != show_year:
                    continue
                scripts = html2.findAll("script")
                for script in scripts:
                    match = re.findall(
                        '\[?{?"id": "(.*?)".*?"title": "(.*?)"',
                        script.text,
                        re.DOTALL)
                    if not match:
                        continue
                    match2 = re.findall(
                        'showid.attr\("value", (\d+)',
                        script.text,
                        re.DOTALL)
                    if not match2:
                        continue
                    match3 = re.findall(
                        'var csrf = .*?value="(.*?)"',
                        script.text,
                        re.DOTALL)
                    if not match3:
                        continue
                    csrf = match3[0]
                    showid = match2[0]
                    for i, _ in enumerate(match):
                        epid = match[i][0]
                        epname = match[i][1].replace("\\u00a0", " ")
                        if epname.lower() != "%s s%02de%02d" % (title.lower(), int(season), int(episode)):
                            continue
                        data = {
                            "epid": epid,
                            "showid": showid,
                            "epname": epname,
                            "foo": "%s (%s)" % (title, year),
                            "csrfmiddlewaretoken": csrf
                        }
                        headers = {"Referer": movie_link}
                        links_html = BS(session.post(self.base_link + "link/",
                                                     data=data,
                                                     verify=False,
                                                     headers=headers).text)
                        list_group_items = links_html.findAll(
                            "a",
                            attrs={"class": "list-group-item"})
                        link_set = set()
                        for list_group_item in list_group_items:
                            link = list_group_item["href"]
                            play_link = self.base_link + link[1:]
                            quality = re.findall("(\d+)p", list_group_item.text)
                            if not quality:
                                quality = "unknown"
                            else:
                                quality = quality[0]
                            link_set.add((play_link, quality))
                        for (url2, quality) in link_set:                            
                            html3 = session.get(url2, verify=False).text
                            match2 = re.findall('.*?<source src="(.*?)"',
                                                html3)
                            if not match2:
                                html3 = BS(html3)
                                iframe = html3.find("iframe")                                
                                match2 = [iframe["src"].replace("/preview", "")]
                                quality = "HD"
                            if match2:
                                for link in match2:
                                    # get base host (ex. www.google.com)
                                    loc = urlparse.urlparse(link).netloc
                                    loc_fragment = loc.split(".")[1:-1]
                                    source_base = str.join(".",
                                                           loc_fragment)
                                    if "google" in source_base:
                                        source_base = "google video"
                                    link = link.replace('&amp;', "&")
                                    self.sources.append(
                                        {'source': source_base,
                                         'quality': quality,
                                         'scraper': self.name,
                                         'url': link,
                                         'direct': True})
                return self.sources
        except Exception, argument:
            return self.sources
