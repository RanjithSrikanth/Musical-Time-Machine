from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "playlist-modify-private"

client_id = "81420c598f6f479eb31a2c3f4d5e1b56"
client_secret = "de680527426447289d67bd337e438c14"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = client_id,
                                               client_secret= client_secret,
                                               scope= scope,
                                               redirect_uri= "http://example.com",
                                               ))

date = input("Enter the date you want to travel to ? Type the date in YYYY-MM-DD format : ")
# print(date)
URL = f"https://www.billboard.com/charts/hot-100/{date}/"

response = requests.get(URL)
data = response.text

soup = BeautifulSoup(data, 'html.parser')
# print(soup.prettify())
top_100 = soup.find_all(name="h3", class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only")
# print(top_100)
top_100s = [i.getText().strip() for i in top_100]
# print(top_100s)
# for i in top_100s:
#     print(i)
user_name = sp.current_user()["id"]
# print(user_name)

urii = []
for i in top_100s:
    results = sp.search(q=f"track:{i}",type="track")
    # print(results['tracks']['items'][0]['uri'])
    try:
        uri = results["tracks"]["items"][0]["uri"]
        urii.append(uri)
    except IndexError:
        print(f"{i} doesn't exist in Spotify. Skipped.")

# for i in urii:
#     print(i)

playlist = sp.user_playlist_create(user=user_name, name=f"{date} Billiboard 100", public=False)
# print(playlist[id])

sp.playlist_add_items(playlist_id=playlist["id"], items=urii)
