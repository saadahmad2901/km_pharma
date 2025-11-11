from sqlalchemy.orm import Session
from app import schemas, models
from typing import List

def get_parties(db: Session) -> List[schemas.PartiesOut]:
    parties = db.query(models.Parties).all()

    for party in parties:
        # Step 1: Get distributer by ID
        distributer = (
            db.query(models.Distributers)
            .filter(models.Distributers.id == party.distributer_id)
            .first()
        )

        if distributer:
            # Step 2: Get user using user_id from distributer
            user = (
                db.query(models.Users)
                .filter(models.Users.id == distributer.user_id)
                .first()
            )

            # Step 3: Assign user fullname to party
            party.distributer_name = user.fullname if user else None
        else:
            party.distributer_name = None

    return parties

def get_party_by_id(db: Session, party_id: int) -> schemas.PartiesOut:
    party = db.query(models.Parties).filter(models.Parties.id == party_id).first()
    if not party:
        return None  

    distributer = (
        db.query(models.Distributers)
        .filter(models.Distributers.id == party.distributer_id)
        .first()
    )

    if distributer:
        user = (
            db.query(models.Users)
            .filter(models.Users.id == distributer.user_id)
            .first()
        )

        party.distributer_name = user.fullname if user else None
    else:
        party.distributer_name = None

    return party 

def get_parties_by_distributer_id(db: Session, distributer_id: int) -> schemas.DistributerResponse:
    # Fetch parties from DB
    parties_objects = db.query(models.Parties).filter(models.Parties.distributer_id == distributer_id).all()

    # Convert each SQLAlchemy object to PartiesBase
    parties = [
        schemas.PartiesBase(
            name=p.name,
            email=p.email,
            phone=p.phone,
            adress=p.adress,
            distributer_id=p.distributer_id
        )
        for p in parties_objects
    ]

    # Fetch distributer and corresponding user
    distributer = db.query(models.Distributers).filter(models.Distributers.id == distributer_id).first()
    distributer_name = None
    if distributer:
        user = db.query(models.Users).filter(models.Users.id == distributer.user_id).first()
        distributer_name = user.fullname if user else None

    # Return a clean Pydantic model
    return schemas.DistributerResponse(
        distributer_id=distributer_id,
        distributer_name=distributer_name,
        parties=parties
    )



def create_party(party: schemas.PartiesCreate, db: Session) -> models.Parties:
    

    db_party = models.Parties(**party.dict())
    db.add(db_party)
    db.commit()
    db.refresh(db_party)
    return db_party

def update_party(db: Session, party_id: int, party: schemas.PartiesUpdate) -> models.Parties:
    db_party = db.query(models.Parties).filter(models.Parties.id == party_id).first()
    if db_party:
        for key, value in party.dict().items():
            setattr(db_party, key, value)
        db.commit()
        db.refresh(db_party)
    return db_party

def delete_party(db: Session, party_id: int) -> models.Parties:
    db_party = db.query(models.Parties).filter(models.Parties.id == party_id).first()
    if db_party:
        db.delete(db_party)
        db.commit()
    return db_party

