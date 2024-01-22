# Keskustelusovellus

__Sovelluksessa on keskustelupalstoja joille voi tehdä postauksia joita voi kommentoida.
Keskustelupalstoilla on vain otsikko, postauksissa on otsikko ja leipäteksti ja kommenteissa on vain leipäteksti.__

Sovelluksen ominaisuuksia:

* Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
* Käyttäjä näkee sovelluksen etusivulla listan palstoista sekä jokaisen palstan postauksien määrän sekä viimeisimmän postauksen ajankohdan.
* Käyttäjä voi luoda palstalle uuden postauksen antamalla postauksen otsikon ja leipätekstin.
* Käyttäjä voi kirjoittaa kommentin postaukseen.
* Käyttäjä voi muokata luomansa postauksen otsikkoa ja leipätekstiä sekä lähettämänsä kommentin sisältöä. Käyttäjä voi myös poistaa oman postauksen tai kommentin.
* Käyttäjä voi etsiä postaukset, joiden osana on annettu sana, ja joihin hänellä on pääsy.
* Ylläpitäjä voi lisätä ja poistaa keskustelualueita.
* Ylläpitäjä voi luoda yksityisen alueen ja määrittää, keillä käyttäjillä on pääsy yksityisille alueille.
* Ylläpitäjä voi poista ja muokata kaikkea sivun sisältöä.
___
## Käynnistysohjeet
Kloonaa reposition sisältö laitteelle.
```sh
$ git clone git@github.com:levitesuo/Keskustelusovellus.git
```
Liiku juurikansioon.
```sh
$ cd Keskustelusovellus
```
Aloita virtuaaliympäristö.
```sh
$ python3 -m venv venv
$ source venv/bin/activate
```
Lataa riippuvuudet.
```sh
(venv)$ pip install -r requirements.txt
```
Luo juurikansioon .env tiedosto ja lisää sinne seuraavat tiedot.
```sh
DATABASE_URL=<tietokannan-paikallinen-osoite>
SECRET_KEY=<salainen-avain>
```
### Tietokannan alustaminen / tietokanta komennot
Luo pöydät ja lataa teitokantaan esimerkkidataa: (__Suositeltu__)
_Tietokannan pitää olla tyhjä. Esimerkkidata luotu komennolla "dump"_
```sh
$ psql < example_data.sql
```
Luo tyhjät datapöydät tietokantaan.
```sh
$ psql < tables.sql
```
Poista kaikki data tietokannasta.
```sh
$ psql < drop_all.sql
```
### Sovelluksen käynnistys
```sh
(venv)$ flask run
```
___

### Valmis data tietokannassa
Tietokannan pöytien luonnin yhteydessä sinne ladataan ylläpitäjä käyttäjä, jonka käyttäjänimi ja salasana on __admin__.

Jos latasit esimerkkidatan on tietokannassa myös 3 muuta käyttäjää. Joiden salasanat ovat samat kuin käyttäjänimet.

Käyttäjät
* __Käärme__
* __Harry__
* __Zayn__
