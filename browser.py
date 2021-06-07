import sys
import os
from collections import deque

import requests
import tldextract
import validators
from bs4 import BeautifulSoup, SoupStrainer
from colorama import Fore, init


class TextBasedBrowser():
    def __init__(self, directory):
        init(strip=False)
        self.saved_pages = dict()
        self.history = deque()
        self.welcome_message = self.color_text("magenta",
                                               '''                                               
        Welcome to Squirrel-Navigator!!
        
        Here are your options:
        
            * Enter a URL (e.g. "squirrelcom.github.io/seARch/")
            * Enter "back" to go to previous page
            * Enter just domain name to see saved search (e.g."seARch" for "squirrelcom.github.io/seARch/")
            * Enter "exit" to exit the browser
            
        ''')
        self.input_message = "\n" + self.color_text("magenta", "Enter a URL or back or exit: ")
        self.state = "active"
        self.create_cache_directory(directory)
        self.directory = directory

    @staticmethod
    def create_cache_directory(directory):
        if not os.path.exists(directory):
            os.mkdir(directory)

    @staticmethod
    def color_text(color, text):
        colors = {
            "blue": Fore.BLUE,
            "green": Fore.GREEN,
            "magenta": Fore.MAGENTA,
            "red": Fore.RED
        }
        return f"{colors[color]}{text}{Fore.RESET}"

    @staticmethod
    def valid_url(url):
        return validators.url(url)

    @staticmethod
    def get_domain(url):
        extract = tldextract.extract(url)
        domain = extract.domain
        if extract.subdomain:
            domain = f"{extract.subdomain}.{extract.domain}"
        return domain

    def save_page(self, domain, page_content):
        file_name = f"{domain}.txt"
        file_path = os.path.join(self.directory, file_name)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(page_content)
            self.saved_pages[domain] = file_path

    def fetch_from_cache(self, url):
        info_message = self.color_text("green", "Fetching from cache...")
        file_name = self.saved_pages[url]
        with open(file_name, "r", encoding="utf-8") as file:
            file_content = file.read()
            return f"{info_message}\n\n{file_content}"

    def parse_page(self, content):
        result = ""
        tags = ['p', 'a', 'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        soup = BeautifulSoup(content, "html.parser", parse_only=SoupStrainer(tags))

        for script in soup(["script", "style"]):
            script.decompose()

        for link in soup(["a"]):
            link.string = self.color_text("blue", link.text)

        content = soup.stripped_strings
        for line in content:
            result += line + "\n"
        return result

    def fetch_page(self, url):
        try:
            # page = requests.get(url)
            page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        except requests.ConnectionError:
            return f"{url} does not exist on Internet"
        return self.parse_page(page.content)

    def get_page_content(self, url):
        if url in self.saved_pages:
            return self.fetch_from_cache(url)
        else:
            url = url if url.startswith("https://") else f"https://{url}"
            if not self.valid_url(url):
                return self.color_text("red", "Invalid URL error!")
            else:
                page_content = self.fetch_page(url)
                domain = self.get_domain(url)
                self.save_page(domain, page_content)
                self.history.append(url)
                return page_content

    def find_prev_page(self):
        if len(self.history) > 1:
            self.history.pop()
            return self.history.pop()
        return None

    def process_request(self, user_input):
        page_url = user_input
        if user_input == "exit":
            self.state = "stop"
            return "Bye!"
        elif user_input == "back":
            page_url = self.find_prev_page()
            if not page_url:
                return "No history"

        return self.get_page_content(page_url)


if __name__ == "__main__":
    cache_directory = sys.argv[1]
    text_based_browser = TextBasedBrowser(cache_directory)
    print(text_based_browser.welcome_message)

    while text_based_browser.state != "stop":
        print(text_based_browser.input_message, end="")
        user_input = input()
        print()
        try:
            print(text_based_browser.process_request(user_input))
        except:
            # actual exception can be added to logging mechanism
            print("Error got in processing request")
