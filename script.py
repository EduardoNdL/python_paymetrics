import psutil, datetime, time, pandas as pd, os, platform

while True:

    disco_usado = ((psutil.disk_io_counters().write_bytes) / 1024 / 1024)
    time.sleep(5)
    disco_usadoN = ((psutil.disk_io_counters().write_bytes) / 1024 / 1024)
    taxaI = disco_usadoN - disco_usado

    rede_antiga = (psutil.net_io_counters())
    time.sleep(5)
    rede_nova = psutil.net_io_counters()

    bytes_enviados = ((rede_nova.bytes_sent - rede_antiga.bytes_sent) / 1024 / 1024 )
    bytes_recebidos = ((rede_nova.bytes_recv - rede_antiga.bytes_recv) / 1024 / 1024 )


    mac_Ethernet = None
    mac_Wifi = None
    for itens, detalhes in psutil.net_if_addrs().items():
        for especicacoes in detalhes:
            if platform.system() == 'Windows':
                if itens == 'Ethernet' and mac_Ethernet == None:
                    mac_Ethernet = especicacoes.address
                elif itens == 'Wi-Fi' and mac_Wifi == None:
                    mac_Wifi = especicacoes.address
            else:
                if itens.startswith(("eth", "enp", "ens")) and mac_Ethernet == None:
                    mac_Ethernet = especicacoes.address
                elif itens.startswith(("wlan", "wlp")) and mac_Wifi == None:
                    mac_Wifi = especicacoes.address
    
    timestamp = time.time()
    data_formatada = datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

    valores = {
        "Datetime": [data_formatada],
        "Mac_Ethernet": [mac_Ethernet],
        "Mac_Wifi": [mac_Wifi],
        "cpu": [psutil.cpu_percent(interval=1)],
        "ram_usada": [psutil.virtual_memory().percent],
        "ram_livre": [((psutil.virtual_memory().available) / 1024 / 1024 / 1024)],
        "swap": [psutil.swap_memory().percent],
        "discoTot_usado": [(psutil.disk_usage('/').percent)],
        "Taxa_Inscricao": [taxaI],
        "Mb_Enviados": [bytes_enviados],
        "Mb_Recebidos": [bytes_recebidos]
    }
    
    df = pd.DataFrame(valores)
    if os.path.exists("DadosHardware.csv"):
        df.to_csv("DadosHardware.csv", sep= ';', mode= 'a', index=False, header=False)
    else:
        df.to_csv("DadosHardware.csv", index=False, sep= ';')
    
    time.sleep(5)
