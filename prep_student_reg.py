"""
Dataprep script which accepts a .csv file of raw student registration data
and appends custom check-in codes using the what3words API.

Then returns four .csv files:
    - student_early_soft.csv - students who are eligible for 9am check-in if they pay DS3 dues, else 10am check-in
    - student_early_hard.csv - students who are eligible for 9am check-in if they pay DS3 dues, else ineligible to attend
    - student_regular.csv - students who are eligible for 10am check-in
    - student_invalid.csv - students who are ineligible to attend
"""

import json
import pandas as pd
import random
import what3words
from tqdm import trange

# w3w geocoder
geocoder = what3words.Geocoder("IFHYTWYY")
starting_cols = [
    "First off, what's your full name?",
    "Hi {{field:479a780b-4131-4583-9519-9736b749a0d4}}, what's your email address?",
    "What year are you?",
    "Which sessions will you be attending?",
    "Are you currently a DS3 Member?",
    "Please upload your resume here.",
    "Are you currently studying for (or already earned) your B.S. or M.S. in Data Science at UCSD?",
    "Submitted At",
    "Token",
]
ending_cols = [
    "full_name",
    "email",
    "year",
    "sessions",
    "ds3_member",
    "resume",
    "ucsd_ds",
    "submitted_at",
    "token",
]


def get_random_w3w():
    """Returns a random what3words address"""
    # Get a random set of coordinates from anywhere in the world
    lat = random.uniform(-90, 90)
    lng = random.uniform(-180, 180)
    # Return the what3words address for those coordinates
    return geocoder.convert_to_3wa(what3words.Coordinates(lat, lng))["words"]


def add_w3w_codes(df):
    """Add a column with w3w address to df."""
    # Get a list of random w3w addresses
    w3w_codes = [get_random_w3w() for _ in trange(len(df))]
    # Ensure that all w3w addresses are unique
    while len(set(w3w_codes)) != len(w3w_codes):
        w3w_codes = [get_random_w3w() for _ in range(len(df))]
    # Add the w3w codes to the dataframe
    df["w3w"] = w3w_codes
    return df


def sort_df(df):
    """Take df and sort it according to the scheme defined at the top of the file."""
    # Get students who are ineligible to attend
    df_invalid = df.query(
        """
        (ucsd_ds == False and (ds3_member == "Yes" or ds3_member == "No, but I'd like to be!") and year == "Graduate Student") or (ucsd_ds == False and ds3_member == "No")
        """
    )
    df_soft_early = df.query(
        """
        (ds3_member == "Yes" or ds3_member == "No, but I'd like to be!") and ucsd_ds == True and year != "Graduate Student"
        """
    )
    df_hard_early = df.query(
        """
        ucsd_ds == False and (ds3_member == "Yes" or ds3_member == "No, but I'd like to be!") and year != "Graduate Student"
        """
    )
    df_regular = df.query(
        """
        (ucsd_ds == True and ds3_member == "No") or (ucsd_ds == True and (ds3_member == "Yes" or ds3_member == "No, but I'd like to be!") and year == "Graduate Student")
        """
    )
    # Save dataframes
    df_invalid.to_csv("reglists/student_invalid.csv", index=False)
    df_soft_early.to_csv("reglists/student_early_soft.csv", index=False)
    df_hard_early.to_csv("reglists/student_early_hard.csv", index=False)
    df_regular.to_csv("reglists/student_regular.csv", index=False)

    # build checkin code lookup dict
    checkin_codes = {}
    dfs = [df_regular, df_soft_early, df_hard_early]
    for code, df in enumerate(dfs):
        for _, row in df.iterrows():
            checkin_codes[row['w3w']] = (row['full_name'], row['email'], row['ds3_member'], row['ucsd_ds'], code)
    
    with open('reglists/checkin_codes.json', 'w') as f:
        json.dump(checkin_codes, f)

    print(
        f"Sorted and saved student registration lists:\n\tInvalid: {len(df_invalid)}\n\tEarly Soft: {len(df_soft_early)}\n\tEarly Hard: {len(df_hard_early)}\n\tRegular: {len(df_regular)}"
    )


def import_df(filename):
    """Import a .csv file and return a dataframe."""
    df = pd.read_csv(filename)
    # Rename the columns to match the scheme defined at the top of the file
    df = df.rename(columns={col: ending_cols[i] for i, col in enumerate(starting_cols)})
    # Convert submitted_at to datetime
    df['submitted_at'] = pd.to_datetime(df.submitted_at)
    # Sort by most recent submission
    df = df.sort_values(by="submitted_at", ascending=False)
    # Deduplicate the dataframe, taking the last entry for each email
    df = df.drop_duplicates(subset="email", keep="first")
    return df


def main():
    FILENAME = "../talentdaystudents_raw_10_7.csv"
    df = import_df(FILENAME)
    print(f"Imported {len(df)} student registrations.")
    df = add_w3w_codes(df)
    print(f"Added w3w codes to {len(df)} student registrations.")
    sort_df(df)
    print("Done!")


if __name__ == "__main__":
    main()
