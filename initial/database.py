import pandas as pd
from sqlalchemy import create_engine, MetaData
from test import get_rankings

host="champion.cvvdxaeh2ffd.ap-southeast-1.rds.amazonaws.com"
port=3306
dbname="champion"
user="TAP"
password="colacola1"

engine = create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.format(user, password, host, dbname)).connect()
# engine = create_engine('sqlite:///champion.db', echo = True)
meta = MetaData()

# Read the data as a dataframe
team_info = pd.read_csv('test_cases_csv\Test_case_1_info.csv', header=None)
team_results = pd.read_csv('test_cases_csv\Test_case_1_results.csv', header=None)

# Create the table and overwrite if necessary
team_info.to_sql('team_information', con=engine, if_exists='replace', index=False)
team_results.to_sql('team_matches', con=engine, if_exists='replace', index=False)

# Execute to select from the tables and then read them as a dataframe
information = pd.read_sql('SELECT * FROM team_information',con=engine)
matches = pd.read_sql('SELECT * FROM team_matches', con=engine)

print(get_rankings(information, matches))