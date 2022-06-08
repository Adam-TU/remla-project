import time

import data_validation
import pandas as pd
import requests


def get_scraped_questions(dateFrom: str, dateTo: str):
    # Request data
    # api_query = "https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&site=stackoverflow&filter=!SlcPR-sfZetz0asIdM"
    api_query = f"https://api.stackexchange.com/2.3/questions?fromdate={dateFrom}&todate={dateTo}&order=desc&sort=activity&site=stackoverflow&filter=!Fc7.FlqcJXCgmWba*Q45*UiJ(2"
    response = requests.request(method="GET", url=api_query)

    # transform to dataframe and store as tsv file
    df = pd.DataFrame(response.json()["items"])
    if not df.empty:
        df = df[["title", "tags"]]
        file_name = f"result_{int(time.time())}.tsv"
        df.to_csv(file_name, sep="\t", index=False)
        data_validation.validate(file_name)
        return "200: Questions scraped"
    else:
        return "400: No questions found"


if __name__ == "__main__":
    get_scraped_questions("1653536661", "1653537661")
