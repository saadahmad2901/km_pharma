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
    # Step 1: Get the party
    party = db.query(models.Parties).filter(models.Parties.id == party_id).first()

    if not party:
        return None  # or raise HTTPException(status_code=404, detail="Party not found")

    distributer = (
        db.query(models.Distributers)
        .filter(models.Distributers.id == party.distributer_id)
        .first()
    )

    if distributer:
        # Step 3: Get user using user_id from distributer
        user = (
            db.query(models.Users)
            .filter(models.Users.id == distributer.user_id)
            .first()
        )

        # Step 4: Set distributer_name
        party.distributer_name = user.fullname if user else None
    else:
        party.distributer_name = None

    return party 

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

