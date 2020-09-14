from reportlab.lib.units import cm

FACTURA = (21.6*cm, 22.7*cm)

def landscape(pagesize):
    """Use this to get page orientation right"""
    a, b = pagesize
    if a < b:
        return (b, a)
    else:
        return (a, b)
 
def portrait(pagesize):
    """Use this to get page orientation right"""
    a, b = pagesize
    if a >= b:
        return (b, a)
    else:
        return (a, b)