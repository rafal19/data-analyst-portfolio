import pandas as pd
from bs4 import BeautifulSoup # this module helps in web scrapping.
import requests
from collections import defaultdict
import time

passing_headers = ['Player','Nation','Position','Age','90s','Pass_TotalCmp','Pass_TotalAtt','Pass_TotalCmp%','Pass_TotDist','Pass_TotalPrgDist','Pass_ShortCmp','Pass_ShortAtt','Pass_ShortCmp%','Pass_MediumCmp',
'Pass_MediumAtt', 'Pass_MediumCmp%','Pass_LongCmp','Pass_LongAtt','Pass_LongCmp%','Pass_Ast','Pass_xAG','Pass_xA','Pass_A-xAG','Pass_KP','Pass_1/3','Pass_PPA','Pass_CrsPA','Pass_PrgP','Matches']

passes_type_headers = ['Player','Nation','Position','Age','90s','PT_PassesAttempted','PT_Live','PT_Dead','PT_FK','PT_TB','PT_Sw','PT_Crs','PT_TI','PT_CK',
                       'PT_In','PT_Out','PT_Str','PT_PassesCompleted','PT_Off','PT_Blocks','Matches']

gca_headers = ['Player','Nation','Position','Age','90s','SCA','SCA90','SCA_PassLive', 'SCA_PassDead','SCA_TO','SCA_Sh','SCA_Fld'
               ,'SCA_Def', 'GCA','GCA90','GCA_PassLive', 'GCA_PassDead','GCA_TO','GCA_Sh','GCA_Fld','GCA_Def','Matches']


shooting_headers = ['Player','Nation','Position','Age','90s','Shoot_Gls','Shoot_Sh','Shoot_SoT','Shoot_SoT%','Shoot_Sh/90','Shoot_SoT/90','Shoot_G/Sh',
                            'Shoot_G/SoT','Shoot_Dist','Shoot_FK','Shoot_PK','Shoot_PKatt','Shoot_xG','Shoot_npxG','Shoot_npxG/Sh','Shoot_G-xG',
                            'Shoot_np:G-xG','Matches']

defence_actions_headers = ['Player','Nation','Position','Age','90s','Def_Tkl','Def_TklW','Def_Def3rd','Def_Mid3rd','Def_Att3rd','Def_Tkl_chal','Def_Att',
                           'Def_Tkl%','Def_Lost','Def_Blocks','Def_Sh','Def_Pass','Def_Int','Def_Tkl+Int','Def_Clr','Def_Err','Matches']

possesion_headers = ['Player','Nation','Position','Age','90s','Poss_Touches','Poss_DefPen','Poss_Def3rd','Poss_Mid3rd','Poss_Att3rd','Poss_AttPen','Poss_Live-ball',
                     'Poss_TakeonsAtt','Poss_TakeonsSucc','Poss_TakeonsSucc%','Poss_TakeonsTkld','Poss_TakeonsTkld%','Poss_Carries','Poss_ToDist','Poss_PrgDist','Poss_Prgc','Poss_1/3','Poss_CPA','Poss_Mis','Poss_Dis','Poss_Rec',
                     'Poss_PrgR','Matches']

playing_time_headers = ['Player','Nation','Position','Age','play_time_MP','play_time_Min','play_time_Mn/MP','play_time_Min%','90s','play_time_Starts','play_time_Mn/Start','play_time_Compl','play_time_Subs',
                        'play_time_Mn/Sub','play_time_unSub','play_time_PPM','play_time_onG','play_time_onGA','play_time_plus/minus','play_time_plus/minus90','play_time_OnOff','play_time_onxG','play_time_onxGA','play_time_xGplus/minus','play_time_xGplus/minus90','play_time_xG_On-Off','Matches']


stats_misc_headers = ['Player','Nation','Position','Age','90s','Misc_CrdY','Misc_CrdR','Misc_2CrdY','Misc_Fls','Misc_Fld','Misc_Off','Misc_Crs','Misc_Int',
                      'Misc_Tklw','Misc_PKwon','Misc_PKcon','Misc_OG','Misc_Recov','Misc_Won','Misc_Lost','Misc_Won%','Matches']



def create_table(names_of_columns):
    df  = pd.DataFrame(columns=names_of_columns)
    df['club'] = ''

    return df
    


def get_passing_soup(soup):
    return soup.find('div', attrs = {'class' : 'table_container tabbed current', 'id':'div_stats_passing_9'}) 

def get_passing_type_soup(soup):
    return soup.find("div", attrs = {"class" : "table_wrapper tabbed", "id":"all_stats_passing_types"})  

