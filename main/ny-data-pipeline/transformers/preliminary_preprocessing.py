if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd
import numpy as np
@transformer
def transform(df, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """

    columns_to_convert = ['RatecodeID', 'passenger_count', 'fare_amount', 'extra', 
                          'mta_tax', 'tip_amount', 'tolls_amount', 
                          'improvement_surcharge', 'total_amount']
    df[columns_to_convert] = df[columns_to_convert].apply(pd.to_numeric, errors='coerce')

    # Convert datetime columns
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])

    # Calculate trip duration in minutes
    df["duration"] = (df["tpep_dropoff_datetime"] - df["tpep_pickup_datetime"]).dt.total_seconds() / 60

    # Remove outliers using IQR for fare_amount, duration, and passenger_count
    for col_name in ["fare_amount", "duration", "passenger_count"]:
        Q1 = df[col_name].quantile(0.25)
        Q3 = df[col_name].quantile(0.75)
        IQR = Q3 - Q1
        upper_bound = Q3 + 1.5 * IQR
        lower_bound = max(Q1 - 1.5 * IQR, 0)  # Ensure lower bound is non-negative
        df = df[(df[col_name] >= lower_bound) & (df[col_name] <= upper_bound)]

    # Step 2: Feature Engineering
    # Calculate fare per mile
    df['fare_per_mile'] = np.where(df['trip_distance'] > 0, df['fare_amount'] / df['trip_distance'], 0)

    # Categorize trips by distance
    def categorize_distance(distance):
        if distance < 1:
            return "short"
        elif distance < 5:
            return "medium"
        else:
            return "long"

    df['distance_category'] = df['trip_distance'].apply(categorize_distance)

    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
