from bs4 import BeautifulSoup
import requests


def get_single_certifs(interprete: str):
    """ Take a string as argument (artist name) and return a dictionnay with certif names as keys and their values """
    next_page = 1
    or_single = 0
    diamant_single = 0
    platine_single = 0
    is_next_page = True

    while (is_next_page):
    
        r = requests.get(f"https://snepmusique.com/les-certifications/page/{next_page}/?categorie=Singles&order=Artiste%20A-Z&interprete={interprete}")
        soup = BeautifulSoup(r.content, 'html.parser')
        certif_html = soup.find_all("div", class_={"certification":True})
        for occurence in certif_html:

            artist = occurence.find("div", class_={"artiste":True})
            artist = artist.get_text(strip=True) if artist is not None else ""
            artist = artist.split()
            interprete_splitted = interprete.split()

            for word in artist:
                if interprete_splitted[0].lower() == word.lower().strip(','):
                    break
            else:
                continue

            certif = occurence.find("div", class_={"certif":True})
            certif_text = certif.get_text(strip=True).lower() if certif is not None else ""

            if "or" in certif_text:
                or_single +=1
            elif "diamant" in certif_text:
                    diamant_single += 1
            elif "platine" in certif_text:
                    platine_single += 1

        is_next_page = soup.find("div", class_={"next":True})
        next_page += 1
    return {"Or":or_single, "Platine":platine_single, "Diamant":diamant_single}

def get_albums_certifs(interprete: str):

    """ Take a string as argument (artist name) and return a dictionnay with certif names as keys and their values """
    next_page = 1
    is_next_page = True
    or_album = 0
    platine_album = 0
    diamant_album = 0

    while (is_next_page):
        r = requests.get(f"https://snepmusique.com/les-certifications/page/{next_page}/?categorie=Albums&order=Artiste%20A-Z&interprete={interprete}")
        soup = BeautifulSoup(r.content, 'html.parser')
        certif_html = soup.find_all("div", class_={"certification":True})

        for occurence in certif_html:

            artist = occurence.find("div", class_={"artiste":True})
            artist = artist.get_text(strip=True) if artist is not None else ""
            artist = artist.split()
            interprete_splitted = interprete.split()

            for word in artist:
                if interprete_splitted[0].lower() == word.lower().strip(','):
                    break
            else:
                continue

            certif = occurence.find("div", class_={"certif":True})
            certif_text = certif.get_text(strip=True).lower() if certif is not None else ""

            if "or" in certif_text:
                or_album += 1
            elif "double diamant" in certif_text:
                diamant_album += 2
            elif "triple diamant" in certif_text:
                diamant_album += 3
            elif "quadruple diamant" in certif_text:
                diamant_album += 4
            elif "diamant" in certif_text:
                diamant_album += 1
            elif "double platine" in certif_text:
                    platine_album += 2
            elif "triple platine":
                platine_album += 3
            elif "platine" in certif_text:
                platine_album += 1
        
        is_next_page = soup.find("div", class_={"next":True})
        next_page += 1
    return {"Or":or_album, "Platine":platine_album, "Diamant":diamant_album}

def get_total_album_sales(certifs: dict):
    return ((certifs["Or"] * 50000) + (certifs["Platine"] * 100000) + (certifs["Diamant"] * 500000))
    


artist_input = input("Artiste : ")
while len(artist_input) < 2:
    artist_input = input("Artiste : ")
singles_certifs = get_single_certifs(artist_input)
print(f"singles : {singles_certifs}")
albums_certifs = get_albums_certifs(artist_input)
print(f"albums : {albums_certifs}")
print(f"ventes : {get_total_album_sales(albums_certifs)}")