def get_shooting_soup(soup):
    return soup.find('div', attrs = {"class":"table_container tabbed current","id":"div_stats_shooting_9"}) 

def get_possesion_soup(soup):
    return soup.find('div', attrs = {"class":"table_container tabbed current" ,"id":"div_stats_possession_9"})

def get_playing_time_soup(soup):
    return soup.find('div', attrs = {"class":"table_container tabbed current" ,"id":"div_stats_playing_time_9"})  

def get_stats_misc_soup(soup):
    return soup.find('div', attrs = {"class":"table_container tabbed current" ,"id":"div_stats_misc_9"})  

def get_defense_soup(soup):
    return soup.find('div', attrs = {"class":"table_container tabbed current","id":"div_stats_defense_9"})

def get_gca_soup(soup):
    return soup.find('div', attrs = {'class':'table_container tabbed current' ,'id':'div_stats_gca_9'})


#collecting data
def export_csv_data(urls,fdict,choice):
    lst = []
    data_lst = []
    for i in choice:
        for url in urls:
            #needed in full version of program but unavaiable due of limitation of requests from fbref.com website
            time.sleep(3)
            data  = requests.get(url).text 
            soup = BeautifulSoup(data,"html5lib")

            #new empty Datatable
            table = fdict[i][2](fdict[i][3])
            #Seperated HTML code
            web = fdict[i][0](soup)
            #extracting data
            club_data= fdict[i][1](table,web,url)
            cleaned_data = data_cleaning(club_data)
            lst.append(i)
            data_lst.append(cleaned_data)
        zip_data = zip(lst,data_lst)
    table_result = []
    my_dict = defaultdict(list)
    #sorting datatables by chosen options
    for k, v in zip_data:
        my_dict[k].append(v)
    for i in my_dict:
        #concatenating by chosen options
        result = pd.concat(my_dict[i])
        table_result.append(result)
    #joing set of datasets in one dataset
    data = pd.concat(table_result,axis=1)
    return data

                   
        
def get_passing_data(passing_df,table,url):
    players_info = table.find('tbody').find_all('tr')
    for data in players_info:
        full_name = data.find_all("th")
        details= data.find_all("td")
        player = full_name[0].text
        nation = details[0].text
        position = details[1].text      
        age = details[2].text 
        ninety90 = details[3].text 
        TotalCmp = details[4].text 
        TotalAtt = details[5].text 
        TotalCmpPer = details[6].text 
        ToDist = details[7].text 
        TotalPrgDist  = details[8].text 
        ShortCmp  = details[9].text 
        ShortAtt = details[10].text 
        ShortCmpPer = details[11].text 
        MediumCmp = details[12].text 
        MediumAtt  = details[13].text
        MediumCmpPer = details[14].text 
        LongCmp  = details[15].text 
        LongAtt = details[16].text 
        LongCmpPer = details[17].text 
        Ast = details[18].text 
        xAG = details[19].text 
        xA = details[20].text 
        AxAG = details[21].text 
        KP= details[22].text 
        onethird = details[23].text 
        PPA = details[24].text 
        CrsPA = details[25].text 
        PrgP = details[26].text 
        Matches = details[27].text
        club = url[url.rfind('/')+1:url.find('-Stats')]


        passing_df = passing_df._append({'Player': player,'Nation':nation,'Position':position, 'Age':age, '90s':ninety90,
        'Pass_TotalCmp':TotalCmp, 'Pass_TotalAtt':TotalAtt, 'Pass_TotalCmp%': TotalCmpPer,'Pass_TotDist':ToDist,'Pass_TotalPrgDist':TotalPrgDist,
        'Pass_ShortCmp':ShortCmp,'Pass_ShortAtt':ShortAtt, 'Pass_ShortCmp%':ShortCmpPer,'Pass_MediumCmp':MediumCmp,'Pass_MediumAtt':MediumAtt,
        'Pass_MediumCmp%':MediumCmpPer,'Pass_LongCmp':LongCmp, 'Pass_LongAtt':LongAtt,'Pass_LongCmp%':LongCmpPer,'Pass_Ast':Ast,'Pass_xAG':xAG,
        'Pass_xA':xA, 'Pass_A-xAG':AxAG,'Pass_KP':KP,'Pass_1/3':onethird,'Pass_PPA':PPA,'Pass_CrsPA':CrsPA,'Pass_PrgP':PrgP,'Matches':Matches,'club':club},ignore_index=True)
        
    return passing_df

