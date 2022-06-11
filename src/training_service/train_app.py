import json
import os
import shutil
import subprocess  # nosec

import yaml
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, Response
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    CollectorRegistry,
    Gauge,
    Summary,
    generate_latest,
    multiprocess,
)

PROMETHEUS_MULTIPROC_DIR = os.environ["PROMETHEUS_MULTIPROC_DIR"]
# make sure the dir is clean
shutil.rmtree(PROMETHEUS_MULTIPROC_DIR, ignore_errors=True)
os.makedirs(PROMETHEUS_MULTIPROC_DIR)

app_name = "training-service"
app = Flask(app_name)
app.logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))

registry = CollectorRegistry()
multiprocess.MultiProcessCollector(registry)

duration_metric = Summary("train_duration", "Time spent on training")
score_metrics = {
    score: Gauge(score, score)
    for score in ["accuracy_score", "f1_score", "avg_precision_score", "roc_auc_score", "num_samples"]
}

scrape_save_dir = os.environ["SCRAPE_SAVE_DIR"]
train_file = f"{os.environ['SHARED_DATA_PATH']}/raw/train.tsv"


def load_yaml_params():
    # Fetch params from yaml params file
    with open("params.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def merge_scraped():
    app.logger.info("Merging scraped files")
    with open(train_file, "a+", encoding="utf-8") as train_f:
        if os.path.exists(scrape_save_dir):
            for scraped_file in os.listdir(scrape_save_dir):
                with open(f"{scrape_save_dir}/{scraped_file}", "r", encoding="utf-8") as scraped:
                    train_f.write(scraped.read())
            shutil.rmtree(scrape_save_dir)
        num_samples = len(train_f.readlines()) - 1

    app.logger.info("Finished merging scraped files")
    return num_samples


@app.route("/train", methods=["POST"])
@duration_metric.time()
def train():
    app.logger.info("Running training")
    num_train_samples = merge_scraped()
    output = subprocess.run(["sh", "src/train.sh"], capture_output=True)  # nosec
    if output.returncode == 0:
        # get scores and update counters
        with open("reports/scores.json", "r") as f:
            scores = json.load(f)
        for score_key in scores:
            score_metrics[score_key].set(scores[score_key])
        score_metrics["num_records"] = num_train_samples
    else:
        app.logger.warning(
            f"train.sh returned non zero exit code: \nstdout:{output.stdout}" f"\n stderr: {output.stderr}"
        )

    app.logger.info("Training finished")


@app.route("/metrics")
def metrics():
    data = generate_latest(registry)
    app.logger.debug(f"Metrics, returning: {data}")
    return Response(data, mimetype=CONTENT_TYPE_LATEST)


cron = BackgroundScheduler(daemon=True)
# Explicitly kick off the background thread
cron.start()

TRAIN_INTERVAL_SECONDS = int(os.environ.get("TRAIN_INTERVAL_SECONDS", 30))
# cron.add_job('training_service.train:train', 'interval', minutes=TRAIN_INTERVAL_MINUTES)
cron.add_job(train, "interval", seconds=TRAIN_INTERVAL_SECONDS)
