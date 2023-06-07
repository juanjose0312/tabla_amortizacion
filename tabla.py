from datetime import datetime, timedelta

def pago_puntual(tabla,num_ciclo):

        # tabla          = en la que se almacena los datos
        # numero de cilo = cuota que se esta evaluando
        # fecha_oficial  = cuando se deberia de pagar
        # fecha_pago     = cuando se pago

        fecha_oficial= tabla[1][num_ciclo]
        fecha_pago   = tabla[2][num_ciclo]
        difencia     = 0

        if fecha_oficial == fecha_pago:
            return True,difencia

        diferencia= fecha_pago-fecha_oficial
        return False,diferencia.days

def tabla_amortizacion(opcion_fecha,valor_inicial,numero_cuotas,intereses,interes_mora):

    

    dias_ciclo_mes=[58,88,119,149,180,210,241,272,302,333,363,0]

    fecha_inicial= datetime.strptime("2022-01-01",'%Y-%m-%d')
    ciclo_cuota  = 0

    tabla=[[],[],[],[],[],[],[],[],[],[]]

    # numero de cuotas  1

    for i in range(numero_cuotas):
        tabla[0].append(i+1)

    # fecha de pago     2

    for i in range(numero_cuotas):
        if opcion_fecha == 'periodo 1':
            tabla[1].append(fecha_inicial + timedelta(dias_ciclo_mes[i]))
        else:
            tabla[1].append(fecha_inicial + timedelta(dias_ciclo_mes[i+5]))

        


    while ciclo_cuota < numero_cuotas:
        
        # fecha pagada      3

        if opcion_fecha == 'periodo 1':
            tabla[2].append(fecha_inicial + timedelta(dias_ciclo_mes[ciclo_cuota]))
        else:
            tabla[2].append(fecha_inicial + timedelta(dias_ciclo_mes[ciclo_cuota+5]))

        
        # cuota normal      4

        if ciclo_cuota == 0:
            tabla[4].append(int(valor_inicial/((1-(1+intereses)**(numero_cuotas*-1))/intereses)))
        else:
            tabla[4].append(int(tabla[8][ciclo_cuota-1]/((1-(1+intereses)**((numero_cuotas-ciclo_cuota)*-1))/intereses)))

        
        # interes de mora   5

        pago_puntual_bool,difencia = pago_puntual(tabla,ciclo_cuota)

        if pago_puntual_bool:
            tabla[7].append(0)
        else:
            interes_mora_aux=(((tabla[4][ciclo_cuota]*interes_mora)/(30))*difencia)
            tabla[7].append(int(interes_mora_aux))
            print(difencia)

        # abono a intereses 7

        if ciclo_cuota == 0:
            tabla[6].append(int(valor_inicial*intereses))
        else:
            tabla[6].append(int(tabla[8][ciclo_cuota-1]*intereses))

        # cuota extra       6

        tabla[3].append(0)

        # abono a capital   8

        if ciclo_cuota == 0:
            tabla[5].append(int(tabla[4][ciclo_cuota]-tabla[6][ciclo_cuota]))
        else:
            tabla[5].append(int(tabla[4][ciclo_cuota]-tabla[6][ciclo_cuota]+tabla[3][ciclo_cuota]-tabla[7][ciclo_cuota-1]))

        # saldo             9

        if ciclo_cuota == 0:
            tabla[8].append(int(valor_inicial-tabla[5][ciclo_cuota]))
        else:
            tabla[8].append(int(tabla[8][ciclo_cuota-1]-tabla[5][ciclo_cuota]))

        
        # pagado            10

        tabla[9].append(True)

        ciclo_cuota+=1

    return tabla