def get_passing_type_data(df,table,url):
    players_passes_type_info = table.find('tbody').find_all('tr')
    for data in players_passes_type_info:
        full_name = data.find_all("th")
        details= data.find_all("td")
        player = full_name[0].text
        nation = details[0].text
        position = details[1].text      
        age = details[2].text 
        ninety90 = details[3].text 
        PassesAttempted = details[4].text 
        Live = details[5].text 
        Dead = details[6].text 
        FK = details[7].text 
        TB  = details[8].text 
        Sw  = details[9].text 
        Crs = details[10].text 
        TI = details[11].text 
        CK = details[12].text 
        In  = details[13].text
        Out = details[14].text 
        Str  = details[15].text 
        PassesCompleted = details[16].text 
        Off = details[17].text 
        Blocks = details[18].text 
        Matches = details[19].text
        club = url[url.rfind('/')+1:url.find('-Stats')]


        df = df._append({'Player': player,'Nation':nation,'Position':position, 'Age':age, '90s':ninety90,
        'PT_PassesAttempted': PassesAttempted, 'PT_Live': Live, 'PT_Dead': Dead,'PT_FK':FK,'PT_TB':TB,
        'PT_Sw':Sw,'PT_Crs':Crs, 'PT_TI':TI,'PT_CK':CK,'PT_In':In,'PT_Out':Out,'PT_Str': Str, 'PT_PassesCompleted':PassesCompleted,'PT_Off':Off,'PT_Blocks':Blocks,'Matches':Matches,'club':club},ignore_index=True)

    return df


def get_gsc_data(df,table,url):
    gsc_info = table.find('tbody').find_all('tr')
    for data in gsc_info:
        full_name = data.find_all("th")
        details= data.find_all("td")
        player = full_name[0].text
        nation = details[0].text
        position = details[1].text      
        age = details[2].text 
        ninety90 = details[3].text 
        SCA = details[4].text 
        SCA_90 = details[5].text 
        SCA_PassLive  = details[6].text 
        SCA_PassDead = details[7].text 
        SCA_TO = details[8].text 
        SCA_Sh  = details[9].text 
        SCA_Fld  = details[10].text 
        SCA_Def = details[11].text 
        GCA  = details[12].text 
        GCA90 = details[13].text 
        GCA_PassLive  = details[14].text
        GCA_PassDead = details[15].text 
        GCA_TO  = details[16].text 
        GCA_Sh = details[17].text 
        GCA_Fld = details[18].text 
        GCA_Def = details[19].text
        Matches = details[20].text
        club = url[url.rfind('/')+1:url.find('-Stats')]
        df = df._append({'Player': player,'Nation':nation,'Position':position, 'Age':age, '90s':ninety90,
        'SCA':SCA, 'SCA90':SCA_90, 'SCA_PassLive': SCA_PassLive, 'SCA_PassDead': SCA_PassDead,'SCA_TO':SCA_TO,'SCA_Sh':SCA_Sh,
        'SCA_Fld':SCA_Fld,'SCA_Def':SCA_Def, 'GCA':GCA,'GCA90':GCA90,'GCA_PassLive':GCA_PassLive,'GCA_PassDead':GCA_PassDead,'GCA_TO':GCA_TO, 'GCA_Sh':GCA_Sh,'GCA_Fld':GCA_Fld,'GCA_Def':GCA_Def,'Matches':Matches,'club':club},ignore_index=True)

    return df

def get_shooting_data(df,table,url):
    shooting_info = table.find('tbody').find_all('tr')
    for data in shooting_info:
        full_name = data.find_all("th")
        details= data.find_all("td")
        player = full_name[0].text
        nation = details[0].text
        position = details[1].text      
        age = details[2].text 
        ninety90 = details[3].text 
        Gls = details[4].text 
        Sh  = details[5].text 
        SoT = details[6].text 
        SoTPer = details[7].text 
        ShPer90  = details[8].text 
        SoTPer90  = details[9].text 
        G_Sh = details[10].text 
        G_SoT = details[11].text
        Dist  = details[12].text 
        FK = details[13].text 
        PK  = details[14].text
        PKatt  = details[15].text
        xG = details[16].text 
        npxG = details[17].text 
        npxG_Sh = details[18].text 
        GoalminusxG = details[19].text 
        npGoalminusxG = details[20].text
        Matches = details[21].text
        club = url[url.rfind('/')+1:url.find('-Stats')]

        
        df= df._append({'Player': player,'Nation':nation,'Position':position, 'Age':age, '90s':ninety90,
        'Shoot_Gls':Gls, 'Shoot_Sh':Sh, 'Shoot_SoT': SoT,'Shoot_SoT%':SoTPer,'Shoot_Sh/90':ShPer90, 'Shoot_SoT/90':SoTPer90,
        'Shoot_G/Sh':G_Sh,'Shoot_G/SoT':G_SoT, 'Shoot_Dist':Dist,'Shoot_FK':FK,'Shoot_PK':PK,'Shoot_PKatt':PKatt,'Shoot_xG':xG,
        'Shoot_npxG':npxG, 'Shoot_npxG/Sh':npxG_Sh,'Shoot_G-xG':GoalminusxG,'Shoot_np:G-xG':npGoalminusxG,'Matches':Matches,'club':club},ignore_index=True)

    return df
        

