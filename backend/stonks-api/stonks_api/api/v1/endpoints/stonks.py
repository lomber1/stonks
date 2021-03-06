from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from stonks_types import schemas

from stonks_api import crud
from stonks_api.api.v1.endpoints.offers import offer_not_found
from stonks_api.crud import crud_stonks
from stonks_api.database import get_db

router = APIRouter()


def stonks_not_found(stonks):
    if stonks is None:
        raise HTTPException(status_code=404, detail="Stonks not found")


@router.get("/stonks", response_model=List[schemas.Stonks])
def get_stonks_list(skip: int = 0,
                    limit: int = 50,
                    is_active: Optional[bool] = True,
                    sort: schemas.StonksSortBy = schemas.StonksSortBy.stonks_amount_desc,
                    db: Session = Depends(get_db)):
    db_stonkses = crud.stonks.get_many(db=db,
                                       skip=skip,
                                       limit=limit)

    return db_stonkses


@router.get("/stonks/{stonks_id}", response_model=schemas.Stonks)
def get_stonks(stonks_id: int,
               db: Session = Depends(get_db)):
    db_stonks = crud.stonks.get_one(db=db, id=stonks_id)
    stonks_not_found(db_stonks)

    return db_stonks


@router.post("/offers/{offer_id}/stonks", response_model=schemas.Stonks, status_code=201)
def create_stonks(offer_id: str,
                  stonks: schemas.StonksCreate,
                  db: Session = Depends(get_db)):
    offer = crud.offer.get_one(db=db, id=offer_id)
    offer_not_found(offer)

    db_stonks = crud.stonks.create_for_offer(db=db,
                                             offer_id=offer_id,
                                             stonks=stonks)

    return db_stonks


# @router.put("/stonks/{stonks_id}")
# def update_stonks(stonks_id: int,
#                   stonks: schemas.Stonks,
#                   db: Session = Depends(get_db)):
#     pass


@router.delete("/stonks/{stonks_id}")
def delete_stonks(stonks_id: int,
                  db: Session = Depends(get_db)):
    stonks = crud.stonks.get_one(db=db, id=stonks_id)
    stonks_not_found(stonks)

    crud.stonks.remove(db=db, id=stonks_id)

    return {"detail": "Stonks has been deleted."}
