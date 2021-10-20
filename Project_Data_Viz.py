#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import streamlit as st

# toutes les fonctions
def get_all_from_year(df, year_string):
    full_date_begin = year_string + '-01-01'
    full_date_ending = year_string + '-12-31'
    mask = (df['endTime'] > full_date_begin) & (df['endTime'] < full_date_ending)
    return df[mask]


def get_when_listen_my_fav_artist(df, name):
    new_df = pd.DataFrame()
    mask = df['trackName'] == name
    new_df = df[mask]
    return new_df

def get_all_song_about_artist(df, name):
    mask = df['artistName'] == name
    return df[mask]

def skip_line(i):
    for j in range(i):
        st.write(" ")
    return

def get_time_from_music_name(df, name):
    mask = df['trackName'] == name
    return df[mask].max()

def get_all_time_by_artist(df, name):
    return int(get_all_song_about_artist(df, name)['msPlayed'].sum() / (1000 * 60 * 60))

def get_name_from_rank_artist(df, i):
    return list(df.items())[i][0]

def artist_regulier(df, value):
    mask = df['trackName'] > value
    return df[mask]



# partie read json history #
dfHistory0 = pd.read_json('./myData/StreamingHistory0.json')
dfHistory1 = pd.read_json('./myData/StreamingHistory1.json')
dfHistory2 = pd.read_json('./myData/StreamingHistory2.json')
dfHistory3 = pd.read_json('./myData/StreamingHistory3.json')

dfHistory = pd.concat([dfHistory0, dfHistory1, dfHistory2, dfHistory3], ignore_index=True)

dfHistory['endTime'] = pd.to_datetime(dfHistory['endTime'])

# fin

st.set_page_config(layout="wide")

dfHistChoice = get_all_from_year(dfHistory, '2021')

time_listen = get_all_from_year(dfHistory, '2021')['msPlayed'].sum()



df_my_fav_artist = dfHistChoice.groupby(['artistName'])['msPlayed'].sum().sort_values(ascending=False)


df_number_music_by_artist = dfHistory.drop(columns=['endTime', 'msPlayed']).drop_duplicates().groupby(['artistName']).count().sort_values(['trackName'], ascending=False)
df_number_music_by_artist.reset_index(inplace=True)

df_my_all_fav_song = dfHistChoice.groupby(['trackName'])['msPlayed'].sum().sort_values(ascending=False)

df_just_track = dfHistChoice['trackName']

df_my_fav_song = dfHistChoice.groupby(['trackName']).count().drop(columns=['artistName', 'msPlayed']).sort_values(by=['endTime'], ascending=False)
df_my_fav_song.reset_index(inplace=True)



# Première partie de la présentation #

col1, col2 = st.columns(2)
with col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Spotify_logo_with_text.svg/1118px-Spotify_logo_with_text.svg.png", width=200)
with col2:
    st.markdown("<h2>🔗 <a href='https://www.linkedin.com/in/arthur-chevron-719abb176/'>Go to my linkedin</a></h2>", unsafe_allow_html=True)

skip_line(4)

# Informations générales #

st.title("My listening information in 2021 👇")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Songs listened to", len(dfHistChoice))
    st.metric("Different pieces", len(dfHistory.drop(columns=['endTime', 'msPlayed']).drop_duplicates()))
with col2:
    st.metric("Listening times", str(int(time_listen / (1000 * 60 * 60))) + "h" + str(int(df_my_all_fav_song[0] / (1000 * 60) % 60)) + "min")
    st.metric("Listening times", str(int(time_listen / (1000 * 60 * 60 * 24))) + "j")
with col3:
    st.metric("Different artists", len(dfHistChoice.groupby(['artistName'])))
    st.metric("Regular artists", len(artist_regulier(df_number_music_by_artist, 9)), 10)


skip_line(8)

# Mon artiste préféré #
st.title("This year, my favourite artist 🦋")
skip_line(1)
#st.write(df_my_fav_artist)

