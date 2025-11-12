from bs4 import BeautifulSoup

with open("website.html") as file:
    content = file.read()

soup = BeautifulSoup(content, "html.parser")
print(soup.title)
print(soup.title.name)
print(soup.find_all("p"))
for paragraph in soup.find_all("p"):
    print(paragraph.text)
for tag in soup.find_all(name="a"):
    print(tag.get("href"))
