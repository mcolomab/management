from .formats import formatFloats

def dosCifras(num):
    UNIDADES = [
        'uno ',
        'dos ',
        'tres ',
        'cuatro ',
        'cinco ',
        'seis ',
        'siete ',
        'ocho ',
        'nueve ',
        'diez ',
        'once ',
        'doce ',
        'trece ',
        'catorce ',
        'quince ',
        'dieciseis ',
        'diecisiete ',
        'dieciocho ',
        'diecinueve ',
        'veinte ',
    ]

    DECENAS = [
        'veinti',
        'treinta ',
        'cuarenta ',
        'cincuenta ',
        'sesenta ',
        'setenta ',
        'ochenta ',
        'noventa ',
        'cien ',
    ]

    if int(num) <= 20:
        return UNIDADES[int(num) - 1]

    if len(num) == 2:
        if int(num[0]) == 2:
            return DECENAS[0] + UNIDADES[int(num[1]) - 1]
        else:
            return DECENAS[int(num[0]) - 2] + 'y ' + UNIDADES[int(num[1]) - 1]

def tresCifras(num):
    CENTENAS = [
        'ciento ',
        'doscientos ',
        'trescientos ',
        'cuatrocientos ',
        'quinientos ',
        'seiscientos ',
        'setecientos ',
        'ochocientos ',
        'novecientos ',
    ]

    if int(num) == 100:
        return 'cien '
    return CENTENAS[int(num[0]) - 1] + dosCifras(num[1:])

def cuatroCifras(num):
    if int(num) == 1000:
        return 'mil '
    
    if num[0] == '1':
        return 'mil ' + tresCifras(num[1:])

    return dosCifras(num[0]) + 'mil ' + tresCifras(num[1:])

def cincoCifras(num):
    if int(num) == 10000:
        return 'diez mil '
    return dosCifras(num[:2]) + 'mil ' + tresCifras(num[2:])

def seisCifras(num):
    if int(num) == 100000:
        return 'cien mil '
    return tresCifras(num[:3]) + 'mil ' + tresCifras(num[3:])

def intToLetters(num):
    if len(num) <= 2:
        return dosCifras(num)
    
    if len(num) == 3:
        return tresCifras(num)

    if len(num) == 4:
        return cuatroCifras(num)

    if len(num) == 5:
        return cincoCifras(num)

    if len(num) == 6:
        return seisCifras(num)

def numberToStr(num):
    if num < 0 or num > 999999.99:
        return 'No es posible convertir el numero en letras'
    
    entero, decimal = formatFloats(num).split('.')

    return intToLetters(entero) + 'con ' + decimal + '/100 soles'