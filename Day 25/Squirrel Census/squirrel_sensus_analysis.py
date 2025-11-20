import pandas

primary_fur_color = pandas.read_csv("2018_Central_Park_Squirrel_Census_-_Squirrel_Data.csv")
print(primary_fur_color["Primary Fur Color"])

grey_color = primary_fur_color[primary_fur_color["Primary Fur Color"] == "Gray"]
print(len(grey_color))
Cinnamon_color = primary_fur_color[primary_fur_color["Primary Fur Color"] == "Cinnamon"]
print(len(Cinnamon_color))
Black_color = primary_fur_color[primary_fur_color["Primary Fur Color"] == "Black"]
print(len(Black_color))

data_dict = {
    "Fur Color": ["Grey", "Black", "Cinnamon"],
    "Count": [len(grey_color), len(Black_color), len(Cinnamon_color)]
}
data = pandas.DataFrame(data_dict)
data.to_csv("squirrel_count.csv")
