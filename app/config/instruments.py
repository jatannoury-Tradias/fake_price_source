from app.models.instrument import Instrument
from app.config.currencies import currency_dict

instruments = [
    Instrument(currency_leg_1=currency_dict["TKN"],
               currency_leg_2=currency_dict["EUR"],
               instrument_precision=2)
]

instruments_dict = {instrument.instrument_code: instrument for instrument in instruments}


