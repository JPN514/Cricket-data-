########

#First version of this cricket stats analysis 
#have removed the sensitive info
#only contains clean up and two graphs for the type of dismissal eg. lbw, caught.
#aim is to clean all the individual data frames and make some nice graphs of runs, wickets, economy, boundaries etc.

########


#Python to analyse cricket stats from university
#Will use an excel spreadsheet collected by the club to form a dataframe and graphs

import pandas as pd 
from matplotlib import pyplot as plt
import seaborn as sns

#importing the data in as dataframes and clean up the dataframes

batting_df = pd.read_excel (r'stats', sheet_name='Batting')
del batting_df['MatchID']
#print(batting_df.head())

bowling_table_df = pd.read_excel (r'stats', sheet_name='Bowling Table')
bowling_table_df = bowling_table_df[5:] # cuts the top part away as this is originally a pivot table
headers = bowling_table_df.iloc[0] # gets the correct labels for each column
bowling_table_df  = pd.DataFrame(bowling_table_df.values[1:], columns=headers)
bowling_table_df = bowling_table_df.rename(columns={"Row Labels": "Player"})
#print(bowling_table_df.head(20))

batting_table_df = pd.read_excel (r'stats', sheet_name='Batting Table')
batting_table_df = batting_table_df[5:] # cuts the top part away as this is originally a pivot table
headers = batting_table_df.iloc[0] # gets the correct labels for each column
batting_table_df  = pd.DataFrame(batting_table_df.values[1:], columns=headers)
batting_table_df = batting_table_df.rename(columns={"Row Labels": "Player"})
#print(batting_table_df.head(20))

dismissals_df = pd.read_excel (r'stats', sheet_name='Dismissals')
#dismissals_df.drop(dismissals_df.index[[0,1,2,3,4]],inplace=True)
dismissals_df = dismissals_df[5:] # cuts the top part away as this is originally a pivot table
headers = dismissals_df.iloc[0] # gets the correct labels for each column
dismissals_df  = pd.DataFrame(dismissals_df.values[1:], columns=headers) #recreates the dataframe in the correct format
dismissals_df = dismissals_df.fillna(value=0) #changes blank cells to 0s
del dismissals_df["(blank)"] 
dismissals_df = dismissals_df.rename(columns={"Row Labels" : "Player", "5" : "Index"})
#print(dismissals_df)


#Dismissals graphs:
def dismissals_graphs():
    outs = ["Bowled","Caught","LBW","Not Out","Run Out","Stumped"] #type of dismissal for labelling purposes
    del dismissals_df['Grand Total']
    #print(dismissals_df.columns)
    dismissal_type = dismissals_df.melt(id_vars='Player',value_name='Amount') #repivot the data
    dismissal_type.sort_values(by='Player',ascending=True,inplace=True) #order to get (blank) entries to the top
    dismissal_type = dismissal_type.rename(columns={5 : "Type"}) 
    dismissal_type = dismissal_type[6:] #cuts out the (blank) entries at the top 
    #print(dismissal_type.columns)
    dismissal_type = dismissal_type[dismissal_type.Player != 'Grand Total'] #removes the Grand Total in the player column to avoid double counting all dismissals
    dismissal_count = dismissal_type.groupby('Type').sum() #counts the total for each type of dismissal
    #print(dismissal_type.head(190))
    print(dismissal_count)



 #bar chart to show frequency of each type of dismissal including not outs
    plt.bar(outs,dismissal_count['Amount']) 
    plt.title("Dismissal by type.")
    plt.xlabel("Type of dismissal")
    plt.ylabel("Frequency of dismissal")
    plt.xticks(outs)
    plt.show()
    plt.close()
    
 #pie chart for dismissal percentages including not outs
    explode = (0.1, 0, 0, 0, 0, 0)
    plt.figure(figsize=(5,5))
    plt.title("Dismissal type as a percentage")
    plt.pie(dismissal_count['Amount'],labels=outs,autopct='%1.1f%%',explode=explode,shadow=True)
    plt.show()
    plt.close()





dismissals_graphs()