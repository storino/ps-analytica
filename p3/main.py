from flask    import Flask, jsonify, request
from requests import get
from datetime import date

app = Flask(__name__)

#POST endpoint implmentation
@app.route('/age', methods=['POST'])
def age():

    def to_datetime(date_string) -> date:
        date_list = date_string.split("-")
        date_list = list(map(lambda x: int(x), date_list))
        a,m,d = date_list
        return date(a,m,d)

    def format_date(date_string) -> str:
        date_list = date_string.split("-")
        a,m,d = date_list
        return f"{d}/{m}/{a}"

    data = dict(request.get_json())
    name, birth, dateThen = [value for value in data.values()]

    birth_datetime    = to_datetime(birth)
    dateThen_datetime = to_datetime(dateThen)

    ageNow  = (date.today() - birth_datetime).days // 365
    ageThen = (dateThen_datetime - birth_datetime).days // 365

    dateThen = format_date(dateThen)

    quote = f"Olá, {name}! Você tem {ageNow} anos e em {dateThen} você terá {ageThen} anos."
    
    response = {
        "quote": quote,
        "ageNow": ageNow,
        "ageThen": ageThen
    }

    return jsonify(response)

#GET endpoint implementation
@app.get('/album-info')
def album_info():

    def get_latest_album(Albums) -> tuple:
        album_year = 0
        latest_album = ''

        for album in Albums:
            if int(album['intYearReleased']) > album_year:
                album_year   = int(album['intYearReleased'])
                latest_album = album

        return album_year, latest_album

    artist_name = request.args.get('artist')

    artist_info = get(f'http://theaudiodb.com/api/v1/json/2/search.php?s={artist_name}').json()
    artist_id   = artist_info['artists'][0]['idArtist']
    artist_name = artist_info['artists'][0]['strArtist']

    albums_info = get(f'http://theaudiodb.com/api/v1/json/2/album.php?i={artist_id}').json()

    album_year, latest_album  = get_latest_album(albums_info['album'])

    tracks_info = get(f'http://theaudiodb.com/api/v1/json/2/track.php?m={latest_album["idAlbum"]}').json()
    tracks = [tracks_info['track'][i]['strTrack'] for i in range(len(tracks_info['track']))]


    response = {
        "artist": artist_name,
        "latest_album": latest_album['strAlbum'],
        "album_year": album_year,
        "album_tracks": {i: track for i, track in enumerate(tracks)}
    }
    
    return jsonify(response)

app.run()