import time
from typing import Tuple

import data_validation
import pandas as pd
import requests
from flask import Flask, Response
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    CollectorRegistry,
    Summary,
    generate_latest,
)

app_name = "scraping-service"
app = Flask(app_name)

registry = CollectorRegistry()

num_queries = Summary("get_query", "Get query function")
scrape_metric = Summary("scrape", "Scrape stackoverflow function")


@app.route("/metrics")
def metrics():
    data = generate_latest(registry)
    app.logger.debug(f"Metrics, returning: {data}")
    return Response(data, mimetype=CONTENT_TYPE_LATEST)


def get_query(dateFrom, dateTo, page=1):
    return (
        f"https://api.stackexchange.com/2.3/questions?"
        f"page={page}&"
        f"pagesize=100&"
        f"fromdate={dateFrom}&"
        f"todate={dateTo}&"
        f"order=desc&"
        f"sort=activity&"
        f"site=stackoverflow&"
        f"filter=!Fc7.FlqcJXCgmWba*Q45*UiJ(2"
    )


@num_queries.time()
def execute_query(query) -> Tuple[bool, dict]:
    res = requests.get(query)
    success = False
    if 200 <= res.status_code < 300:
        backoff = res.json().get("backoff", 0)
        if backoff > 0:
            app.logger.debug(f"Waiting for {backoff} seconds before continuing")
            time.sleep(backoff)
        success = True
    else:
        app.logger.debug(f"query got non OK response: {res.status_code = }, {res.json() = }")
    return success, res.json()


@scrape_metric.time()
def scrape_questions_and_save(dateFrom: str, dateTo: str, save_dir=""):
    app.logger.debug("Scrape and save")
    # Request data
    page = 1
    success, response_dict = execute_query(get_query(dateFrom, dateTo, page=page))
    if not success:
        df = pd.DataFrame()
    else:
        items = response_dict["items"]
        while response_dict["has_more"]:
            items.append(response_dict["items"])
            response_dict = requests.get(get_query(dateFrom, dateTo, page=page + 1))

        df = pd.DataFrame(items)

    # transform to dataframe and store as tsv file
    if not df.empty:
        df = df[["title", "tags"]]
        num_anomalies, df = data_validation.remove_anomalies(df)
        if num_anomalies == 0:
            file_name = f"{save_dir}/result_{dateFrom}-{dateTo}.tsv"
            app.logger.debug(f"Saving to {file_name}")
            df.to_csv(file_name, sep="\t", index=False)
            app.logger.debug(f"{len(df)} questions scraped")
        else:
            app.logger.warning("Anomalies found, not saving results")
    else:
        app.logger.info("Dataframe result empty (no questions found)")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)  # nosec
