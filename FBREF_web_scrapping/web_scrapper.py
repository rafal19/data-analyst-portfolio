import functions

urlss = ['https://fbref.com/en/squads/822bd0ba/Liverpool-Stats','https://fbref.com/en/squads/361ca564/Tottenham-Hotspur-Stats','https://fbref.com/en/squads/18bb7c10/Arsenal-Stats',
         'https://fbref.com/en/squads/8602292d/Aston-Villa-Stats','https://fbref.com/en/squads/b8fd03ef/Manchester-City-Stats','https://fbref.com/en/squads/19538871/Manchester-United-Stats',
         'https://fbref.com/en/squads/b2b47a98/Newcastle-United-Stats','https://fbref.com/en/squads/d07537b9/Brighton-and-Hove-Albion-Stats','https://fbref.com/en/squads/7c21e445/West-Ham-United-Stats',
         'https://fbref.com/en/squads/fd962109/Fulham-Stats','https://fbref.com/en/squads/cd051869/Brentford-Stats','https://fbref.com/en/squads/cff3d9bb/Chelsea-Stats',
         'https://fbref.com/en/squads/8cec06e1/Wolverhampton-Wanderers-Stats','https://fbref.com/en/squads/4ba7cbea/Bournemouth-Stats','https://fbref.com/en/squads/47c64c55/Crystal-Palace-Stats',
         'https://fbref.com/en/squads/e4a775cb/Nottingham-Forest-Stats','https://fbref.com/en/squads/d3fd31cc/Everton-Stats','https://fbref.com/en/squads/e297cd13/Luton-Town-Stats',
         'https://fbref.com/en/squads/943e8050/Burnley-Stats','https://fbref.com/en/squads/1df6b87e/Sheffield-United-Stats']
         

fdict = {'a':[functions.get_passing_soup,functions.get_passing_data,functions.create_table,functions.passing_headers],'b':[functions.get_passing_type_soup,functions.get_passing_type_data,functions.create_table,functions.passes_type_headers],
         'c':[functions.get_shooting_soup,functions.get_shooting_data,functions.create_table,functions.shooting_headers],'d':[functions.get_possesion_soup,functions.get_possesion_data,functions.create_table,functions.possesion_headers],
         'e':[functions.get_playing_time_soup,functions.get_playing_time_data,functions.create_table,functions.playing_time_headers],'f':[functions.get_stats_misc_soup,functions.get_stat_misc_data,functions.create_table,functions.stats_misc_headers],
         'g': [functions.get_defense_soup,functions.get_def_actions_data,functions.create_table,functions.defence_actions_headers],'h': [functions.get_gca_soup,functions.get_gsc_data,functions.create_table,functions.gca_headers]}

options_string = ("Choose parameters to scrape, (type letters seperated space) \n"
    "a - Passing data \n"
    "b - Passing Type data  \n"
    "c - Shooting data  \n"
    "d - Possesion data  \n"
    "e - Playing time data  \n"
    "f - Miscellaneous data  \n"
    "g - Defensive Actions data  \n"
    "h - Goal Shot Creation data  \n"
    )

print(options_string)
options = input('Choose options   ').split(' ')

clubs_string = ("Choose clubs to scrape (type numbers seperated space)\n"
    "1 - Liverpool \n"
    "2 - Tottenham  \n"
    "3 - Arsenal  \n"
    "4 - Aston Villa  \n"
    "5 - Manchester City  \n"
    "6 - Manchester United  \n"
    "7 - Newcastle United  \n"
    "8  Brighton  \n"
    "9-  West Ham \n"
    "10-  Fulham \n"
    "11-  Brendford \n"
    "12-  Chelsea  \n"
    "13-  Wolverhampton  \n"
    "14-  Bournemouth  \n"
    "15-  Crystal Palace  \n"
    "16-  Nottigham Forrest \n"
    "17-  Everton  \n"
    "18-  Luton \n"
    "19-  Burnley  \n"
    "20-  Sheffield United  \n"
    )

print(clubs_string)
clubs = input('Choose club   ').split(' ')

clubs = map(int,clubs)

#deacresing index in order to retrive proper link
urls = [urlss[i-1] for i in clubs]


ready_data = functions.export_csv_data(urls,fdict,options)
functions.save_as_csv(ready_data)

