import time

import data_validation
import pandas as pd
import requests


def get_scraped_questions():
    # Request data
    api_query = "https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&site=stackoverflow&filter=!SlcPR-sfZetz0asIdM"
    response = requests.request(method="GET", url=api_query)

    # transform to dataframe and store as tsv file
    df = pd.DataFrame(response.json()["items"])
    df = df[["title", "tags"]]
    file_name = f"result_{int(time.time())}.tsv"
    df.to_csv(file_name, sep="\t", index=False)
    data_validation.validate(file_name)


if __name__ == "__main__":
    get_scraped_questions()