df_all_song_about_my_fav_artist = get_all_song_about_artist(dfHistChoice, list(df_my_fav_artist.items())[0][0])

#st.write(df_all_song_about_my_fav_artist)

df_my_fav_song_about_my_fav_artist = df_all_song_about_my_fav_artist.groupby(['trackName'])['msPlayed'].sum().sort_values(ascending=False)

col1, col2, col3 = st.columns(3)

with col1:
    st.image('https://pbs.twimg.com/media/Elh-s4-XgAA2BJd.jpg', width=300, caption=list(df_my_fav_artist.items())[0][0])
with col2:
    st.metric("Total listening time", str(int(df_my_fav_artist[0] / (1000 * 60 * 60))) + "h" + str(int(df_my_all_fav_song[0] / (1000 * 60) % 60)) + "min")
    st.metric("Different music", len(df_all_song_about_my_fav_artist.groupby(['trackName'])))
with col3:
    st.metric("My favourite music by the artist", list(df_my_fav_song_about_my_fav_artist.items())[0][0])
    st.metric("Time spent listening to my favourite music", str(int(df_my_fav_song_about_my_fav_artist[0] / (1000 * 60))) + "min")
    st.metric("Number of times listened to", len(get_when_listen_my_fav_artist(df_all_song_about_my_fav_artist, list(df_my_fav_song_about_my_fav_artist.items())[0][0] )))

# Mes 5 artistes préférés #
st.title("This year, my 5 favourite artists 🐬")
skip_line(1)
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.image('https://pbs.twimg.com/media/Elh-s4-XgAA2BJd.jpg', width=200, caption=get_name_from_rank_artist(df_my_fav_artist, 0))
    st.metric("Different music", df_number_music_by_artist[df_number_music_by_artist.artistName == get_name_from_rank_artist(df_my_fav_artist, 0)].trackName.item(), str(get_all_time_by_artist(dfHistChoice, get_name_from_rank_artist(df_my_fav_artist, 0))) + 'h')
with col2:
    st.image('./image-1.png', width=200, caption=get_name_from_rank_artist(df_my_fav_artist, 1))
    st.metric("Different music", df_number_music_by_artist[df_number_music_by_artist.artistName == get_name_from_rank_artist(df_my_fav_artist, 1)].trackName.item(), str(int(get_all_song_about_artist(dfHistChoice, list(df_my_fav_artist.items())[1][0])['msPlayed'].sum() / (1000 * 60 * 60))) + 'h')
with col3:
    st.image('./image-2.png', width=200, caption=list(df_my_fav_artist.items())[2][0])
    st.metric("Different music", df_number_music_by_artist[
        df_number_music_by_artist.artistName == list(df_my_fav_artist.items())[2][0]].trackName.item(), str(int(
        get_all_song_about_artist(dfHistChoice, list(df_my_fav_artist.items())[2][0])['msPlayed'].sum() / (
                    1000 * 60 * 60))) + 'h')

with col4:
    st.image('./image-3.png', width=200, caption=list(df_my_fav_artist.items())[3][0])
    st.metric("Different music", df_number_music_by_artist[
        df_number_music_by_artist.artistName == list(df_my_fav_artist.items())[3][0]].trackName.item(), str(int(
        get_all_song_about_artist(dfHistChoice, list(df_my_fav_artist.items())[3][0])['msPlayed'].sum() / (
                    1000 * 60 * 60))) + 'h')
with col5:
    st.image('./image-4.png', width=200, caption=list(df_my_fav_artist.items())[4][0])
    st.metric("Different music", df_number_music_by_artist[
        df_number_music_by_artist.artistName == list(df_my_fav_artist.items())[5][0]].trackName.item(), str(int(
        get_all_song_about_artist(dfHistChoice, list(df_my_fav_artist.items())[5][0])['msPlayed'].sum() / (
                    1000 * 60 * 60))) + 'h')


