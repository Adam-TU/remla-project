import requests
import pandas as pd


def get_scraped_questions():
    # Request data
    api_query = "https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&site=stackoverflow&filter=!SlcPR-sfZetz0asIdM"
    response = requests.request(method="GET", url=api_query)

    # transform to dataframe and store as tsv file
    df = pd.DataFrame(response.json()['items'])
    df = df[['title', 'tags']]
    df.to_csv("result.tsv", sep='\t', index=False)


if __name__ == "__main__":
    get_scraped_questions()
