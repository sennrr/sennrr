from app import app, db, Vacature

# Zet de Flask-applicatiecontext aan
with app.app_context():
    db.create_all()  # Zorg ervoor dat de database wordt aangemaakt als die nog niet bestaat

    # Testvacatures toevoegen
    vacature1 = Vacature(titel="Verpleegkundige", beschrijving="We zoeken een ervaren verpleegkundige voor een zorginstelling.")
    vacature2 = Vacature(titel="Administratief Medewerker", beschrijving="Ben jij nauwkeurig en communicatief sterk? Solliciteer nu!")
    vacature3 = Vacature(titel="Software Developer", beschrijving="Werk mee aan innovatieve projecten als Python Developer.")

    db.session.add_all([vacature1, vacature2, vacature3])
    db.session.commit()

    print("Vacatures succesvol toegevoegd!")