skip_line(10)
# Mes musiques préférées
st.title("My favourite music 🦄")
skip_line(1)
col1, col2, col3 = st.columns(3)

with col1:
    st.image('https://images-eu.ssl-images-amazon.com/images/I/81ADlEPj9sL._AC_UL600_SR600,600_.jpg', width=300, caption=df_my_fav_song.trackName[0])
with col2:
    st.metric("Total listening time", str(int(df_my_all_fav_song[0] / (1000 * 60 * 60))) + 'h' + str(int(df_my_all_fav_song[0] / (1000 * 60) % 60)) + "min")
    st.metric("Number of times played", int(df_my_fav_song.endTime[0]))
with col3:
    st.metric("Name of the music", df_my_fav_song.trackName[0])
    st.metric("Name of the artist", dfHistChoice[dfHistChoice.trackName == df_my_fav_song.trackName[0]].artistName.iloc[0])


st.title("My other favourite music 🦁")
skip_line(1)
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.image('./tchin.png', width=200, caption=df_my_fav_song.trackName[1])
    st.metric("Number of times played", int(df_my_fav_song.endTime[1]), 2)
with col2:
    st.image('./california.png', width=200, caption=df_my_fav_song.trackName[2])
    st.metric("Number of times played", int(df_my_fav_song.endTime[2]), 3)
with col3:
    st.image('./california.png', width=200, caption=df_my_fav_song.trackName[3])
    st.metric("Number of times played", int(df_my_fav_song.endTime[3]), 4)
with col4:
    st.image('./laylow.png', width=200, caption=df_my_fav_song.trackName[4])
    st.metric("Number of times played", int(df_my_fav_song.endTime[4]), 5)
with col5:
    st.image('./cheddar.png', width=200, caption=df_my_fav_song.trackName[5])
    st.metric("Number of times played", int(df_my_fav_song.endTime[5]), 6)

skip_line(10)
st.title("My listening hours during the day 🕙")
skip_line(1)
dfHistChoice['hour'] = dfHistChoice['endTime'].dt.hour

df_by_hour = dfHistChoice.groupby(['hour']).count()
df_by_hour = df_by_hour.drop(columns=['endTime', 'trackName', 'artistName'])
df_by_hour = df_by_hour.rename(columns={"msPlayed": "timePlayed"})

st.line_chart(df_by_hour)

age = st.slider('Choose a period', 0, 23, (7, 9))



st.title("My favourite music from " + str(age[0]) + "h to " + str(age[1]) + 'h')
df_music_by_hour = dfHistChoice.groupby(['hour', 'trackName', 'artistName']).count()
df_music_by_hour.reset_index(inplace=True)

mask_hour = (df_music_by_hour['hour'] > age[0] - 1) & (df_music_by_hour['hour'] < age[1])
df_music_by_hour = df_music_by_hour[mask_hour]
df_music_by_hour = df_music_by_hour.drop(columns=['endTime'])
df_music_by_hour = df_music_by_hour.rename(columns={"msPlayed": "timePlayed"})

df_add = df_music_by_hour.groupby(['trackName', 'artistName']).sum()
df_add.reset_index(inplace=True)
df_add = df_add.sort_values(['timePlayed'], ascending=False)

max_value = df_add['timePlayed'].max()

def print_my_music(df, i):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Name of the artist", df.artistName.iloc[i])

    with col2:
        st.metric("Name of the music", df.trackName.iloc[i].split("(", len(df.trackName.iloc[i]))[0])

    with col3:
        st.metric("Number of times listened to", str(df.timePlayed.iloc[i]))


for i in range(len(df_add[df_add['timePlayed'] == max_value])):
    print_my_music(df_add[df_add['timePlayed'] == max_value], i)


skip_line(10)

if st.button("🎉"):
    st.balloons()



#st.write(df_music_by_hour[df_music_by_hour['timePlayed'] == max_value].trackName)