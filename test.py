import pandas as pd

def get_rankings(team_info, team_results):
    # Inititalize dictionaries for each group 1 and 2
    group_1_dict = {
        'team_scores': {},
        'team_goals': {},
        'team_alt_scores': {},
        'team_regi_date': {}}
    group_2_dict = {
        'team_scores': {},
        'team_goals': {},
        'team_alt_scores': {},
        'team_regi_date': {}}

    # Add the teams to their respective dictionaries and initialize the metrics for each team
    for index, row in team_info.iterrows():
        if row[2] == 1:
            group_1_dict['team_regi_date'][row[0]] = row[1]
            group_1_dict['team_scores'][row[0]] = 0
            group_1_dict['team_alt_scores'][row[0]] = 0
            group_1_dict['team_goals'][row[0]] = 0
        elif row[2] == 2:
            group_2_dict['team_regi_date'][row[0]] = row[1]
            group_2_dict['team_scores'][row[0]] = 0
            group_2_dict['team_alt_scores'][row[0]] = 0
            group_2_dict['team_goals'][row[0]] = 0

    # Do our evaluation and score the metrics accordingly
    for i, team in enumerate(team_results[0]):
        # If from team A
        if team in list(group_1_dict['team_scores'].keys()):
            group_1_dict['team_goals'][team_results.iloc[i, 0]] += team_results.iloc[i, 2]
            group_1_dict['team_goals'][team_results.iloc[i, 1]] += team_results.iloc[i, 3]

            if team_results.iloc[i, 2] > team_results.iloc[i, 3]:
                group_1_dict['team_scores'][team_results.iloc[i, 0]] += 3
                group_1_dict['team_alt_scores'][team_results.iloc[i, 0]] += 5
                group_1_dict['team_alt_scores'][team_results.iloc[i, 1]] += 1
            elif team_results.iloc[i, 2] == team_results.iloc[i, 3]:
                group_1_dict['team_scores'][team_results.iloc[i, 0]] += 1
                group_1_dict['team_scores'][team_results.iloc[i, 1]] += 1
                group_1_dict['team_alt_scores'][team_results.iloc[i, 1]] += 3
                group_1_dict['team_alt_scores'][team_results.iloc[i, 0]] += 3
            else:
                group_1_dict['team_scores'][team_results.iloc[i, 1]] += 3
                group_1_dict['team_alt_scores'][team_results.iloc[i, 1]] += 5
                group_1_dict['team_alt_scores'][team_results.iloc[i, 0]] += 1
        elif team in list(group_2_dict['team_scores'].keys()):
            # If from team B
            group_2_dict['team_goals'][team_results.iloc[i, 0]] += team_results.iloc[i, 2]
            group_2_dict['team_goals'][team_results.iloc[i, 1]] += team_results.iloc[i, 3]

            if team_results.iloc[i, 2] > team_results.iloc[i, 3]:
                group_2_dict['team_scores'][team_results.iloc[i, 0]] += 3
                group_2_dict['team_alt_scores'][team_results.iloc[i, 0]] += 5
                group_2_dict['team_alt_scores'][team_results.iloc[i, 1]] += 1
            elif team_results.iloc[i, 2] == team_results.iloc[i, 3]:
                group_2_dict['team_scores'][team_results.iloc[i, 0]] += 1
                group_2_dict['team_scores'][team_results.iloc[i, 1]] += 1
                group_2_dict['team_alt_scores'][team_results.iloc[i, 1]] += 3
                group_2_dict['team_alt_scores'][team_results.iloc[i, 0]] += 3
            else:
                group_2_dict['team_scores'][team_results.iloc[i, 1]] += 3
                group_2_dict['team_alt_scores'][team_results.iloc[i, 1]] += 5
                group_2_dict['team_alt_scores'][team_results.iloc[i, 0]] += 1

    # Order team_scores sub-dict by team_scores, if same score, order by team_goals, if same goals, order by team_alt_scores, if same alt_scores, order by team_regi_date
    group_1_dict['team_scores'] = dict(sorted(group_1_dict['team_scores'].items(), key=lambda x: (x[1], group_1_dict['team_goals'][x[0]], group_1_dict['team_alt_scores'][x[0]], group_1_dict['team_regi_date'][x[0]]), reverse=True))
    group_2_dict['team_scores'] = dict(sorted(group_2_dict['team_scores'].items(), key=lambda x: (x[1], group_2_dict['team_goals'][x[0]], group_2_dict['team_alt_scores'][x[0]], group_2_dict['team_regi_date'][x[0]]), reverse=True))

    # # get the keys of the team_scores dict which is in order of ranking from left to right
    # rankings_A = list(group_1_dict['team_scores'].keys())
    # rankings_B = list(group_2_dict['team_scores'].keys())

    # group_1_dict to dataframe
    group_1_df = pd.DataFrame(group_1_dict)
    group_2_df = pd.DataFrame(group_2_dict)

    # append an ranking column to the dataframe
    group_1_df['ranking'] = range(1, len(group_1_df) + 1)
    group_2_df['ranking'] = range(1, len(group_2_df) + 1)

    # append a next_round yes(if ranking 1 to 4)
    group_1_df['next_round'] = group_1_df['ranking'].apply(lambda x: 'Yes' if x <= 4 else 'No')
    group_2_df['next_round'] = group_2_df['ranking'].apply(lambda x: 'Yes' if x <= 4 else 'No')
    
    print(group_1_df, group_2_df)
    return group_1_df, group_2_df

if __name__ == '__main__':
    # Run our test cases (saved as a csv file) check the output if logic all correct
    for i in range(3): 
        if i == 0:
            team_info = pd.read_csv('test_cases_csv\Test_case_1_info.csv', header=None)
            team_results = pd.read_csv('test_cases_csv\Test_case_1_results.csv', header=None)
            get_rankings(team_info, team_results)
        elif i == 1:
            team_info = pd.read_csv('test_cases_csv\Test_case_2_info.csv', header=None)
            team_results = pd.read_csv('test_cases_csv\Test_case_2_results.csv', header=None)
            get_rankings(team_info, team_results)
        elif i == 2:
            team_info = pd.read_csv('test_cases_csv\Test_case_3_info.csv', header=None)
            team_results = pd.read_csv('test_cases_csv\Test_case_3_results.csv', header=None)
            get_rankings(team_info, team_results)

