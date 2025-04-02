import pandas as pd, numpy as np, seaborn as sns, matplotlib.pyplot as plt
import re, math
from natsort import natsorted

# Author: [Vigano' Salvatore]
# Date: [04/02/2025]
# Description: This script processes IMDb movie data, handling missing values, sorting, and performing analysis with visualisations.

def read_csv(file_path):
    """
    Reads a CSV file into a pandas DataFrame.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    pandas.DataFrame: The DataFrame if the file is read successfully, otherwise None.
    """
    try:
        df = pd.read_csv(file_path)
        print(f"\nFile successfully loaded from: {file_path}\n")
        return df
    except FileNotFoundError:
        print(f"\nError: file {file_path} not found.\n")
        return None
    except pd.errors.EmptyDataError:
        print("\nError: CSV file is empty.\n")
        return None
    except Exception as e:
        print(f"\nUnexpected error during file reading: {e}\n")
        return None

def convert_duration_to_minutes(duration):
    """
    Converts a duration string (e.g., '2h 30m') to minutes.

    Parameters:
    duration (str or float): The duration string to convert.

    Returns:
    int: The duration in minutes, or 0 in case of error or NaN.
    """
    try:
        if pd.isna(duration):
            return 0  # Return 0 if duration is NaN
        if isinstance(duration, str):
            hours, minutes = 0, 0
            time_parts = re.findall(r'(\d+)(h|m)', duration)  # Find hours and minutes parts
            for value, unit in time_parts:
                if unit == 'h':
                    hours = int(value)
                elif unit == 'm':
                    minutes = int(value)
            return hours * 60 + minutes  # Calculate total minutes
        else:
            return 0  # Return 0 if duration is not a string
    except Exception as e:
        print(f"\nError during duration conversion: {e}\n")
        return 0

def convert_minutes_to_duration_string(minutes):
    """
    Converts minutes to a duration string in 'Xh Ym' format.

    Parameters:
    minutes (int): The duration in minutes.

    Returns:
    str: The duration in 'Xh Ym' format.
    """
    hours = math.floor(minutes / 60)  # Calculate hours
    minutes = round(minutes % 60)  # Calculate remaining minutes
    return f"{hours}h {minutes}m"  # Format and return duration string

def fill_nan_with_mean(df):
    """
    Fills NaN values in 'Rating', 'Votes', and 'Duration' columns with the mean.

    Parameters:
    df (pandas.DataFrame): The DataFrame to process.

    Returns:
    pandas.DataFrame: The processed DataFrame.
    """
    try:
        print("\nNaN values before filling:\n")
        print(df.isnull().sum())  # Print the sum of NaN values in each column

        df['Duration'] = df['Duration'].fillna(0)  # Fill NaN in 'Duration' with 0
        df['Duration_minutes'] = df['Duration'].apply(convert_duration_to_minutes)  # Convert duration to minutes
        mean_duration = df['Duration_minutes'].mean()  # Calculate mean duration in minutes
        df['Duration_minutes'] = df['Duration_minutes'].apply(lambda x: math.ceil(mean_duration) if x == 0 else math.ceil(x))  # Fill 0 duration with mean

        def convert_votes(vote_str):
            """Converts votes to numeric or 'K' format."""
            if pd.isna(vote_str):
                return np.nan  # Return NaN if vote_str is NaN
            if isinstance(vote_str, (int, float)):
                return vote_str  # Return as is if already numeric
            vote_str = str(vote_str).upper()  # Convert to uppercase
            if 'K' in vote_str:
                return float(vote_str.replace('K', '')) * 1000  # Convert 'K' format to numeric
            return float(vote_str)  # Convert to float

        df['Votes'] = df['Votes'].apply(convert_votes)  # Apply vote conversion
        mean_rating = math.ceil(df['Rating'].mean())  # Calculate mean rating
        mean_votes = math.ceil(df['Votes'].mean())  # Calculate mean votes
        df['Rating'] = df['Rating'].fillna(mean_rating)  # Fill NaN in 'Rating' with mean
        df['Votes'] = df['Votes'].fillna(mean_votes)  # Fill NaN in 'Votes' with mean
        df['Duration_string'] = df['Duration_minutes'].apply(convert_minutes_to_duration_string)  # Convert minutes to duration string
        df['Duration'] = df['Duration_string']  # Replace 'Duration' with formatted string
        df.drop(['Duration_string'], axis=1, inplace=True)  # Remove temporary 'Duration_string' column

        print("\nNaN values for 'Rating', 'Votes' and 'Duration' filled with the rounded up mean, 'Duration' overwritten with 'Duration_string', and 'Duration_string' removed.\n")
        return df
    except Exception as e:
        print(f"\nError during NaN value filling: {e}\n")
        return df

def impute_mpa(df):
    """
    Imputes NaN values in the 'MPA' column with 'Not Rated'.

    Parameters:
    df (pandas.DataFrame): The DataFrame to process.

    Returns:
    pandas.DataFrame: The processed DataFrame.
    """
    try:
        df['MPA'] = df['MPA'].fillna('Not Rated')  # Fill NaN in 'MPA' with 'Not Rated'
        df['MPA'] = df['MPA'].replace('Unrated', 'Not Rated')  # Replace 'Unrated' with 'Not Rated'
        print("\nNaN values for 'MPA' filled with 'Not Rated'.\n")
        return df
    except Exception as e:
        print(f"\nError during NaN value imputation for 'MPA': {e}\n")
        return df

