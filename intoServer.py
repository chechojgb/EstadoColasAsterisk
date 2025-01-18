import paramiko
import re
import os
from dotenv import load_dotenv

load_dotenv()
# Server Access Credentials
USER_SERVER = os.getenv('USER_SERVER')
PASSWORD_SERVER = os.getenv('PASSWORD_SERVER')
SERVER_ID = os.getenv('SERVER_ID')
# DB Access Credentials



options = [
    "TRAMITES_CW17932",
    "SOPORTE_CW17932",
    "MOVIL_CW17932",
    "HOGARES-POSTVENTAS",
    "CANCELACION-TOTAL_FTTH",
    "CROSS_POSVENTA_CAMBIO_DE_PLAN-COS",
    "HOGARES-POSTVENTA_PQR_PLATINO",
    "HOGARES-POSTVENTA_TRASLADOS_COBRE",
    "HOGARES-POSTVENTA_TRASLADOS_FIBRA",
    "HOGARES-POSTVENTA_TRAMITES_COBRE",
    "HOGARES-POSTVENTA_TRAMITES_FIBRA",
    "HOGARES-POSTVENTA_QUEJAS_RECURSOS_COBRE",
    "HOGARES-POSTVENTA_QUEJAS_RECURSOS_FIBRA_2",
    "HOGARES-POSTVENTA_PROCESO_EMPRESA-COS",
    "MIGRACIONES SOPORTE-COS",
    "CANCELACION-TOTAL_PLATINO",
    "HOGARES-SOPORTE_TECNICO_PLATINO",
    "HOGARES-SOPORTE_TECNICO_COBRE",
    "HOGARES-SOPORTE_TECNICO_FIBRA_2",
    "HOGARES-SOPORTE_FALLAS MASIVAS",
    "HOGARES-SOPORTE_TECNICO",
    "HOGARES_SOPORTE_PLATINO-COS",
    "CANCELACION-TOTAL_COBRE",
    "HOGARES-SOPORTE_TECNICO_AGENDADAS",
    "HOGARES-SOPORTE_TECNICO_DTV",
    "HOGARES-SOPORTE_TECNICO_WIFI",
    "MOVILES-POSTVENTA_PREPAGO",
    "MOVILES-POSTVENTA_PREPAGO_PERDIDA_ROBO",
    "PREPAGO_POSVENTA_COS",
    "MOVILES-POSTVENTA_POSPAGO_PERDIDA_ROBO",
    "CLIENTES_EMPRESAS_COS",
    "MOVILES-POSTVENTA_MOVILES_DEFAULT",
    "MOVILES-POSTVENTA_SIM_PREACTIVAS_750",
    "MOVILES-SOPORTE_PREPAGO",
    "MOVILES-POSTVENTA_POSPAGO",
    "OUTBOUND",
    "MOVILES-SOPORTE_POSPAGO",
    "ETB RECUPERACION",
    "T_HOGARES-POSTVENTA_TRASLADOS_COBRE",
    "ALL CAMPAIGNS"
]

print("Hi, what campaign status do you want to see?")
for i, option in enumerate(options, start=1):
    print(f"{i}. {option}")

choice = input("Enter the number of the campaign you want to see: ")

if choice.isdigit():
    choice = int(choice)
    if 1 <= choice <= len(options):
        
        selected_campaign = choice 
        print(f"You selected campaign number: {selected_campaign}")
        

        if selected_campaign == len(options):  
            rasterisk = "rasterisk -rx 'queue show' | sort"
        else:
            rasterisk = f"rasterisk -rx 'queue show q{selected_campaign}' | sort"  
        
        print("Generated command:", rasterisk)
    else:
        print("Invalid selection. Please enter a number from the list.")
else:
    print("Invalid input. Please enter a number.")




def colorize_state(state):
    if "Not in use" in state:
        return f"\033[1;32m{state}\033[0m"  # Verde
    elif "On Hold" in state:
        return f"\033[1;33m{state}\033[0m"  # Amarillo
    elif "Busy" in state:
        return f"\033[1;31m{state}\033[0m"  # Rojo
    else:
        return state  

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    print(f"Conectando a {SERVER_ID} como {USER_SERVER}...")
    ssh.connect(hostname=SERVER_ID, username=USER_SERVER, password=PASSWORD_SERVER)

    command = rasterisk
    stdin, stdout, stderr = ssh.exec_command(command)

    output = stdout.read().decode()
    print("Salida completa del comando antes de limpiar:")
    print(repr(output)) 

    ansi_escape = re.compile(r'\x1B\[.*?m')
    clean_output = ansi_escape.sub('', output)
    print("Salida limpia del comando:")
    print(clean_output)

    pattern = r"SIP/(\d+)\s+\((.*?)\)\s+\((.*?)\)"
    matches = re.findall(pattern, clean_output)

    # print(selected_campaign)
    
    if selected_campaign != 40:
        if matches:
            print("\nDatos extraídos:")
            for match in matches:
                extension, ringinuse_status, call_status = match
                colored_status = colorize_state(call_status)
                print(f"Extensión: {extension}, Ringinuse: {ringinuse_status}, Estado: {colored_status}")
        else:
            print("No se encontraron coincidencias.")
    
except paramiko.SSHException as e:
    print(f"Error en la conexión SSH: {e}")
finally:
    ssh.close()
    print("Conexión cerrada.")