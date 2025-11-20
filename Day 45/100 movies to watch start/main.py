import requests
from bs4 import BeautifulSoup

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

# Write your code below this line 👇

soup = BeautifulSoup(requests.get(URL).content, "html.parser")
titles_list = soup.find_all(name="h3", class_="title")
titles_text = [title.getText() for title in titles_list][::-1]
with open("movies.txt", "w") as file:
    file.write("\n".join(titles_text))
