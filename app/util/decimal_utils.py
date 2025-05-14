from decimal import Decimal

class DecimalUtils:
    
    def __init__(self):
        pass
    
    def decimal_default(obj: object):
        if isinstance(obj, Decimal):
            try:
                return int(obj) 
            except (ValueError, OverflowError):
                return float(obj) 
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")
