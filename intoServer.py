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




ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    print(f"Conectando a {SERVER_ID} como {USER_SERVER}...")
    ssh.connect(hostname=SERVER_ID, username=USER_SERVER, password=PASSWORD_SERVER)

    # Ejecutar el comando
    command = rasterisk
    stdin, stdout, stderr = ssh.exec_command(command)

    # Obtener la salida y procesarla
    output = stdout.read().decode()  # La salida del comando
    print("Salida del comando:")
    print(output)  # Imprimir para verificar si tiene la información esperada

    error = stderr.read().decode()

    if error:
        print("Errores:")
        print(error)
    
    # Filtrar las líneas que contienen los valores que necesitamos (número y estado)
    pattern = r"(\d+)\s+\((.*?)\)\s+\((.*?)\)"  # Captura ambos paréntesis
    matches = re.findall(pattern, output)  # Encuentra todas las coincidencias

    if matches:
        print("Datos extraídos:")
        for match in matches:
            queue_number = match[0]  # Número de la cola
            queue_state = match[1]   # Estado del primer paréntesis
            queue_status = match[2]  # Estado del segundo paréntesis
            print(f"Cola: {queue_number}, Estado: {queue_state}, Estado adicional: {queue_status}")
    else:
        print("No se encontraron coincidencias.")

except paramiko.SSHException as e:
    print(f"Error en la conexión SSH: {e}")
finally:
    ssh.close()
    print("Conexión cerrada.")