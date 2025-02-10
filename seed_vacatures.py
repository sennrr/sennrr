from app import app, db, Vacature

with app.app_context():
    db.create_all()

    vacatures = [
        {"titel": "Verpleegkundige", "beschrijving": "Wij zoeken een verpleegkundige voor een ziekenhuis in Amsterdam.",
         "werkuren": "Fulltime", "salaris": "€3.000 - €4.200", "locatie": "Amsterdam", 
         "vereisten": "Verpleegkunde diploma, BIG-registratie", 
         "verantwoordelijkheden": "Zorg verlenen aan patiënten, medicatie toedienen"},
         
        {"titel": "Doktersassistent", "beschrijving": "Assisteer huisartsen en specialisten in een drukke praktijk.",
         "werkuren": "Parttime", "salaris": "€2.500 - €3.500", "locatie": "Rotterdam", 
         "vereisten": "MBO-diploma Doktersassistent", 
         "verantwoordelijkheden": "Afspraken plannen, medische dossiers beheren"}
    ]

    for vacature in vacatures:
        db.session.add(Vacature(**vacature))

    db.session.commit()
    print("✅ Zorgvacatures met extra informatie toegevoegd!")
