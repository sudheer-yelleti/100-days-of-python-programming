are_there_further_bids = "Yes"
bid_date = {}
highest_bid = 0
highest_bidder_name = ""


def AddBid():
    bidder_name = input("Enter your name:")
    bid_value = int(input("Enter your bid:"))
    bid_date[bidder_name] = bid_value


while are_there_further_bids == "Yes":

    AddBid()

    are_there_further_bids = input("Would you like to do another bid? (Yes/No): ")
    if are_there_further_bids == "Yes":
        print("\n" * 20)
    else:
        for key in bid_date:
            if bid_date[key] > highest_bid:
                highest_bid = bid_date[key]
                highest_bidder_name = key

print(f"Highest bid is from {highest_bidder_name}, and the bid amount is: {highest_bid}")
