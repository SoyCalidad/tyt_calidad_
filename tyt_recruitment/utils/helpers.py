from .constants import ( 
    GENDER_SELECTION,
    MARITAL_STATUS_SELECTION
)
from .constants_string import (
    MARITAL_STATUS_DEFAULT_VALUE, 
    GENDER_DEFAULT_VALUE
)

def get_label_from_marital_status_list(key):

    for item in MARITAL_STATUS_SELECTION:
        if item[0] == key:
            return item[1]
    return MARITAL_STATUS_DEFAULT_VALUE

def get_label_from_gender_list(key):

    for item in GENDER_SELECTION:
        if item[0] == key:
            return item[1]
    return GENDER_DEFAULT_VALUE