class SubscriptionRequestError(ValueError):
    pass


class OrderFormatError(TypeError):
    pass


class NonJsonOrderError(OrderFormatError):
    pass


class InvalidDatatypeError(OrderFormatError):
    pass


class OrderValueError(ValueError):
    pass


class InstrumentNotFoundError(OrderValueError):
    pass


class InvalidOrderTypeError(OrderValueError):
    pass


class InvalidOrderSideError(OrderValueError):
    pass


class InvalidAmountError(OrderValueError):
    pass


class ExcessiveAmountError(OrderValueError):
    pass


class PriceRequestFormatError(TypeError):
    pass


class PriceRequestValueError(ValueError):
    pass


class InstrumentNotPriceableError(PriceRequestValueError):
    pass


class InvalidLevelsError(PriceRequestValueError):
    pass

class InvalidFileName(PriceRequestValueError):
    pass


