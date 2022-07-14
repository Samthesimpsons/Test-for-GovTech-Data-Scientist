from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import pandas as pd
from sqlalchemy import create_engine, MetaData
from test import get_rankings as rankings

app = FastAPI()

engine = create_engine('sqlite:///champion.db', echo = True)
meta = MetaData()

@app.get("/get-rankings/")
def get_rankings():
    team_info = pd.read_csv('test_cases_csv\Test_case_1_info.csv', header=None)
    team_results = pd.read_csv('test_cases_csv\Test_case_1_results.csv', header=None)
    df = rankings(team_info, team_results)

    return HTMLResponse(content=df.to_html(), status_code=200) 

# @app.get("/get-team-info/")
# def get_team_info(multi_line: str):
#     # E.g. str = 'teamA 01/04 1\n teamB 02/04 2\n teamC 03/04 3'
#     # split by newline
#     lines = multi_line.split('\n')
#     # empty dataframe with columns team_name, team_regi_date, group_number
#     df = pd.DataFrame(columns=['team_name', 'team_regi_date', 'group_number'])
#     # loop through each line
#     for line in lines:
#         # split by space
#         line_split = line.split(' ')
#         # append to dataframe
#         df = df.append({'team_name': line_split[0], 'team_regi_date': line_split[1], 'group_number': line_split[2]}, ignore_index=True)
#     return HTMLResponse(content=df.to_html(), status_code=200)  npm -v command

# app post
@app.post("/post-team-info/{multi_line}")
def create_team_info(multi_line: str):
    # E.g. str = 'teamA 01/04 1\n teamB 02/04 2\n teamC 03/04 3'
    # split by newline
    lines = multi_line.split('\n')
    # empty dataframe with columns team_name, team_regi_date, group_number
    df = pd.DataFrame(columns=['team_name', 'team_regi_date', 'group_number'])
    # loop through each line
    for line in lines:
        # split by space
        line_split = line.split(' ')
        # append to dataframe
        df = df.append({'team_name': line_split[0], 'team_regi_date': line_split[1], 'group_number': line_split[2]}, ignore_index=True)
    df.to_sql('team_information', con=engine, if_exists='replace', index=False)
    information = pd.read_sql('SELECT * FROM team_information',con=engine)
    print(information)
    return information

