# Court data analysis
# James Bennett for Code for C-ville

import pandas as pd
import streamlit as st
import plotly.express as px
import json
import streamlit_theme as stt
import urllib

########################## SETTINGS ###################################
st.set_page_config(layout="wide", initial_sidebar_state="expanded")
st.title('A view of court data in Virginia ')
stt.set_theme({'primary': '#1b3388'})


###CENSUS DATA URLS ####
json_url = 'https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json'
pop_url = "https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/asrh/cc-est2019-alldata.csv"


#####CIRCUIT CASES URLS LIST
civ_cir_urls = [
'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fcircuit_civil_2014_anon_00.csv',
'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fcircuit_civil_2015_anon_00.csv',
'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fcircuit_civil_2016_anon_00.csv',
'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fcircuit_civil_2017_anon_00.csv',
'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fcircuit_civil_2018_anon_00.csv',
'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fcircuit_civil_2019_anon_00.csv']
cri_cir_urls = [
'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fcircuit_criminal_2014_anon_00.csv',
'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fcircuit_criminal_2015_anon_00.csv',
'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fcircuit_criminal_2016_anon_00.csv',
'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fcircuit_criminal_2017_anon_00.csv',
'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fcircuit_criminal_2018_anon_00.csv',
'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fcircuit_criminal_2019_anon_00.csv',
]
#####DISTRICT CASES URLS LIST
civ_dist_urls = [
'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_civil_2014_anon_00.csv',
'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_civil_2014_anon_01.csv',
'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_civil_2014_anon_02.csv',
'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_civil_2015_anon_00.csv',
'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_civil_2015_anon_01.csv',
'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_civil_2015_anon_02.csv',
'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_civil_2016_anon_00.csv',
'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_civil_2016_anon_01.csv',
'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_civil_2016_anon_02.csv',
'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_civil_2017_anon_00.csv',
'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_civil_2017_anon_01.csv',
'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_civil_2017_anon_02.csv',
'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_civil_2018_anon_00.csv',
'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_civil_2018_anon_01.csv',
'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_civil_2018_anon_02.csv',
'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_civil_2019_anon_00.csv',
'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_civil_2019_anon_01.csv',
'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_civil_2019_anon_02.csv',
'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_civil_2019_anon_03.csv',
]
cri_dist_urls = [
#'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_criminal_2015_anon_00.csv',
#'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_criminal_2015_anon_01.csv',
#'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_criminal_2015_anon_02.csv',
#'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_criminal_2015_anon_03.csv',
#'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_criminal_2015_anon_04.csv',
#'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_criminal_2015_anon_05.csv',
#'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_criminal_2015_anon_06.csv',
#'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_criminal_2015_anon_07.csv',
#'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_criminal_2016_anon_00.csv',
#'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_criminal_2016_anon_01.csv',
#'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_criminal_2016_anon_02.csv',
#'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_criminal_2016_anon_03.csv',
#'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_criminal_2016_anon_04.csv',
#'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_criminal_2016_anon_05.csv',
#'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_criminal_2016_anon_06.csv',
#'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_criminal_2016_anon_07.csv',
#'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_criminal_2017_anon_00.csv',
#'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_criminal_2017_anon_01.csv',
#'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_criminal_2017_anon_02.csv',
#'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_criminal_2017_anon_03.csv',
#'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_criminal_2017_anon_04.csv',
#'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_criminal_2017_anon_05.csv',
#'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_criminal_2017_anon_06.csv',
#'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_criminal_2017_anon_07.csv',
'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_criminal_2018_anon_00.csv',
'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_criminal_2018_anon_01.csv',
'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_criminal_2018_anon_02.csv',
'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_criminal_2018_anon_03.csv',
'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_criminal_2018_anon_04.csv',
'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_criminal_2018_anon_05.csv',
'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_criminal_2018_anon_06.csv',
'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_criminal_2018_anon_07.csv',
'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_criminal_2019_anon_00.csv',
'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_criminal_2019_anon_01.csv',
'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_criminal_2019_anon_02.csv',
'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_criminal_2019_anon_03.csv',
'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_criminal_2019_anon_04.csv',
'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_criminal_2019_anon_05.csv',
'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_criminal_2019_anon_06.csv',
'https://objectstorage.us-ashburn-1.oraclecloud.com/n/idbllzgo8pgz/b/virginia-court-data-code4cville/o/courtdata%2Fdistrict_criminal_2019_anon_07.csv',

]

