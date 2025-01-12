import json

def visa_bokningar():
    """Visar alla bokningar från bookings.json i en tabell med snygg formatering."""
    try:
        with open("bookings.json", "r") as file:
            bokningar = json.load(file)
            if bokningar:
                print("\nAlla bokningar:\n")
                print(f"{'Namn':<20}{'Datum och Tid':<20}")
                print("=" * 40)
                for bokning in bokningar:
                    print(f"{bokning['name']:<20}{bokning['date_time']:<20}")
            else:
                print("\nInga bokningar hittades.")
    except FileNotFoundError:
        print("\nIngen bokningsfil hittades.")
    except json.JSONDecodeError:
        print("\nFel i bokningsfilen.")


import json
from datetime import datetime

from datetime import datetime

def skapa_bokning():
    """Skapar en ny bokning med validering av namn och datum/tid."""
    while True:
        name = input("Ange ditt namn: ").strip()
        if name:
            break
        print("Namnet får inte vara tomt!")

    while True:
        tid_str = input("Ange datum och tid för bokningen (YYYY-MM-DD HH:MM): ").strip()
        try:
            tid = datetime.strptime(tid_str, "%Y-%m-%d %H:%M")
            if tid < datetime.now():
                print("Datumet och tiden måste vara i framtiden!")
                continue
            break
        except ValueError:
            print("Fel format! Använd formatet YYYY-MM-DD HH:MM.")

    ny_bokning = {
        "name": name,
        "date_time": tid_str
    }

    try:
        with open("bookings.json", "r") as fil:
            bokningar = json.load(fil)
    except FileNotFoundError:
        bokningar = []

    # Kontrollera om bokningen redan finns (namn och datum/tid)
    if any(bokning["name"].lower() == name.lower() and bokning["date_time"] == tid_str for bokning in bokningar):
        print("\nEn bokning med detta namn och datum/tid finns redan!")
        return

    bokningar.append(ny_bokning)

    with open("bookings.json", "w") as fil:
        json.dump(bokningar, fil, indent=4)

    print("\nBokningen har sparats!")




def sok_bokning():
    """Söker efter bokningar baserat på namn eller datum (delvis matchning)."""
    try:
        with open("bookings.json", "r") as fil:
            bokningar = json.load(fil)
    except FileNotFoundError:
        print("\nIngen bokningsfil hittades.")
        return

    if not bokningar:
        print("\nInga bokningar hittades.")
        return

    soktyp = input("Vill du söka efter namn eller datum? (namn/datum): ").strip().lower()
    if soktyp == "namn":
        sokterm = input("Ange namnet eller del av namnet att söka efter: ").strip().lower()
        resultat = [b for b in bokningar if sokterm in b.get("name", "").lower()]
    elif soktyp == "datum":
        sokterm = input("Ange datum eller del av datumet att söka efter (YYYY-MM-DD): ").strip()
        resultat = [b for b in bokningar if sokterm in b.get("date_time", "")]
    else:
        print("Ogiltigt val. Försök igen.")
        return

    if resultat:
        print("\nSökresultat:\n")
        print(f"{'Namn':<20}{'Datum och Tid':<20}")
        print("=" * 40)
        for bokning in resultat:
            print(f"{bokning['name']:<20}{bokning['date_time']:<20}")
    else:
        print("\nIngen bokning matchade din sökning.")





def ta_bort_bokning():
    """Tar bort en bokning baserat på namn eller datum och tid."""
    visa_bokningar()
    
    if input("\nVill du ta bort en bokning? (ja/nej): ").lower() != 'ja':
        return

    namn = input("Ange namnet på bokningen du vill ta bort: ")
    datum_tid = input("Ange datum och tid på bokningen du vill ta bort: ")

    try:
        with open("bookings.json", "r") as file:
            bokningar = json.load(file)

        # Kontrollera om bokningen finns
        bokning_to_remove = None
        for bokning in bokningar:
            if bokning['name'] == namn and bokning['date_time'] == datum_tid:
                bokning_to_remove = bokning
                break

        if bokning_to_remove:
            bokningar = [bokning for bokning in bokningar if bokning != bokning_to_remove]
            with open("bookings.json", "w") as file:
                json.dump(bokningar, file, indent=4)
            print("\nBokningen har tagits bort!")
        else:
            print("\nIngen bokning hittades med det namnet och datumet/tiden.")
    except (FileNotFoundError, json.JSONDecodeError):
        print("\nFel med bokningsfilen, inget att ta bort.")

