import requests
from requests.adapters import HTTPAdapter, Retry
from bs4 import BeautifulSoup, Tag
from dataclasses import dataclass
import json
from time import sleep, time

BASE_URL = "https://serverfault.com"

@dataclass
class Post:
    title: str
    question: str
    top_answer: str
    url: str

    def __repr__(self):
        return f"{self.title}\n{self.question}\nAnswer:\n{self.top_answer}"
    
    def to_json(self):
        json = {
            "title": self.title,
            "question": self.question,
            "top_answer": self.top_answer,
            "url": self.url
        }
        return json

def get_post_links(page_num: int = 1, post_count: int = 50) -> list[str]:
    page_url = BASE_URL+"/questions?tab=Votes"
    if (page_num >= 2):
        page_url += f"&page={page_num}"
    post_links: list[str] = []
    while (len(post_links) < post_count):
        html = get_page_html(page_url)
        if not html:
            page_url = BASE_URL+f"/questions?tab=Votes&page={page_num+1}"
            page_num += 1
            continue
        soup = BeautifulSoup(html, features="lxml")
        limit = post_count - len(post_links)
        posts = soup.find_all("div", {"class": "s-post-summary"}, recursive=True, limit=limit)
        post_links += [post.find("a", {"class": "s-link"}, recursive=True).get("href") for post in posts]
        page_url = BASE_URL+f"/questions?tab=Votes&page={page_num+1}"
        page_num += 1
        sleep(0.2)
    return post_links

def get_post_content(post_url: str) -> Post | None:

    def get_div_text(div: Tag) -> str:
        text: list[str] = []
        if not div:
            return ""
        children = div.find("div", {"class": "s-prose"}).findChildren(recursive=False)
        for child in children:
            skip = False
            for grandchild in child.findChildren():
                if "s-notice" in grandchild.get("class", []):
                    skip = True
            if skip:
                continue
            text.append(child.text)
        return "\n".join(text)

    html = get_page_html(post_url)
    if not html:
        return

    soup = BeautifulSoup(html, "lxml")
    questionDiv = soup.find("div", {"class": "question"})
    answerDiv = soup.find("div", {"class": "answer"})
    question = get_div_text(questionDiv)
    answer = get_div_text(answerDiv)
    title = soup.find("a", {"class": "question-hyperlink"}).text

    return Post(
        title=title,
        question=question,
        top_answer=answer,
        url=post_url
    )

def get_page_html(url: str) -> str | None:
    s = requests.Session()

    retries = Retry(5, backoff_factor=0.5, status_forcelist=[429], raise_on_redirect=False, raise_on_status=False)
    s.mount(BASE_URL+"/", HTTPAdapter(max_retries=retries))

    resp = s.get(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0"})
    if resp.status_code != 200:
        print(f"{url} returned non-200 code: {resp.status_code}")
        return None
    return resp.text

def main():
    post_count = input("Please enter the number of posts to scrape: ")
    if not post_count.isdigit():
        return
    post_links = get_post_links(post_count=int(post_count))
    data = []
    start_time = time()
    print("Fetching posts... might take a while")
    for link in post_links:
        #print(BASE_URL+str(link))
        content = get_post_content(BASE_URL+str(link))
        if content:
            data.append(content.to_json())
        sleep(0.5)
    finish_time = time()
    print("Scraping complete!")
    total_time = finish_time-start_time
    print(f"Took {int(total_time // 60)} minutes and {int(total_time % 60)} seconds")

    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)

    print("Data written to data.json")

main()