#####List of Columns
civ_cir_cols = ['HearingDate', 'HearingResult', 'HearingJury', 'HearingPlea', 'HearingType',
                   'fips', 'Filed', 'Locality', 'Sex', 'Race',
                   'Charge', 'ChargeType', 'Class', 'OffenseDate', 'ArrestDate',
                   'DispositionCode', 'ConcludedBy', 'AmendedCharge', 'AmendedChargeType',
                   'ConcurrentConsecutive', 'LifeDeath', 'SentenceTime', 'SentenceSuspended',
                   'OperatorLicenseSuspensionTime', 'FineAmount', 'Costs', 'FinesCostPaid',
                   'ProbationType', 'ProbationTime', 'ProbationStarts', 'CourtDMVSurrender', 'DriverImprovementClinic',
                   'RestitutionAmount', 'TrafficFatality', 'AppealedDate', 'person_id']

cri_cir_cols = ['HearingDate', 'HearingResult', 'HearingJury', 'HearingPlea', 'HearingType',
                   'fips', 'Filed', 'Locality', 'Sex', 'Race',
                   'Charge', 'ChargeType', 'Class', 'OffenseDate', 'ArrestDate',
                   'DispositionCode', 'ConcludedBy', 'AmendedCharge', 'AmendedChargeType',
                   'ConcurrentConsecutive', 'LifeDeath', 'SentenceTime', 'SentenceSuspended',
                   'OperatorLicenseSuspensionTime', 'FineAmount', 'Costs', 'FinesCostPaid',
                   'ProbationType', 'ProbationTime', 'ProbationStarts', 'CourtDMVSurrender', 'DriverImprovementClinic',
                   'RestitutionAmount', 'TrafficFatality', 'AppealedDate', 'person_id']

civ_dist_cols = ['HearingDate', 'HearingResult', 'HearingPlea', 'HearingType',
                   'fips', 'FiledDate', 'Locality', 'Name', 'Status',
                   'DefenseAttorney', 'Address', 'AKA1', 'AKA2', 'Gender', 'Race', 'DOB', 'Charge', 'CodeSection',
                   'CaseType', 'Class', 'OffenseDate', 'ArrestDate', 'Complainant', 'AmendedCharge', 'AmendedCode',
                   'AmendedCaseType', 'FinalDisposition', 'SentenceTime', 'SentenceSuspendedTime', 'ProbationType',
                   'ProbationTime', 'ProbationStarts',
                   'OperatorLicenseRestrictionCodes', 'Fine', 'Costs', 'FineCostsDue',
                   'FineCostsPaid', 'FineCostsPaidDate', 'VASAP', 'FineCostsPastDue', 'person_id']

cri_dist_cols = ['HearingDate', 'HearingResult', 'HearingPlea', 'HearingType',
                   'fips', 'FiledDate', 'Locality', 'Name', 'Status',
                   'DefenseAttorney', 'Address', 'AKA1', 'AKA2', 'Gender', 'Race', 'DOB', 'Charge', 'CodeSection',
                   'CaseType', 'Class', 'OffenseDate', 'ArrestDate', 'Complainant', 'AmendedCharge', 'AmendedCode',
                   'AmendedCaseType', 'FinalDisposition', 'SentenceTime', 'SentenceSuspendedTime', 'ProbationType',
                   'ProbationTime', 'ProbationStarts',
                   'OperatorLicenseRestrictionCodes', 'Fine', 'Costs', 'FineCostsDue',
                   'FineCostsPaid', 'FineCostsPaidDate', 'VASAP', 'FineCostsPastDue', 'person_id']

