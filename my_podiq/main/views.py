from django.shortcuts import render, redirect
from requests import post, get
import json
import base64


def index(request):
    global a1, b1, c1, g
    a1=0.5
    b1=0.5
    c1=0
    g='1111111111'
    #print(request.POST)
    if request.method == "POST" and 'slider' in request.POST:
        c1=request.POST['slider']
    if request.method =="POST" and 'name' in request.POST:
        qrt = request.POST['name']
        g=list(map(str, qrt.split(';')))
    if request.method == "POST" and '1' in request.POST:
        a1=request.POST['1']
    if request.method == "POST" and '2' in request.POST:
        b1=request.POST['2']
    data = {
        'title': 'MUSIFYER',
        'values': ['Some', 'Hello', '123'],
        'obj': {
            'car': a1,
            'age': b1,
            'hobby': c1
        },
        'error': ''
    }
    if request.method == "POST" and '6' in request.POST:
        return redirect('about')
    if request.method == 'POST' and '89' in request.POST:
        return render(request, 'main/index.html', data)
    return render(request, 'main/zastavka.html')


def about(request):
    global a1, c1, b1, g


    def get_token():
        auth_string = 'secret_code' + ':' + 'secret+code'
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": "Basic " + auth_base64,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}
        result = post(url, headers=headers, data=data)
        json_result = json.loads(result.content)
        token = json_result["access_token"]
        return token

    def get_auth_header(token):
        return {"Authorization": "Bearer " + token}

    def search_for_artist(token, artist_name):
        url = "https://api.spotify.com/v1/search"
        headers = get_auth_header(token)
        query = f"?q={artist_name}&type=artist&limit=1"

        query_url = url + query
        result = get(query_url, headers=headers)
        json_result = json.loads(result.content)["artists"]["items"]
        return json_result

    def get_songs_by_artist(token, artist_id):
        url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=BY"
        headers = get_auth_header(token)
        result = get(url, headers=headers)
        json_result = json.loads(result.content)["tracks"]
        return json_result

    def song_features(token, song_id):
        url = f"https://api.spotify.com/v1/audio-features/{song_id}"
        headers = get_auth_header(token)
        resuld = get(url, headers=headers)
        json_result = json.loads(resuld.content)
        return json_result

    def album(token, album_id):
        url = f"https://api.spotify.com/v1/albums/{album_id}"
        headers = get_auth_header(token)
        resuld = get(url, headers=headers)
        json_result = json.loads(resuld.content)
        return json_result

    def all(token, artist_id):
        url = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
        headers = get_auth_header(token)
        resuld = get(url, headers=headers)
        json_result = json.loads(resuld.content)
        return json_result

    def molodec(elto):
        return elto[6]

    token = get_token()
    j = g[0:5]
    if len(j)==1:
        ju=3
    elif len(j)>1 and len(j)<=3:
        ju=2
    else:
        ju=1
    #print(request.POST)
    #print(ju)
    #print(j)
    idshki = []
    pesni=''
    albom = ''
    mood = int(c1)/100
    #print(mood, a1, b1)
    b1 = float(b1)
    a1 = float(a1)
    #https://mohithsubbarao.medium.com/moodtape-using-spotify-api-to-create-mood-generated-playlists-6e1244c70892
    for t in range(len(j)):
        if j[t] == '' or j[t][0]==' ':
            data = {
                'title': 'Ошибка',
                'error': 'Неправильно заполена форма, вернитесь на главную страницу'
            }
            return render(request, 'main/error.html', data)
        else:
            result = search_for_artist(token, j[t])
            if result == []:
                data = {
                    'title': 'Ошибка',
                    'error': 'Неправильно заполена форма, вернитесь'
                }
                return render(request, 'main/error.html', data)
            else:
                result = result[0]
                cep = result['name']
                artist_id = result["id"]
                songs = get_songs_by_artist(token, artist_id)
                if songs==[]:
                    data = {
                        'title': 'Ошибка',
                        'error': 'Неправильно заполена форма, вернитесь'
                    }
                    return render(request, 'main/error.html', data)
                album_id = all(token, artist_id)["items"]
                for tutya in range(min(ju,len(songs),len(album_id))):
                    album_id = all(token, artist_id)["items"][tutya]['uri'][14:]
                    ty = album(token, album_id)
                    cu = ty['tracks']['items']
                    if ty['name'] not in albom:
                        albom+=ty['name']
                        for i in range(len(cu)):
                            x = []
                            l1 = (cu[i]['id'])
                            l2 = (cu[i]['name'])
                            if l2 not in pesni:
                                pesni+=l2
                                l3 = (cu[i]['artists'][0]["name"])
                                l4 = (cu[i]['external_urls']['spotify'])
                                if cep not in l3:
                                    l3 = l3 + '(' + cep + ')'
                                u = song_features(token, l1)
                                if 'error' not in u:
                                    d1 = u["valence"]
                                    d2 = u["energy"]
                                    d3 = u["danceability"]
                                    dur = (a1 - d1) ** 2 + (mood - d2) ** 2 + (b1 - d3) ** 2
                                    x.append(l1)
                                    x.append(l2)
                                    x.append(l3)
                                    x.append(d1)
                                    x.append(d2)
                                    x.append(d3)
                                    x.append(dur)
                                    x.append(l4)
                                    idshki.append(x)
                for i in range(len(songs)):
                    x = []
                    l1 = (songs[i]['id'])
                    l2 = (songs[i]['name'])
                    if l2 not in pesni:
                        l3 = (songs[i]['artists'][0]["name"])
                        l4 = (songs[i]['external_urls']['spotify'])
                        if cep not in l3:
                            l3 = l3 + '(' + cep + ')'
                        u = song_features(token, l1)
                        if 'error' not in u:
                            d1 = u["valence"]
                            d2 = u["energy"]
                            d3 = u["danceability"]
                            dur = (mood-d1)**2+(a1-d2)**2+(b1-d3)**2
                            x.append(l1)
                            x.append(l2)
                            x.append(l3)
                            x.append(d1)
                            x.append(d2)
                            x.append(d3)
                            x.append(dur)
                            x.append(l4)
                            idshki.append(x)
    #b1-погода, a1 - день
    #1)valence2)energy3)danceability
    if len(idshki)<10:
        data = {
            'title': 'Ошибка',
            'error': 'Неправильно заполена форма, вернитесь на главную страницу'
        }
        return render(request, 'main/error.html', data)
    idshki.sort(key = molodec)
    #print(idshki)
    datac = {
        'title': 'MUSIFYER',
        'values1': idshki[0][1]+' - by '+idshki[0][2],
        'values2': idshki[1][1] + ' - by ' + idshki[1][2],
        'values3': idshki[2][1] + ' - by ' + idshki[2][2],
        'values4': idshki[3][1] + ' - by ' + idshki[3][2],
        'values5': idshki[4][1] + ' - by ' + idshki[4][2],
        'values6': idshki[5][1] + ' - by ' + idshki[5][2],
        'values7': idshki[6][1] + ' - by ' + idshki[6][2],
        'values8': idshki[7][1] + ' - by ' + idshki[7][2],
        'values9': idshki[8][1] + ' - by ' + idshki[8][2],
        'values10': idshki[9][1] + ' - by ' + idshki[9][2],
        'link1': idshki[0][7],
        'link2': idshki[1][7],
        'link3': idshki[2][7],
        'link4': idshki[3][7],
        'link5': idshki[4][7],
        'link6': idshki[5][7],
        'link7': idshki[6][7],
        'link8': idshki[7][7],
        'link9': idshki[8][7],
        'link10': idshki[9][7],
        'karapuz1': idshki[0][7][:24]+"/embed"+idshki[0][7][24:],
        'karapuz2': idshki[1][7][:24] + "/embed" + idshki[1][7][24:],
        'karapuz3': idshki[2][7][:24] + "/embed" + idshki[2][7][24:],
        'karapuz4': idshki[3][7][:24] + "/embed" + idshki[3][7][24:],
        'karapuz5': idshki[4][7][:24] + "/embed" + idshki[4][7][24:],
        'karapuz6': idshki[5][7][:24] + "/embed" + idshki[5][7][24:],
        'karapuz7': idshki[6][7][:24] + "/embed" + idshki[6][7][24:],
        'karapuz8': idshki[7][7][:24] + "/embed" + idshki[7][7][24:],
        'karapuz9': idshki[8][7][:24] + "/embed" + idshki[8][7][24:],
        'karapuz10': idshki[9][7][:24] + "/embed" + idshki[9][7][24:],
    }
    if request.method == "POST" and 'boba' in request.POST:
        return redirect ('board_home')

    #for idx, song in enumerate(songs):
    #    print(f"{idx + 1}. {song['name']}")

    return render(request, 'main/about.html',datac)