def get_def_actions_data(df,table,url):
    def_action_info = table.find('tbody').find_all('tr')
    for data in def_action_info:
        full_name = data.find_all("th")
        details= data.find_all("td")
        player = full_name[0].text
        nation = details[0].text
        position = details[1].text      
        age = details[2].text 
        ninety90 = details[3].text 
        Tkl = details[4].text 
        TklW = details[5].text 
        Def3rd = details[6].text 
        Mid3rd = details[7].text 
        Att3rd  = details[8].text 
        Tkl_chal  = details[9].text 
        Att = details[10].text 
        TklPercent = details[11].text
        Lost  = details[12].text 
        Blocks = details[13].text 
        Sh  = details[14].text
        Pass  = details[15].text
        Int  = details[16].text
        TklplusInt = details[17].text 
        Clr = details[18].text 
        Err = details[19].text 
        club = url[url.rfind('/')+1:url.find('-Stats')]

        
        df = df._append({'Player': player,'Nation':nation,'Position':position, 'Age':age, '90s':ninety90,
        'Def_Tkl':Tkl, 'Def_TklW':TklW, 'Def_Def3rd': Def3rd,'Def_Mid3rd':Mid3rd,'Def_Att3rd':Att3rd, 'Def_Tkl_chal':Tkl_chal,'Def_Att':Att ,'Def_Tkl%':TklPercent, 'Def_Lost':Lost,'Def_Blocks':Blocks,'Def_Sh':Sh,'Def_Pass':Pass,'Def_Int':Int,'Def_Tkl+Int':TklplusInt, 'Def_Clr':Clr,'Def_Err':Err,'club':club},ignore_index=True)

    return df

def get_possesion_data(df,table,url):
    possesion_info = table.find('tbody').find_all('tr')
    for data in possesion_info:
        full_name = data.find_all("th")
        details= data.find_all("td")
        player = full_name[0].text
        nation = details[0].text
        position = details[1].text      
        age = details[2].text 
        ninety90 = details[3].text 
        Touches = details[4].text 
        DefPen = details[5].text 
        Def3rd = details[6].text 
        Mid3rd = details[7].text 
        Att3rd  = details[8].text 
        AttPen  = details[9].text 
        LiveTouches = details[10].text 
        takeons_att = details[11].text
        takeons_succ  = details[12].text 
        takeons_succ_perc = details[13].text 
        takeons_Tkld  = details[14].text
        takeons_Tkld_perc  = details[15].text
        Carries  = details[16].text
        TotDist = details[17].text 
        PrgDist = details[18].text 
        PrgC = details[19].text 
        Onethird = details[20].text
        CPA = details[21].text
        Mis = details[22].text
        Dis = details[23].text
        Rec = details[24].text
        PrgR = details[25].text
        club = url[url.rfind('/')+1:url.find('-Stats')]


        df = df._append({'Player': player,'Nation':nation,'Position':position, 'Age':age, '90s':ninety90,
        'Poss_Touches':Touches, 'Poss_DefPen':DefPen, 'Poss_Def3rd': Def3rd,'Poss_Mid3rd':Mid3rd,'Poss_Att3rd':Att3rd, 'Poss_AttPen':AttPen,
        'Poss_Live-ball':LiveTouches ,'Poss_TakeonsAtt':takeons_att, 'Poss_TakeonsSucc':takeons_succ,'Poss_TakeonsSucc%':takeons_succ_perc,'Poss_TakeonsTkld':takeons_Tkld,'Poss_TakeonsTkld%':takeons_Tkld_perc,'Poss_Carries':Carries,'Poss_ToDist':TotDist,'Poss_PrgDist':PrgDist, 
        'Poss_Prgc':PrgC,'Poss_1/3':Onethird,'Poss_CPA':CPA,'Poss_Mis':Mis,'Poss_Rec':Rec,'Poss_Dis':Dis,'Poss_PrgR':PrgR,'club':club},ignore_index=True)

    return df