@st.cache(persist=True)
def load_data(folder):
    frame_list = []

    if folder == 'data_civil_circuit':
        columns = civ_cir_cols
        urls = civ_cir_urls
    elif folder =='data_criminal_circuit':
        columns = cri_cir_cols
        urls = cri_cir_urls
    elif folder == 'data_civil_district':
        columns = civ_dist_cols
        urls = civ_dist_urls
    elif folder == 'data_criminal_district':
        columns = cri_dist_cols
        urls = cri_dist_urls


    for url in urls:
        df1 = pd.read_csv(url, sep=",")
        df = df1[:]
        frame_list.append(df)

    df = pd.concat(frame_list, ignore_index=True)
    df.fips = "51" + df.fips.astype(str).str.zfill(3)

    ###CLEAN SOME DATA
    if folder == 'data_civil_circuit' or folder == 'data_criminal_circuit':
        df.Race.replace(['White Caucasian (Non-Hispanic)', 'Black (Non-Hispanic)', 'American Indian', 'Unknown'],
                        ['White', 'Black', 'American Indian Or Alaskan Native',
                         'Other (Includes Not Applicable, Unknown)'], inplace=True)
    elif folder == 'data_civil_district' or folder == 'data_criminal_district':
        df.Race.replace(['White Caucasian(Non-Hispanic)', 'Black(Non-Hispanic)',
                         'Unknown (Includes Not Applicable, Unknown)', 'Unknown',
                         'American Indian or Alaskan Native',
                         'Asian or Pacific Islander', 'American Indian'],
                        ['White', 'Black',
                         'Other(Includes Not Applicable, Unknown)', 'Other(Includes Not Applicable, Unknown)',
                         'American Indian Or Alaskan Native', 'Asian Or Pacific Islander',
                         'American Indian Or Alaskan Native'],
                          inplace=True)
    df.SentenceTime = df['SentenceTime'].fillna(0)
    ############################################################################################################
    return df

