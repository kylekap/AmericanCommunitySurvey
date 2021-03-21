import config
import requests
import pandas as pd


def acs_readable_headers(var_list=None):
    """Creates a dictionary to replace / update the ACS titles.

    Args:
        theList (dictionary, optional): All possible names for columns to rename, with their real text descriptions to update to

    Returns:
        [dictionary]: Cleaned titles for the dataframe queried from the ACS.
    """

    if var_list == None:
        requests.get(r'https://api.census.gov/data/2018/acs/acs1/variables').json()

    the_dict = {}
    for element in theList:
        a = element[1].replace('Estimate','').replace('!','_').replace('-','_').replace('Total','Total_').replace(' ','_')
        a = a.replace('__','_').replace('__','_')
        if a[0] == '_':
            a=a[1:]
        if a[-1] == '_':
            a=a[:-1]
        the_dict[element[0]]= a

    the_dict = {k: v.lower() for k, v in the_dict.items()}
    the_dict.update({'B01001_001E':'population'})
    return the_dict

def acs_request_data(get_variables, geography="county", rename=False, api_key=config.api_key, url=r'https://api.census.gov/data/2018/acs/acs1'):
    """Get ACS data from the Census datasets.

    Args:
        get_variables (str or list): ACS variables to pull
        geography (str, optional): What level to do the data grouping on. Defaults to "county". https://api.census.gov/data/2013/acs/acs1/geography.html
        rename (bool, optional): Renames all column headers to be more readable. Defaults to False.
        api_key (str): Enter the API key for the census.gov site. Defaults to config.api_key, which is an imported value for this project
        url (str, optional): Determines which ACS version you will be querying. Defaults to the 2018 version of the 1 year results- https://api.census.gov/data/2018/acs/acs1

    Returns:
        [type]: Pandas dataframe of the queried data
    """    

    if type(get_variables) == str:
        varia = get_variables
    elif type(get_variables) == list:
        varia = ",".join(map(str, get_variables))
    else
        return None

    #Get Data
    d = requests.get(url, params={'key': api_key, 'get': 'NAME,'+varia, 'for':f"{geography}:*"}).json()
    
    #Dataframe it
    dfACS = pd.DataFrame(d[1:],columns=d[0])
    list_var = list(get_variables.split(","))
    dfACS[list_var] = dfACS[list_var].apply(pd.to_numeric)


    if(rename):
        #Get readable column headers
        dfACS.rename(columns=acs_readable_headers(), inplace=True)
        dfACS.rename(columns={'NAME':geography},inplace=True)
    return dfACS