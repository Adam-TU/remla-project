import pandas as pd
import tensorflow_data_validation as tfdv
from tensorflow_data_validation.utils.display_util import get_anomalies_dataframe


def tensorflow_analysis(filename):
    # df_train = pd.read_csv("../../data/raw/train.tsv", sep='\t')
    # df_scraped = pd.read_csv("../../data/external/" + filename, sep='\t')
    # df_scraped = pd.read_csv("../../data/external/result_1654101025.tsv", sep='\t')
    # df_scraped = df_scraped.drop(['title'], axis=1)
    df_train = pd.read_csv("train.tsv", sep="\t")
    df_scraped = pd.read_csv(filename, sep="\t")
    train_stats = tfdv.generate_statistics_from_dataframe(df_train)
    test_stats = tfdv.generate_statistics_from_dataframe(df_scraped)

    schema = tfdv.infer_schema(train_stats)
    anomalies = tfdv.validate_statistics(statistics=test_stats, schema=schema)

    return get_anomalies_dataframe(anomalies), df_scraped


def remove_anomalies(filename):
    df_anomalies, df_scraped = tensorflow_analysis(filename)

    # In case no anomalies have been found.
    if df_anomalies.empty:
        return 0, df_scraped
    else:
        unresolved_anomalies = 0
        for index, row in df_anomalies.iterrows():
            column_name = index.__str__().replace("\'", "")
            error_message = row[1]
            # print(f"Feature: {column_name} has anomaly: '{error_message}'")

            # Check for the case of additional columns besides question and tags being stored.
            if 'New column' in error_message:
                df_scraped = df_scraped.drop([column_name], axis=1)
            else:
                # For returning anomalies that could not be resolved like questions or tags missing.
                unresolved_anomalies += 1

        return unresolved_anomalies, df_scraped
