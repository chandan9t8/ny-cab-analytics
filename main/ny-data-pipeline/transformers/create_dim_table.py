if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd
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
    # Datetime Dimension Table
    datetime_dim = (
        df[['tpep_pickup_datetime', 'tpep_dropoff_datetime']]
        .drop_duplicates()
        .assign(
            pickup_hour=lambda x: x.tpep_pickup_datetime.dt.hour,
            pickup_day=lambda x: x.tpep_pickup_datetime.dt.day,
            pickup_month=lambda x: x.tpep_pickup_datetime.dt.month,
            pickup_year=lambda x: x.tpep_pickup_datetime.dt.year,
            pickup_weekday=lambda x: x.tpep_pickup_datetime.dt.weekday,
            dropoff_hour=lambda x: x.tpep_dropoff_datetime.dt.hour,
            dropoff_day=lambda x: x.tpep_dropoff_datetime.dt.day,
            dropoff_month=lambda x: x.tpep_dropoff_datetime.dt.month,
            dropoff_year=lambda x: x.tpep_dropoff_datetime.dt.year,
            dropoff_weekday=lambda x: x.tpep_dropoff_datetime.dt.weekday,
        )
        .reset_index(drop=True)
    )
    datetime_dim.insert(0, 'datetime_id', datetime_dim.index)

    # Location Dimension Table (combining pickup and dropoff locations)
    location_dim = (
        pd.concat([
            df[['pickup_longitude', 'pickup_latitude']]
            .rename(columns={'pickup_longitude': 'longitude', 'pickup_latitude': 'latitude'}),
            df[['dropoff_longitude', 'dropoff_latitude']]
            .rename(columns={'dropoff_longitude': 'longitude', 'dropoff_latitude': 'latitude'})
        ])
        .drop_duplicates()
        .reset_index(drop=True)
    )
    location_dim.insert(0, 'location_id', location_dim.index)

    # Rate Code Dimension Table
    rate_code_type = {
        1: "Standard rate",
        2: "JFK",
        3: "Newark",
        4: "Nassau or Westchester",
        5: "Negotiated fare",
        6: "Group ride"
    }
    rate_code_dim = (
        df[['RatecodeID']]
        .drop_duplicates()
        .reset_index(drop=True)
        .assign(rate_code_name=lambda x: x['RatecodeID'].map(rate_code_type))
    )
    rate_code_dim.insert(0, 'rate_code_id', rate_code_dim.index)

    # Passenger Count Dimension Table
    passenger_count_dim = (
        df[['passenger_count']]
        .drop_duplicates()
        .reset_index(drop=True)
    )
    passenger_count_dim.insert(0, 'passenger_count_id', passenger_count_dim.index)

    # Payment Type Dimension Table
    payment_type_name = {
        1: "Credit card",
        2: "Cash",
        3: "No charge",
        4: "Dispute",
        5: "Unknown",
        6: "Voided trip"
    }
    payment_type_dim = (
        df[['payment_type']]
        .drop_duplicates()
        .reset_index(drop=True)
        .assign(payment_type_name=lambda x: x['payment_type'].map(payment_type_name))
    )
    payment_type_dim.insert(0, 'payment_type_id', payment_type_dim.index)

    # Create Fact Table
    fact_table = (
        df.merge(passenger_count_dim, on='passenger_count', how='left')
          .merge(rate_code_dim, on='RatecodeID', how='left')
          .merge(location_dim, left_on=['pickup_longitude', 'pickup_latitude'], 
                 right_on=['longitude', 'latitude'], how='left')
          .rename(columns={'location_id': 'pickup_location_id'})
          .merge(location_dim, left_on=['dropoff_longitude', 'dropoff_latitude'], 
                 right_on=['longitude', 'latitude'], how='left')
          .rename(columns={'location_id': 'dropoff_location_id'})
          .merge(datetime_dim, on=['tpep_pickup_datetime', 'tpep_dropoff_datetime'], how='left')
          .merge(payment_type_dim, on='payment_type', how='left')
          [['VendorID', 'datetime_id', 'passenger_count_id',
            'pickup_location_id', 'dropoff_location_id',
            'rate_code_id', 'payment_type_id',
            'fare_amount', 'extra', 'mta_tax',
            'tip_amount', 'tolls_amount',
            'improvement_surcharge', 'total_amount',
            'trip_distance', 'duration', 
            'fare_per_mile','distance_category']]
    )

    # Return results as dictionaries for loading into BigQuery
    return {
        "datetime_dim": datetime_dim.to_dict(orient="records"),
        "location_dim": location_dim.to_dict(orient="records"),
        "rate_code_dim": rate_code_dim.to_dict(orient="records"),
        "passenger_count_dim": passenger_count_dim.to_dict(orient="records"),
        "payment_type_dim": payment_type_dim.to_dict(orient="records"),
        "fact_table": fact_table.to_dict(orient="records")
    }


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