def map_data(df, va_census, option):

    if option == 'Circuit Civil' or option == 'Circuit Criminal':
        charge = st.sidebar.selectbox("Select the charge type", df.ChargeType.unique())
        df = df.loc[df.ChargeType == charge]
    elif option == "District Civil" or option == 'District Criminal':
        charge = st.sidebar.selectbox("Select the Case type", df.CaseType.unique())
        df = df.loc[df.CaseType == charge]

    county_pop = va_census[va_census.AGEGRP == 0].set_index('fips')['TOT_POP'].to_dict()

    fips_counts = df['fips'].value_counts().reset_index()
    fips_counts.columns = ['fips', 'counts']

    dfw = df.loc[df.Race == "White"]
    w_fips_counts = dfw['fips'].value_counts().reset_index()
    w_fips_counts.columns = ['fips', 'counts']

    dfb = df.loc[df.Race == "Black"]
    b_fips_counts = dfb['fips'].value_counts().reset_index()
    b_fips_counts.columns = ['fips', 'counts']

    # fips_counts["counts_per_100k"] = fips_counts.apply(lambda row: row.counts / (county_pop[row.fips] / 100000), axis=1)

    response = urllib.request.urlopen(json_url)
    counties = json.loads(response.read())

    ranker = px.choropleth(fips_counts, geojson=counties, locations='fips', color='counts',
                           color_continuous_scale='Viridis',
                           scope='usa',
                           range_color=[0, df.shape[0] / 100],
                           width=500,
                           height=500,
                           basemap_visible=False,
                           labels={'counts_per_100k': 'Cases per 100K'})

    ranker.update_geos(fitbounds="locations", visible=False)
    ranker.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    ranker.update_layout(coloraxis_colorbar=dict(
                         thicknessmode="pixels", thickness=10,
                         lenmode="pixels", len=150,
                         yanchor="top", y=0.8,
                         ticks="outside", ticksuffix=" %",
                         dtick=5, bgcolor='rgba(0,0,0,0)'
                                                )
                        )

    w_ranker = px.choropleth(w_fips_counts, geojson=counties, locations='fips', color='counts',
                             color_continuous_scale='Viridis',
                             scope='usa',
                             range_color=[0, df.shape[0] / 100],
                             width=500,
                             height=500,
                             labels={'counts_per_100k': 'Cases per 100K'})

    w_ranker.update_geos(fitbounds="locations", visible=False)
    w_ranker.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    w_ranker.update_layout(coloraxis_colorbar=dict(
        thicknessmode="pixels", thickness=10,
        lenmode="pixels", len=150,
        yanchor="top", y=0.8,
        ticks="outside", ticksuffix=" %",
        dtick=5
    ))
    b_ranker = px.choropleth(b_fips_counts, geojson=counties, locations='fips', color='counts',
                             color_continuous_scale='Viridis',
                             scope='usa',
                             range_color=[0, df.shape[0] / 100],
                             width=500,
                             height=500,
                             labels={'counts_per_100k': 'Cases per 100K'})

    b_ranker.update_geos(fitbounds="locations", visible=False)
    b_ranker.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    b_ranker.update_layout(coloraxis_colorbar=dict(
        thicknessmode="pixels", thickness=10,
        lenmode="pixels", len=150,
        yanchor="top", y=0.8,
        ticks="outside", ticksuffix=" %",
        dtick=5
    ))

    c1, c2, c3 = st.beta_columns((1, 1, 1))
    with c3:
        st.title("Total # of cases")
        st.plotly_chart(ranker)
    with c2:
        st.title("Black - Not Latino")
        st.plotly_chart(b_ranker)
    with c1:
        st.title("White Caucasian")
        st.plotly_chart(w_ranker)
    tabla = df.groupby('Race')['person_id'].nunique()
    df_tabla = pd.DataFrame([tabla]).T

    total = df_tabla.sum()
    df_tabla['Percentage'] = df_tabla/total
    df_tabla['pop'] = [42678,597486,1698568,836481,273137, 5223737]
    pop_total = df_tabla['pop'].sum()
    df_tabla['Percent_pop'] = df_tabla['pop']/pop_total
    df_tabla.rename(columns={'person_id': 'Count_per'}, inplace= True)
    st.table(df_tabla)

def main():

    #####Cencus Data#####
    va_census = pd.read_csv(pop_url, encoding="latin-1", dtype={"COUNTY": str, "STATE": str})
    va_census = va_census[va_census["STATE"] == 51]
    va_census.COUNTY = va_census.COUNTY.astype(str).str.zfill(3)
    va_census = va_census[va_census.YEAR >= 15]
    va_census['fips'] = va_census.STATE + va_census.COUNTY
    ################################################

    menu = ["Home", "Circuit Criminal", "District Criminal", "About"]
    st.sidebar.subheader("Select Option")
    choice = st.sidebar.selectbox("Court", menu)

    if choice == 'Home':
        st.subheader('Home')
    elif choice == 'Circuit Civil':
        civ_cir_df = load_data('data_civil_circuit')
        map_data(civ_cir_df, va_census, choice)
        st.write("""***""")
    elif choice == 'Circuit Criminal':
        cri_cir_df = load_data('data_criminal_circuit')
        map_data(cri_cir_df, va_census, choice)
        st.write("""***""")
    elif choice == 'District Civil':
        civ_dist_df = load_data('data_civil_district')
        map_data(civ_dist_df, va_census,choice)
        st.write("""***""")
    elif choice == 'District Criminal':
        cri_dist_df = load_data('data_criminal_district')
        map_data(cri_dist_df, va_census,choice)
        st.write("""***""")

    elif choice == 'About':
        st.subheader(choice)
        st.write('This Page is under Construction')
    else:
        st.error('Something is wrong')

if __name__ == '__main__':
    main()