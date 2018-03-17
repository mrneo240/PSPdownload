import requests

def download_game(g):
    local_filename = g['Name'] + ".pkg"
    # NOTE the stream=True parameter
    r = requests.get(g['PKG direct link'], stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    return local_filename
