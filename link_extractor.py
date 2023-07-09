from bs4 import BeautifulSoup, NavigableString
import requests


class LinkExtractor:
    def __init__(self, base_url: str, depth=0) -> None:
        self.base_url = base_url
        self.depth = depth
    

    def __get_html_of(self, url: str) -> str:
        resp = requests.get(url)
        if resp.status_code != 200:
            return None
        return resp.content.decode()


    def __get_links_from_html(self, page_html: str):
        soup = BeautifulSoup(page_html, 'html.parser')
        links = soup.find_all("a")
        return links
    

    # TODO: Work out how to return sub directories with full path
    def __get_all_links(self, link, depth: int):
        if depth == 0:
            return link
        else:
            try:
                next_link = link.get('href', '')
                next_link = next_link if next_link.startswith(self.base_url) else self.base_url + next_link
                page_html = self.__get_html_of(next_link)
                links = self.__get_links_from_html(page_html)
            except:
                return link
            if len(links) == 0:
                return link
            else:
                sub_links = []
                for link in links:
                    sub_links += self.__get_all_links(link, depth - 1)
                    sub_links.append(link)
                return sub_links


    def get_links(self) -> list[str]:
        page_html = self.__get_html_of(self.base_url)
        links = self.__get_links_from_html(page_html)
        
        if self.depth == 0:
            return self.__clean_links(links)

        for i in range(len(links)):
            links += list(self.__get_all_links(links[i], self.depth))
        return self.__clean_links(links)
    

    def __clean_links(self, links) -> list[str]:
        links_cleaned = set()
        for link in links:
            if isinstance(link, NavigableString):
                continue
            try:
                link = link.get('href', '')
            except:
                print(link)
                continue
            if len(link) > 0:
                if link.startswith("https://") or link.startswith("http://"):
                    links_cleaned.add(link)
                else:
                    links_cleaned.add(self.base_url + link)
        return list(links_cleaned)


# Testing
'''le = LinkExtractor("http://books.toscrape.com", 0)
list_1 = le.get_links()
for link in list_1:
    print(link)
print(len(list_1))'''

'''le = LinkExtractor("http://books.toscrape.com", 1)
list_2 = le.get_links()
print(len(list_2))'''

'''le = LinkExtractor("http://books.toscrape.com/", 2)
list_3 = le.get_links()
print(len(list_3))'''