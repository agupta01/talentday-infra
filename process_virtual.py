import pandas as pd

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

dues_df = pd.read_csv("reglists/venmo_records.csv", header=2)

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

def checkIfPaidDues(name, email, dues_df):
    """Check if the student has paid dues"""
    dues_json = dues_df.to_json()
    return name in dues_json or email in dues_json

def addEmailCode(row):
    """Adds targeting code based on user.
    
    0 - good to go, able to attend (gets link access)
    1 - needs to pay dues before attending
    2 - not eligible to attend
    """
    if row['ucsd_ds'] != 'Yes':
        print("ok")
        return 0
    else:
        if row['year'] != 'Graduate':
            if row['ds3_member'] == 'Yes' or row['ds3_member'] == "No, but I'd like to be!":
                if checkIfPaidDues(row['full_name'], row['email'], dues_df):
                    return 0
                else:
                    return 1
            else:
                return 2 
        else:
            return 2

def main():
    df = import_df("../talentdaystudents_raw_10_11.csv")
    df = df.query("sessions == 'Virtual' or sessions == 'Both'")
    print(f"Found {len(df)} students for virtual session.")
    df['email_code'] = df.apply(addEmailCode, axis=1)
    df.to_csv("reglists/virtual2.csv", index=False)
    print("Classified students and saved to reglists/virtual2.csv. Here's the breakdown:")
    print(df.email_code.value_counts())

if __name__ == "__main__":
    main()