def uppdatera_bokning():
    """Uppdaterar en befintlig bokning baserat på namn och datum."""
    try:
        with open("bookings.json", "r") as fil:
            bokningar = json.load(fil)
    except FileNotFoundError:
        print("\nIngen bokningsfil hittades.")
        return

    if not bokningar:
        print("\nInga bokningar hittades.")
        return

    visa_bokningar()
    print("\nAnge information om bokningen du vill uppdatera.")
    namn = input("Ange namnet på bokningen: ").strip()
    datum_tid = input("Ange datum och tid på bokningen (YYYY-MM-DD HH:MM): ").strip()

    # Hitta bokningen att uppdatera
    for bokning in bokningar:
        if bokning["name"] == namn and bokning["date_time"] == datum_tid:
            print("\nBokning hittad!")
            nytt_namn = input("Ange nytt namn (lämna tomt för att behålla det gamla): ").strip()
            nytt_datum_tid = input("Ange nytt datum och tid (YYYY-MM-DD HH:MM) (lämna tomt för att behålla det gamla): ").strip()

            if nytt_namn:
                bokning["name"] = nytt_namn
            if nytt_datum_tid:
                bokning["date_time"] = nytt_datum_tid

            with open("bookings.json", "w") as fil:
                json.dump(bokningar, fil, indent=4)
            print("\nBokningen har uppdaterats!")
            return

    print("\nIngen bokning hittades med den angivna informationen.")

import csv

def exportera_till_csv():
    """Exporterar bokningar till en CSV-fil."""
    try:
        with open("bookings.json", "r") as fil:
            bokningar = json.load(fil)

        if not bokningar:
            print("Inga bokningar att exportera.")
            return

        with open("bokningar.csv", "w", newline="") as csv_fil:
            writer = csv.writer(csv_fil)
            writer.writerow(["Namn", "Datum och Tid"])

            for bokning in bokningar:
                writer.writerow([bokning["name"], bokning["date_time"]])

        print("Bokningarna har exporterats till bokningar.csv!")
    except (FileNotFoundError, json.JSONDecodeError):
        print("Fel vid export. Kontrollera bokningsfilen.")

def importera_fran_csv():
    """Importerar bokningar från en CSV-fil."""
    try:
        with open("bokningar.csv", "r") as csv_fil:
            reader = csv.DictReader(csv_fil)
            bokningar = []

            for rad in reader:
                bokningar.append({
                    "name": rad["Namn"],
                    "date_time": rad["Datum och Tid"]
                })

        with open("bookings.json", "w") as fil:
            json.dump(bokningar, fil, indent=4)

        print("Bokningar har importerats från bokningar.csv till bookings.json!")
    except FileNotFoundError:
        print("Ingen CSV-fil hittades.")
    except Exception as e:
        print(f"Fel vid import: {e}")

def main():
    while True:
        print("\nVad vill du göra?")
        print("1. Skapa en bokning")
        print("2. Visa alla bokningar")
        print("3. Ta bort en bokning")
        print("4. Sök efter en bokning")
        print("5. Uppdatera en bokning")
        print("6. Exportera bokningar till CSV")
        print("7. Importera bokningar från CSV")
        print("8. Avsluta")

        val = input("Välj ett alternativ (1/2/3/4/5/6/7/8): ")

        if val == "1":
            skapa_bokning()
        elif val == "2":
            visa_bokningar()
        elif val == "3":
            ta_bort_bokning()
        elif val == "4":
            sok_bokning()
        elif val == "5":
            uppdatera_bokning()
        elif val == "6":
            exportera_till_csv()
        elif val == "7":
            importera_fran_csv()
        elif val == "8":
            print("Tack och hej!")
            break
        else:
            print("Ogiltigt val. Försök igen.")



if __name__ == "__main__":
    main()
