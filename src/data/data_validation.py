import pandas as pd
import tensorflow_data_validation as tfdv


def validate(filename):
    df_train = pd.read_csv("../../data/raw/train.tsv", sep='\t')
    df_scraped = pd.read_csv("../../data/external/" + filename, sep='\t')

    train_stats = tfdv.generate_statistics_from_dataframe(df_train)
    test_stats = tfdv.generate_statistics_from_dataframe(df_scraped)

    schema = tfdv.infer_schema(train_stats)
    anomalies = tfdv.validate_statistics(statistics=test_stats, schema=schema)
    tfdv.display_anomalies(anomalies)

