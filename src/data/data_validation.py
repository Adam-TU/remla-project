import pandas as pd
import tensorflow_data_validation as tfdv
from tensorflow_data_validation.utils.display_util import get_anomalies_dataframe


def validate(filename):
    df_train = pd.read_csv("../../data/raw/train.tsv", sep='\t')
    df_scraped = pd.read_csv("../../data/external/" + filename, sep='\t')
    # df_scraped = pd.read_csv("../../data/external/result_1654101025.tsv", sep='\t')
    # df_scraped = df_scraped.drop(['title'], axis=1)
    train_stats = tfdv.generate_statistics_from_dataframe(df_train)
    test_stats = tfdv.generate_statistics_from_dataframe(df_scraped)

    schema = tfdv.infer_schema(train_stats)
    anomalies = tfdv.validate_statistics(statistics=test_stats, schema=schema)

    df_anomalies = get_anomalies_dataframe(anomalies)

    if df_anomalies.empty:
        print("No anomalies found")
    else:
        for index, row in df_anomalies.iterrows():
            print(f"Feature: {index} has anomaly: '{row[1]}'")

