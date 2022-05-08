"""
Projekti: Ohjelma, joka visualisoi kahden erilaisen lajittelualgoritmin
toiminnan. Käyttäjä voi valita kuinka monta "palkkia" haluaa visualisoida 1-50
palkin väliltä. Käyttäjä voi myös valita visualisoinnin nopeuden ja
visualisoitavien palkkien määrän.
Käytettävinä lajittelualgoritmeina ovat bubble sort ja quicksort.
https://en.wikipedia.org/wiki/Bubble_sort
https://en.wikipedia.org/wiki/Quicksort
"""
from tkinter import *
import random
import time
from tkinter import ttk
class Kayttoliittyma:
    def __init__(self):
        self.__paaikkuna = Tk()
        self.__paaikkuna.title("Algoritmin visualisoija")

        self.__paaikkuna.geometry("500x500")
        self.__paaikkuna.resizable(width = False, height = False)

        self.__frame = Frame(self.__paaikkuna, bg = "gray70")
        self.__frame.grid(row = 0, column = 0, sticky = "new")

        self.__palkkien_korkeudet = []

        self.__palkit_listassa = []

        self.__maksimileveys = 500
        self.__maksimikorkeus = 500

        self.__kaikki_jarjestetty = False

        # Lista joka sisältää algoritmit, joita käyttäjä voi visualisoida.
        algoritmit = ["Bubble Sort", "Quicksort"]

        self.__valitse_algoritmi = ttk.Combobox(self.__frame, width = 30,
        values = algoritmit, state = "readonly")
        self.__valitse_algoritmi.grid(row = 0, column = 1, sticky = "S")

        # Asetetaan oletusarvoksi ensimmäinen mahdollinen arvo eli indeksi 0
        # "algoritmit" listasta, tässä tapauksessa Bubble Sort.
        self.__valitse_algoritmi.current(0)

        # Poistetaan valitusta algoritmista sinisen värinen highlight/korostus.
        self.__valitse_algoritmi.bind("<<ComboboxSelected>>", self.poista_focus)

        # Liu'uttimen avulla käyttäjä voi valita kuinka monta palkkia haluaa
        # visualisoida. Mahdolliset arvot ovat välillä 1-50.
        self.__monta_palkkia_on = Scale(self.__frame, length = 100, digits = 2,
        width = 30, from_ = 1, to = 50, resolution = 1, orient = HORIZONTAL,
        bg = "white", command = self.piirra_palkit, label = "Palkkien määrä")
        self.__monta_palkkia_on.grid(row = 0, column = 0, pady = 5)

        # Tämän liu'uttimen avulla käyttäjä voi valita kuinka nopeasti haluaa
        # lajittelun/visualisoinnin tapahtuvan. Tarkemmin ottaen kyseessä on
        # lajittelun viive eli isompi viive = hitaampi lajittelu.
        self.__viive = Scale(self.__frame, length = 100, digits = 2, width = 30,
        from_ = 10, to = 100, resolution = 10, orient = HORIZONTAL,
                                        label = "Viive (ms)", bg = "white")

        self.__viive.grid(row = 1, column = 0, pady = 5)

        self.__jarjestys_nappi = Button(self.__frame, text = "Järjestä",
                                        command = self.valittu_algoritmi)
        self.__jarjestys_nappi.grid(row = 0, column = 1)

        self.__sekoitus_nappi = Button(self.__frame, text = "Sekoita",
                                        command = self.piirra_palkit)
        self.__sekoitus_nappi.grid(row = 1, column = 1)

        self.__palkki = Canvas(self.__frame, width = self.__maksimileveys,
                                        height = self.__maksimikorkeus)
        self.__palkki.grid(row = 2, column = 0, columnspan = 2)

        self.piirra_palkit()
        self.__paaikkuna.mainloop()

    def poista_focus(self, tapahtuma = None):
        """
        Poistaa sinisen taustan käyttäjän valitsemasta valikon esineeestä
        eli tässä tapauksessa algoritmista. Ilman tätä tausta jäisi sinisen
        väriseksi vaikka painaisit toista nappia. Näyttäisi muuten samalta kuin
        jos teksti olisi maalattuna.
        :param tapahtuma: Funktio tarvitsee 2 parametria toimiakseen, muuten
        tulee error. Parametria ei muuten suoraan käytetä ohjelmassa mutta se
        on pakko olla määriteltynä.
        :returns: None
        """
        return self.__frame.focus()

    def piirra_palkit(self, tapahtuma = None):
        """
        Piirtää palkkeja käyttäjän valitseman määrän verran. Poistaa myös
        aikaisemmin piirretyt palkit, jos esim. palkkien määrää muutetaan.
        ^^Muuten ohjelma täyttyisi eri paksuisista palkeista.
        :param tapahtuma: Funktio tarvitsee 2 parametria toimiakseen, muuten
        tulee error. Parametria ei muuten suoraan käytetä ohjelmassa mutta se
        on pakko olla määriteltynä.
        :returns: None
        """
        self.__palkki.delete("all")

        # Tyhjennetään listat ettei niihin jää vanhoja arvoja/palkkeja
        self.__palkit_listassa.clear()
        self.__palkkien_korkeudet.clear()

        # Kun käyttäjä muuttaa palkkien määrää tai sekoittaa palkit,
        # tulee "järjestä" nappi takaisin käyttöön, jos se oli aikaisemmin otettu
        # pois käytöstä joko siksi, että palkkeja järjestetään para-aikaa tai
        # palkit on jo järjestetty. Selitetty self.kaikki_valmiita() funktiossa
        self.__jarjestys_nappi["state"] = "normal"

        palkin_leveys = (self.__maksimileveys/self.__monta_palkkia_on.get())
        for i in range(1, self.__monta_palkkia_on.get()+1):
            # Arvotaan palkin korkeus (y1) randomisti.
            self.__palkit_listassa.append(self.__palkki.create_rectangle((i-1)*palkin_leveys, random.randint(10, self.__maksimikorkeus-170), i*palkin_leveys, self.__maksimikorkeus-160, fill = "white"))
            # coords-metodi palauttaa listan, jossa on palkin koordinaatit
            # [x1, y1, x2, y2].
            # Palkin korkeus on koordinaatti y1 eli toinen alkio, siksi [1].
            self.__palkkien_korkeudet.append(self.__palkki.coords(self.__palkit_listassa[i-1])[1])
        self.__kaikki_jarjestetty = False


    def ovatko_kaikki_valmiita(self):
        """
        Tarkastetaan onko kaikki palkit lajiteltu. Jos on, muutetaan
        palkit vihreän värisiksi.
        :returns: None
        """

        # Reverse siksi, että isompi arvo = kauempana ylätasosta, eli palkki
        # on silloin matalampi.
        if(self.__palkkien_korkeudet == sorted(self.__palkkien_korkeudet,
        reverse = True)):
            self.__kaikki_jarjestetty = True

            # "Järjestä" nappi muutetaan takaisin "normaaliksi" vasta
            # silloin, kun käyttäjä sekoittaa palkit tai muuttaa palkit
            # määrää eli siis self.piirra_palkit() funktio pitää siitä huolen.
            # Tämä siksi, että jos palkit on jo järjestetty, ei olisi järkeä
            # antaa käyttäjän yrittää järjestää _jo järjestettyjä_ palkkeja
            # uudestaan!
            self.__monta_palkkia_on["state"] = "normal"
            self.__monta_palkkia_on.configure(fg = "black")
            self.__sekoitus_nappi["state"] = "normal"
            for i in self.__palkit_listassa:
                self.__palkki.itemconfig(i, fill = "green")


    def bubble_sort(self):
        """
        Lajittelee palkit käyttäen bubble sort lajittelualgoritmia.
        Algoritmi toimii niin, että se vertaa n ja (n+1) elementin arvoa. Jos
        n>n+1, niin funktio vaihtaa niiden paikat keskenään. Eli isoin
        elementti siirretään aina loppuun, sitten toisiksi isoin... jne. kunnes
        kaikki elementit ovat oikeilla paikoillaan.
        :returns: None
        """

        # Jos lista on jo järjestetty, lopetetaan funktion toiminta.
        if(self.__kaikki_jarjestetty):
            return
        self.__kaikki_jarjestetty = False

        # Kun ohjelma järjestää palkkeja, poistetaan tilapäisesti mahdollisuus
        # painaa "Sekoita", "Järjestä" ja "Koko" nappeja. Sen takia, että kesken
        # lajittelun ne sekoittaisivat ohjelman toimintaa eikä ole järkevää
        # muuttaa esim. kokoa kesken lajittelun. Helppo ja toimiva tapa
        # välttyä virhetilanteilta.

        self.__monta_palkkia_on["state"] = "disabled"
        # Muutetaan teksti harmaaksi, koska "disabled" ei tee sitä scalelle.
        self.__monta_palkkia_on.configure(fg = "gray")

        self.__sekoitus_nappi["state"] = "disabled"
        self.__jarjestys_nappi["state"] = "disabled"
        for i in range(len(self.__palkit_listassa)-1):
            # Bubble sort vaatii n^2 vertailuja eli siksi tarvitaan 2 silmukkaa.
            # Kun esim. 5 viimeistä palkkia on jo lajiteltu, niitä ei enää
            # vertailla uudestaan (-i sisemmän silmukan "rangen" kohdalla).
            for j in range(0, len(self.__palkit_listassa)-1-i):
                # [j] < [j+1] tarkoittaa että [j+1] on kauempana yläreunasta
                # eli palkki on matalampi. Suurempi arvo = _matalampi_ palkki.
                if((self.__palkki.coords(self.__palkit_listassa[j])[1]) <
                self.__palkki.coords(self.__palkit_listassa[j+1])[1]):
                    # Vaihdetaan palkkien korkeudet keskenään funktiolla
                    self.vaihda_koordinaatit((self.__palkit_listassa[j]),
                                             (self.__palkit_listassa[j+1]))

                    # Päivitetään myös korkeudet listassa.
                    self.__palkkien_korkeudet[j], self.__palkkien_korkeudet[j+1] \
                    = self.__palkkien_korkeudet[j+1], self.__palkkien_korkeudet[j]

        self.ovatko_kaikki_valmiita()

    def quicksort(self, alku, loppu):
        """
        Lajittelee palkit käyttäen quicksort lajittelualgoritmia. Algoritmi
        on rekursiivinen mikä tarkoittaa sitä, että funktio kutsuu itse itseään.
        Algoritmi valitsee alussa jonkun "pivotin" joka on tässä tapauksessa
        välin viimeinen alkio. Sitten algoritmi asettaa pivotin oikealle
        paikalle. Pivotin vasemmalla puolella on sitä pienemmät arvot ja
        oikealla puolella sitä suuremmat arvot.
        Kun tätä toistetaan tarpeeksi monta kertaa, on lista lajiteltu
        koska kaikki arvot ovat oikeilla paikoillaan.
        :param alku: Listan välin ensimmäinen indeksi josta aloitetaan
        listan lajittelu eli pivotin oikealle paikalle asettaminen.
        :param loppu: Välin viimeinen indeksi eli indeksi johon lopetetaan
        listan lajittelu. Alku- ja loppuindeksit eivät aina ole 0 ja [-1] vaan
        voidaan tutkia esim. jotain rajattua osaväliä koko listasta, siitä kohta
        lisää.
        :returns: None
        """
        if(self.__kaikki_jarjestetty):
            return
        self.__kaikki_jarjestetty = False

        # Tehdään napeille sama homma kuin bubble sortissa
        self.__monta_palkkia_on["state"] = "disabled"
        self.__sekoitus_nappi["state"] = "disabled"
        self.__jarjestys_nappi["state"] = "disabled"
        if(alku < loppu):
            # Asetetaan ekana pivot oikeaan kohtaan listaa.
            pivot = self.pivotin_asettaminen(alku, loppu)
            # Koska pivot on jo oikealla paikalla, siihen ei siksi kosketa vaan
            self.quicksort(alku, pivot-1)
            self.quicksort(pivot+1, loppu)
        else:
            self.ovatko_kaikki_valmiita()

    def pivotin_asettaminen(self, alku, loppu):
        """
        Funktio lajittelee listan niin, että pivot on lopussa oikealla
        paikallaan ja funktio palauttaa pivotin indexin. Tämä tehdään niin,
        että pivottia pienemmät arvot laitetaan sen vasemmalle puolelle ja sitä
        suuremmat (tai yhtä suuret) menevät pivotin oikealle puolelle. Lopussa
        pivot on siis niiden välissä eli oikealla paikalla.

        :param alku: Listan välin ensimmäinen indeksi josta aloitetaan
        listan lajittelu eli pivotin oikealle paikalle asettaminen.
        :param loppu: Välin viimeinen indeksi eli indeksi johon lopetetaan
        listan lajittelu. Alku- ja loppuindeksit eivät aina ole 0 ja [-1] vaan
        voidaan tutkia esim. jotain rajattua osaväliä koko listasta, siitä kohta
        lisää.
        :returns: None
        """
        pivot = self.__palkit_listassa[loppu]
        i = alku-1
        # [alku-i] ovat arvoltaan pienemmät kuin pivot, ]i-j] ovat suuremmat
        # tai yhtä suuret kuin pivot.
        for j in range(alku, loppu, 1):
            # Jos alkio on arvoltaan pienempi kuin pivot, korotetaan i:n arvoa
            # yhdellä (koska kaikki alkiot i:hin asti ovat pienempiä kuin pivot)
            # ja vaihdetaan [j] ja [i] paikat.
            # Lopussa pivot laitetaan näiden väliin eli kohtaan i+1

            if((self.__palkki.coords(self.__palkit_listassa[j])[1]) > self.__palkki.coords(pivot)[1]):
                i+=1
                self.__palkkien_korkeudet[j], self.__palkkien_korkeudet[i] = self.__palkkien_korkeudet[i], self.__palkkien_korkeudet[j]
                self.vaihda_koordinaatit(self.__palkit_listassa[j], self.__palkit_listassa[i])

        self.__palkkien_korkeudet[i+1], self.__palkkien_korkeudet[loppu] = self.__palkkien_korkeudet[loppu], self.__palkkien_korkeudet[i+1]
        self.vaihda_koordinaatit(self.__palkit_listassa[i+1], self.__palkit_listassa[loppu])
        return i+1

    def valittu_algoritmi(self, tapahtuma = None):
        """
        Toimitaan sen perusteella, että kumpaa algoritmia käyttäjä
        halusi visualisoida.
        :param tapahtuma: Funktio tarvitsee 2 parametria toimiakseen, muuten
        tulee error. Parametria ei muuten suoraan käytetä ohjelmassa mutta se
        on pakko olla määriteltynä.
        :returns: None
        """

        try:
            if(self.__valitse_algoritmi.get() == "Bubble Sort"):
                self.bubble_sort()
            elif(self.__valitse_algoritmi.get() == "Quicksort"):
                self.quicksort(0, len(self.__palkit_listassa)-1)

        # Jos käyttäjä sulkee ohjelman kesken lajittelun, ilmestyy pythonin
        # konsoliin error. Tässä tapauksessa palautetaan vaan False.
        except(TclError):
            return False

    def vaihda_koordinaatit(self, koordinaatti_1, koordinaatti_2):
        """
        Vaihtaa palkit keskenään
        :param koordinaatti_1:
        :param koordinaatti_2:
        :returns: None
        """
        x1_1, x1_2 = self.__palkki.coords(koordinaatti_1)[0], self.__palkki.coords(koordinaatti_2)[0]
        y1_1, y1_2 = self.__palkki.coords(koordinaatti_2)[1], self.__palkki.coords(koordinaatti_1)[1]
        x2_1, x2_2 = self.__palkki.coords(koordinaatti_1)[2], self.__palkki.coords(koordinaatti_2)[2]
        y2_1, y2_2 = self.__palkki.coords(koordinaatti_1)[3], self.__palkki.coords(koordinaatti_2)[3]

        self.__palkki.coords(koordinaatti_1, x1_1, y1_1, x2_1, y2_1)
        self.__palkki.coords(koordinaatti_2, x1_2, y1_2, x2_2, y2_2)
        self.__palkki.update()
        time.sleep(0.001*self.__viive.get())

def main():
    Kayttoliittyma()

main()
