from datetime import datetime, timezone


def calcular_diferenca_datas(data1, data2 = datetime.now(timezone.utc)):
    
    #data2 = datetime(2024, 7, 30, 21, 28, 34, tzinfo=timezone.utc)
    diferenca = data2 - data1
    print(data2)
    if diferenca.total_seconds() < 3600:
        minutos = int(diferenca.total_seconds() // 60)
        if minutos > 1: 
            return f"há {minutos} minutos."
        return f"há {minutos} minuto."
    
    elif diferenca.total_seconds() < 86400:  # 24 horas em segundos
        horas = int(diferenca.total_seconds() // 3600)
        if horas > 1:
            return f"há {int(horas)} horas."
        return f"há {int(horas)} hora."
        
    elif diferenca.days < 7:
        dias = diferenca.days
        if diferenca.days > 1:
            return f"há {int(dias)} dias."
        return f"há {int(dias)} dia."
        
    elif diferenca.days < 30:
        semanas = diferenca.days // 7
        if semanas > 1:
            return f"há {int(semanas)} semanas."
        return f"há {int(semanas)} semana."
    elif diferenca.days < 365:
        semanas = diferenca.days // 7
        meses = int(semanas // 4)
        if meses > 1:
            return f"há { meses } meses."
        return f"há {meses} mes."
    else:
        semanas = diferenca.days // 7
        meses = semanas // 4
        anos = int(meses // 12)
        if anos >1:
            return f"há {int(anos)} anos."
        return f"há {int(anos)} ano."