def sort_by_title(df):
    """
    Sorts movies by title using natural sorting

    Parameters:
    df (pandas.DataFrame): The DataFrame to process.

    Returns:
    pandas.DataFrame: The sorted DataFrame.
    """
    try:
        def custom_sort_key(title):
            """Custom sort key to prioritize titles with special characters."""
            if re.match(r'^[^A-Za-z0-9\s].*', title):  # Check if title starts with a special character
                return (0, title)  # Place special character titles first
            else:
                return (1, re.sub(r"^\d+\.\s*", "", title).strip())  # Place regular titles after, removing leading numbers

        df['Cleaned Title'] = df['Title'].apply(lambda x: re.sub(r"^\d+\.\s*", "", x).strip())  # Clean titles
        # Sort using natsort for natural sorting, with custom sort key for special characters
        df_sorted = df.iloc[natsorted(df.index, key=lambda x: custom_sort_key(df.loc[x, 'Title']))]
        df_sorted['Title'] = df_sorted['Cleaned Title']  # Replace original titles with cleaned titles
        df_sorted.drop('Cleaned Title', axis=1, inplace=True)  # Remove temporary 'Cleaned Title' column
        return df_sorted
    except KeyError:
        print("\nError: 'Title' column not present in the DataFrame.\n")
        return df
    except Exception as e:
        print(f"\nUnexpected error during sorting by title: {e}\n")
        return df

def count_long_movies(df):
    """
    Counts movies with duration >= 2 hours and removes 'Duration_minutes' column.

    Parameters:
    df (pandas.DataFrame): The DataFrame to process.

    Returns:
    pandas.DataFrame: The DataFrame of movies with duration >= 2 hours.
    """
    try:
        long_movies = df[df['Duration_minutes'] >= 120]  # Filter movies with duration >= 120 minutes
        print(f"\nNumber of movies with duration >= 2h: {len(long_movies)}\n")
        df.drop('Duration_minutes', axis=1, inplace=True)  # Remove 'Duration_minutes' column
        return long_movies
    except KeyError:
        print("\nError: 'Duration_minutes' column not present in the DataFrame.\n")
        return pd.DataFrame()
    except Exception as e:
        print(f"\nError during counting long movies: {e}\n")
        return pd.DataFrame()

def movies_by_mpa(df):
    """
    Shows a table with the total number of movies per MPA.

    Parameters:
    df (pandas.DataFrame): The DataFrame to process.

    Returns:
    pandas.DataFrame: The DataFrame with the count of movies per MPA.
    """
    try:
        mpa_counts = df.groupby('MPA')['Title'].count().reset_index(name='Film Count')  # Count movies per MPA
        print("\nTotal movies for each MPA:\n")
        print(mpa_counts)
        return mpa_counts
    except KeyError:
        print("\nError: 'MPA' column not present in the DataFrame.\n")
        return pd.DataFrame()
    except Exception as e:
        print(f"\nUnexpected error during movie aggregation per MPA: {e}\n")
        return pd.DataFrame()

def movies_with_high_rating(df):
    """
    Shows movies with a rating greater than 7.5.

    Parameters:
    df (pandas.DataFrame): The DataFrame to process.

    Returns:
    pandas.DataFrame: The DataFrame of movies with rating > 7.5.
    """
    try:
        high_rating_movies = df[df['Rating'] > 7.5]  # Filter movies with rating > 7.5
        print(f"\nMovies with a rating greater than 7.5: {len(high_rating_movies)}\n")
        return high_rating_movies
    except Exception as e:
        print(f"\nError during selection of movies with rating greater than 7.5: {e}\n")
        return pd.DataFrame()

def plot_rating_distribution(df):
    """
    Plots the distribution of movie ratings using seaborn.

    Parameters:
    df (pandas.DataFrame): The DataFrame containing movie ratings.

    This function generates a histogram of the movie ratings from the input DataFrame,
    using seaborn's histplot. It also includes a kernel density estimation (KDE) to
    show the distribution curve. The plot is then saved as a PNG file and displayed.
    """
    try:
        plt.figure(figsize=(10, 6))  # Set the figure size
        sns.histplot(df['Rating'], bins=20, kde=True)  # Create the histogram with KDE
        plt.title('Distribution of Movie Ratings')  # Set the plot title
        plt.xlabel('Rating')  # Set the x-axis label
        plt.ylabel('Frequency')  # Set the y-axis label
        plt.savefig('rating_distribution.png')  # Save the plot as a PNG file
        plt.show()  # Display the plot
    except Exception as e:
        print(f"\nError during plotting rating distribution: {e}\n")  # Print error message if any

def main(file_path):
    """
    Main function to execute all data processing tasks and plot the rating distribution.

    Parameters:
    file_path (str): The path to the CSV file.
    """
    try:
        df = read_csv(file_path)  # Read the CSV file
        if df is None:
            return  # Exit if DataFrame is None
        df = fill_nan_with_mean(df)  # Fill NaN values
        df = impute_mpa(df)  # Impute MPA values
        df_sorted = sort_by_title(df)  # Sort movies by title
        count_long_movies(df_sorted)  # Count long movies
        movies_by_mpa(df_sorted)  # Group movies by MPA
        movies_with_high_rating(df_sorted)  # Filter high-rated movies
        df_sorted.to_csv('movies_processed.csv', index=False)  # Save processed DataFrame to CSV
        print("\nFile successfully saved as 'movies_processed.csv'\n")
        print("\nNaN values after filling:\n")
        print(df_sorted.isnull().sum())  # Print NaN values after processing

        plot_rating_distribution(df_sorted)  # Plot rating distribution

    except Exception as e:
        print(f"\nError in script execution: {e}\n")  # Print error during execution

if __name__ == "__main__":
    file_path = "imdb_movies_2024.csv"  # Set the file path
    main(file_path)  # Execute the main function