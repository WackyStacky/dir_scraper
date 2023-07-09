import requests


class Fuzzer:
    def __init__(self, base_url: str, word_list_path: str) -> None:
        self.base_url = base_url
        self.word_list_path = word_list_path
    

    # TODO: add additional response codes
    def __is_valid_request(self, url: str) -> bool:
        resp = requests.get(url)
        return resp.status_code == 200
    

    def get_matching_dirs(self) -> list:
        matching_dirs = []
        with open(self.word_list_path, 'r') as fh:
            for dir in fh.readlines():
                dir = dir.strip()
                request_url = self.base_url
                request_url += dir if self.base_url.endswith("/") else "/" + dir

                if self.__is_valid_request(request_url):
                    print(f'{request_url} responded with status code 200')
                    matching_dirs.append(request_url)
        return matching_dirs


# Testing
'''fuzz = Fuzzer("http://books.toscrape.com","/home/theonly_wilko/scripts/dir_scraper/test_wordlist.txt")
print(len(fuzz.get_matching_dirs()))'''
