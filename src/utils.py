# utils.py
from datetime import date
from fastapi import HTTPException, status
import logging

def validate_not_past_date(request_date: date):
    if request_date < date.today():
        logging.warning(f"Request date {request_date} is in the past.")
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="The request_date cannot be in the past.")