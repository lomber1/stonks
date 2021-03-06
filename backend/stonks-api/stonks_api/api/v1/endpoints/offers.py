from datetime import datetime
from typing import Optional, List

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from requests import Session
from starlette.responses import JSONResponse
from stonks_types import schemas

# from stonks_api.api.v1.endpoints.device_recognizer import device_recognizer
from stonks_api import crud
from stonks_api.api.v1.endpoints.devices import device_not_found
from stonks_api.database import get_db

router = APIRouter()


def offer_not_found(offer):
    if offer is None:
        raise HTTPException(status_code=404, detail="Offer not found")


def delivery_not_found(delivery):
    if delivery is None:
        raise HTTPException(status_code=404, detail="Delivery not found")


@router.get("/", response_model=List[schemas.Offer])
def get_offers(skip: int = 0,
               limit: int = 50,
               last_update_before: Optional[datetime] = None,
               last_update_after: Optional[datetime] = None,
               scraped_before: Optional[datetime] = None,
               scraped_after: Optional[datetime] = None,
               last_stonks_check_before: Optional[datetime] = None,
               has_device: Optional[bool] = None,
               is_active: Optional[bool] = True,
               db: Session = Depends(get_db)):
    offers = crud.offer.get_many(db=db,
                                 skip=skip,
                                 limit=limit,
                                 last_update_before=last_update_before,
                                 last_update_after=last_update_after,
                                 scraped_before=scraped_before,
                                 scraped_after=scraped_after,
                                 last_stonks_check_before=last_stonks_check_before,
                                 has_device=has_device,
                                 is_active=is_active)

    return offers


@router.get("/{offer_id}", response_model=schemas.Offer)
def get_offer(offer_id: str, db: Session = Depends(get_db)):
    offer = crud.offer.get_one(db=db, id=offer_id)

    offer_not_found(offer)

    return offer


@router.post("/", response_model=schemas.Offer, status_code=201)
def create_offer(offer: schemas.OfferCreate,
                 get_device_model: bool = False,
                 db: Session = Depends(get_db)):
    db_offer = crud.offer.get_one(db=db, id=offer.id)

    if db_offer is not None:
        raise HTTPException(status_code=409, detail="Offer already exists. Consider using upsert route.")

    # if get_device_model is True get device model and set it
    # if get_device_model:
    #     model = device_recognizer.get_info(offer.title).model.lower()
    #     offer.device_model = model if len(model) > 2 else None

    if offer.device_name is not None:
        device = crud.device.get_one_by_name(db=db,
                                             name=offer.device_name)

        device_not_found(device)

    db_offer = crud.offer.create(db=db, new_model=offer)

    return db_offer


@router.put("/{offer_id}", response_model=schemas.Offer)
def update_offer(offer_id: str,
                 offer: schemas.OfferUpdate,
                 get_device_model: bool = False,
                 db: Session = Depends(get_db)):
    """
    Update offer information.
    Note that you cannot update delivery information from here, instead you must call /offers/id/deliveries/id
    """
    db_offer = crud.offer.get_one(db=db, id=offer_id)

    offer_not_found(db_offer)

    # if get_device_model is True get device model and set it
    # if get_device_model:
    #     model = device_recognizer.get_info(offer.title).model.lower()
    #     offer.device_model = model if len(model) > 2 else None

    db_offer = crud.offer.update(db=db,
                                 id=offer_id,
                                 update_model=offer)

    return db_offer


@router.delete("/{offer_id}")
def delete_offer(offer_id: str, db: Session = Depends(get_db)):
    db_offer = crud.offer.get_one(db=db, id=offer_id)
    offer_not_found(db_offer)

    crud.offer.remove(db=db,
                      id=offer_id)

    return JSONResponse({"detail": "Offer has been deleted"})


@router.get("/{offer_id}/deliveries", response_model=List[schemas.Delivery])
def get_deliveries_for_offer(offer_id: str,
                             skip: int = 0,
                             limit: int = 50,
                             db: Session = Depends(get_db)):
    offer = crud.offer.get_one(db=db, id=offer_id)
    offer_not_found(offer)

    deliveries = crud.delivery.get_deliveries_for_offer(db=db,
                                                        offer_id=offer_id,
                                                        skip=skip,
                                                        limit=limit)

    return deliveries


@router.post("/{offer_id}/deliveries", response_model=List[schemas.Delivery], status_code=201)
def add_deliveries_for_offer(offer_id: str,
                             deliveries: List[schemas.DeliveryCreate],
                             db: Session = Depends(get_db)):
    offer = crud.offer.get_one(db=db, id=offer_id)
    offer_not_found(offer)

    db_deliveries = crud.delivery.create_deliveries_for_offer(db=db,
                                                              offer_id=offer_id,
                                                              deliveries=deliveries)

    return db_deliveries


@router.delete("/{offer_id}/deliveries")
def delete_deliveries_for_offer(offer_id: str,
                                db: Session = Depends(get_db)):
    offer = crud.offer.get_one(db=db, id=offer_id)
    offer_not_found(offer)

    crud.delivery.delete_deliveries_for_offer(db=db,
                                              offer_id=offer_id)

    return {"message": f"Deliveries for offer {offer_id} had been deleted."}


@router.put("/{offer_id}/deliveries/{delivery_id}", response_model=schemas.Delivery)
def update_delivery(offer_id: str,
                    delivery_id: int,
                    delivery: schemas.DeliveryUpdate,
                    db: Session = Depends(get_db)):
    offer = crud.offer.get_one(db=db, id=offer_id)
    offer_not_found(offer)

    db_delivery = crud.delivery.get_one(db=db,
                                        id=delivery_id)
    delivery_not_found(db_delivery)

    db_delivery = crud.delivery.update(db=db,
                                       id=delivery_id,
                                       update_model=delivery)

    return db_delivery