def get_playing_time_data(df,table,url):
    playing_time_info = table.find('tbody').find_all('tr')
    for data in playing_time_info:
        full_name = data.find_all("th")
        details= data.find_all("td")
        player = full_name[0].text
        nation = details[0].text
        position = details[1].text      
        age = details[2].text 
        MP = details[3].text 
        Min = details[4].text
        MnMP = details[5].text 
        MinPerc = details[6].text 
        ninenty = details[7].text 
        Starts = details[8].text 
        MnStart  = details[9].text 
        Compl  = details[10].text 
        Subs = details[11].text 
        MnSub = details[12].text
        unSub  = details[13].text 
        PPM = details[14].text 
        onG  = details[15].text
        onGA  = details[16].text
        plusminus  = details[17].text
        plusminninety = details[18].text 
        OnOff = details[19].text 
        onxG = details[20].text 
        onxGA = details[21].text
        xgplusmin = details[22].text
        xgplusminninety = details[23].text
        xgOnOff = details[24].text
        Matches = details[25].text
        club = url[url.rfind('/')+1:url.find('-Stats')]
        
        df = df._append({'Player': player,'Nation':nation,'Position':position, 'Age':age, 'play_time_MP':MP,'play_time_Min':Min,
        'play_time_Mn/MP':MnMP, 'play_time_Min%':MinPerc, '90s': ninenty,'play_time_Starts':Starts,'play_time_Mn/Start':MnStart, 'play_time_Compl':Compl,
        'play_time_Subs':Subs ,'play_time_Mn/Sub':MnSub, 'play_time_unSub':unSub,'play_time_PPM':PPM,'play_time_onG':onG,'play_time_onGA':onGA,'play_time_plus/minus':plusminus,'play_time_plus/minus90':plusminninety,'play_time_OnOff':OnOff, 
        'play_time_onxG':onxG,'play_time_onxGA':onxGA,'play_time_xGplus/minus':xgplusmin,'play_time_xGplus/minus90':xgplusminninety,'play_time_xG_On-Off': xgOnOff,'Matches':Matches,'club':club},ignore_index=True)

    #df.dropna(subset=['play_time_Min','90s'],inplace=True)
    indexAge = df[(df['play_time_MP'] == '0')].index
    df.drop(indexAge , inplace=True)

    return df



def get_stat_misc_data(df,table,url):

    stats_misc_info = table.find('tbody').find_all('tr')
    for data in stats_misc_info:
        full_name = data.find_all("th")
        details= data.find_all("td")
        player = full_name[0].text
        nation = details[0].text
        position = details[1].text      
        age = details[2].text 
        ninety90 = details[3].text 
        CrdY = details[4].text 
        CrdR  = details[5].text 
        secondCrdY = details[6].text 
        Fls = details[7].text 
        Fld  = details[8].text 
        Off  = details[9].text 
        Crs = details[10].text 
        Int = details[11].text
        TklW  = details[12].text 
        PKwon = details[13].text 
        PKcon  = details[14].text
        OG  = details[15].text
        Recov = details[16].text 
        Aearial_Duels_Won = details[17].text 
        Aearial_Duels_Lost = details[18].text 
        Aearial_Duels_WonPercent = details[19].text 
        Matches = details[20].text
        club = url[url.rfind('/')+1:url.find('-Stats')]

        
        df = df._append({'Player': player,'Nation':nation,'Position':position, 'Age':age, '90s':ninety90,
        'Misc_CrdY':CrdY, 'Misc_CrdR':CrdR, 'Misc_2CrdY': secondCrdY,'Misc_Fls':Fls,'Misc_Fld':Fld, 'Misc_Off':Off,'Misc_Crs':Crs,'Misc_Int':Int,'Misc_Tklw':TklW ,'Misc_PKwon':PKwon,'Misc_PKcon':PKcon,'Misc_OG':OG,'Misc_Recov':Recov,'Misc_Won':Aearial_Duels_Won, 'Misc_Lost':Aearial_Duels_Lost,'Misc_Won%':Aearial_Duels_WonPercent,'Matches':Matches,'club':club},ignore_index=True)

    return df
        

def data_cleaning(data):
    data['club'] = [items.replace('-',' ') for items in data['club']]
    data['Nation'] = [items[-3:] for items in data['Nation']]
    data['Age'] = [items[0:2] for items in data['Age']]

    return data

def save_as_csv(df):
    #removing duplicates
    df = df.loc[:,~df.columns.duplicated()].copy()
    #removing useless table
    df.drop(columns=['Matches'],axis=1,inplace=True)
    #removing empty, irrelevant rows (players which have not played any minute this season)
    df.dropna(subset=['Player'],inplace=True)

    filename = input('TYPE FILENAME ')
    return df.to_csv(f'{filename}.csv',encoding='utf-32',index=False)