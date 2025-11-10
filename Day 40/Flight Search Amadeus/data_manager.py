import gspread
import gspread_dataframe
import pandas
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
worksheet = None


class DataManager:

    def __init__(self):
        self.destination_data = {}
        global worksheet

        # Authenticate with Google Sheets using OAuth credentials
        gc = gspread.oauth()

        # Open the Google Sheet by its URL
        sh = gc.open_by_url(
            "https://docs.google.com/spreadsheets/d/1UzRcEOuiXfoKki19ZiWhNCfFhg2gdEk7CjRBh9jhPA0/edit?usp=sharing"
        )

        # Select the worksheet named 'prices' within the Google Sheet
        worksheet = sh.worksheet("prices")

    def get_destination_data(self):
        # Fetch all records from the Google Sheet and convert them into a pandas DataFrame
        dataframe = pandas.DataFrame(worksheet.get_all_records())

        # Convert the DataFrame into a list of dictionaries for easy iteration and data handling
        result = dataframe.to_dict(orient="records")
        self.destination_data = result

        # Return the destination data as a list of dictionaries
        return self.destination_data

    def update_destination_codes(self):
        """
        Update the Google Sheet with the latest IATA codes and lowest prices.

        Converts the in-memory destination data (Python list of dicts)
        back into a DataFrame and overwrites the sheet with new values.
        """
        global worksheet

        # Create a DataFrame with specific columns to ensure correct order and consistency
        dataframe = pandas.DataFrame(
            self.destination_data,
            columns=["City", "IATA Code", "Lowest Price"],
            index=None
        )

        # Overwrite the existing worksheet content with the updated DataFrame
        # include_index=False → avoids writing DataFrame index as a column
        # include_column_header=True → writes column names as headers
        # resize=True → adjusts the sheet size to fit the new data exactly
        gspread_dataframe.set_with_dataframe(
            worksheet,
            dataframe,
            include_index=False,
            include_column_header=True,
            resize=True
        )
