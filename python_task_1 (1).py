import pandas as pd


def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    car_values_df = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)

    
    car_values_df.values[[range(len(car_values_df.index))], [range(len(car_values_df.columns))]] = 0

    return car_value_df


def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Add a new categorical column 'car_type'
    df['car_type'] = pd.cut(df['car'], bins=[-float('inf'), 15, 25, float('inf')],
                            labels=['low', 'medium', 'high'], include_lowest=True)

    # Calculate the count of occurrences for each car_type category
    car_type_counts = df['car_type'].value_counts().to_dict()

    # Sort the dictionary alphabetically based on keys
    sorted_car_type_counts = dict(sorted(car_type_counts.items()))

    


    return (sorted_car_type_counts)


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    bus_mean = df['bus'].mean()

    # Find indices where 'bus' values are greater than twice the mean
    indices_greater_than_twice_mean = df.index[df['bus'] > 2 * bus_mean].tolist()

    # Sort the indices in ascending order
    sorted_indices = sorted(indices_greater_than_twice_mean)

    

    return (sorted_indices)


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    filtered_df = df[df['truck'].mean() > 7]

    # Get the sorted list of values from the 'route' column
    sorted_route_values = sorted(filtered_df['route'].tolist())

    

    return (sorted_route_values)


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    car_values_df = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)    
    car_values_df.values[[range(len(car_values_df.index))], [range(len(car_values_df.columns))]] = 0
    def modify_values(value):
        if value > 20:
            return round(value * 0.75, 1)
        else:
            return round(value * 1.25, 1)

    modified_df = car_values_df.applymap(modify_values)
    return matrix


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    def check_completeness(group):
        # Check if the timestamps cover a full 24-hour period and span all 7 days
        valid_hours = set(group['hour']) == set(range(24))
        valid_days = set(group['day_of_week']) == set(range(7))

        # Return True if both conditions are satisfied, indicating completeness
        return pd.Series({'complete': valid_hours and valid_days})

    # Combine date and time columns to create a timestamp column
    df['timestamp'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime']) 

    # Extract day of the week and hour from the timestamp
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    df['hour'] = df['timestamp'].dt.hour

    # Group by id and id_2 and check for completeness
    completeness_check = df.groupby(['id', 'id_2']).apply(check_completeness)

    return completeness_check

