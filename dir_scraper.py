from dir_fuzzer import Fuzzer
from link_extractor import LinkExtractor

from os.path import exists
import click

# TODO: Add mulit-threading
# TODO: Add additional status codes

@click.command()
@click.option("--url", "-u", prompt="Enter the url", help="The URL to FUZZ. Required.")
@click.option("--depth", "-d", default=0, help="The recursion depth on each link (Default = 0).")
@click.option("--wordlist", "-w", prompt="Enter the wordlist", help="The directory wordlist. Required.")
@click.option("--mode", "-m", default=0, help="Fuzz mode: 0 = dir fuzz only, 1 = fuzz and scrape (Default = 0).")
def main(url, depth, wordlist, mode):
    if not exists(wordlist):
        print("No path to wordlist")
        exit(1)
    
    # TODO: Add recursion
    discovered_dirs = [url]
    dir_fuzzer = Fuzzer(url, wordlist)
    discovered_dirs += dir_fuzzer.get_matching_dirs()

    # Testing
    print(discovered_dirs)
    print(len(discovered_dirs))

    # TODO: Logic error, change to if link starts with '/' add base URL, else add base URL + dir_path
    if mode == 1:
        for i in range(len(discovered_dirs)):
            le = LinkExtractor(discovered_dirs[i], depth)
            discovered_dirs += le.get_links()
    
    # Testing
    print(discovered_dirs)
    print(len(discovered_dirs))


if __name__ == "__main__":
    main()