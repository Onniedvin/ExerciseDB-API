# Reeniliikehaku (Flask + HTMX)

Projekti hakee harjoitusliikkeitä [**ExerciseDB API**](https://exercisedb-api.vercel.app/docs):sta ja tarjoaa Flask-pohjaisen REST-rajapinnan hakua varten. Tarkoituksena on tehdä myös yksinkertainen HTMX-frontti.

Tavoitteena on tutkia mitä kaikkea tällä rajapinnalla voi tehdä, sillä tämä rupesi kiinnostamaan Hevy -sovellusta käytettyäni.

**update**: API ei enää kehityksessä, joten GIFejä ei saa näkyviin. Joitain muita ominaisuuksia poistuu ehkä myös käytöstä tämän takia.

## Asennus
* Kloonaa repo
* Luo virtuaaliympäristö
```
python -m venv venv
source venv/bin/activate  #Windows: venv\Scripts\activate
```

* Asenna riippuvuudet
```
pip install -r requirements.txt
```
* Käynnistä sovellus
```
python app.py
```