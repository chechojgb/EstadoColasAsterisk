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

def question_calls():
    while True:  # Bucle para manejar entradas no válidas
        for i, option in enumerate(options, start=1):
            print(f"{i}. {option}")

        choice = input("Enter the number of the campaign you want to see: ")

        if choice.isdigit():  # Verificar que la entrada sea un número
            choice = int(choice)
            if 1 <= choice <= len(options):  # Validar que la opción esté en el rango
                print(f"You selected campaign number: {choice}")

                # Generar el comando basado en la selección
                if choice == len(options):  # Si selecciona "ALL CAMPAIGNS"
                    return "rasterisk -rx 'queue show' | sort", choice
                else:  # Para las campañas individuales
                    return f"rasterisk -rx 'queue show q{choice}' | sort", choice
            else:
                print("Invalid selection. Please enter a number from the list.")
        else:
            print("Invalid input. Please enter a valid number.")







def execute_query(rasterisk, selected_campaign):

    def colorize_state(state):
        if "Not in use" in state:
            return f"\033[1;32m{state}\033[0m"  # Green
        elif "On Hold" in state:
            return f"\033[1;33m{state}\033[0m"  # Yellow
        elif "Busy" in state:
            return f"\033[1;31m{state}\033[0m"  # Red
        elif "in call" in state:
            return f"\033[1;34m{state}\033[0m"  # Blue
        else:
            return state

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        print(f"Connecting to {SERVER_ID} as {USER_SERVER}...")
        ssh.connect(hostname=SERVER_ID, username=USER_SERVER, password=PASSWORD_SERVER)

        stdin, stdout, stderr = ssh.exec_command(rasterisk)
        output = stdout.read().decode()

        # Limpieza de caracteres ANSI
        ansi_escape = re.compile(r'\x1B\[.*?m')
        clean_output = ansi_escape.sub('', output)

        # Patrones de extracción
        pattern = r"SIP/(\d+)\s+\((.*?)\)\s+\((.*?)\)"
        matches = re.findall(pattern, clean_output)

        queue_calls_pattern = r"^\s+\d+\.\s+SIP/\S+\s+\(.*?\)"
        queue_calls = re.findall(queue_calls_pattern, clean_output, re.MULTILINE)

        members_pattern = r"^Q\d+\s+.*?strategy.*?$"
        members_summary = re.findall(members_pattern, clean_output, re.MULTILINE)

        # print(output)


        if queue_calls:
            print("\nCalls in Queue:")
            for call in queue_calls:
                print(call, "\n")
        else:
            print("Calls in Queue:\n    No calls in queue found.\n")


        filtered_matches = [match for match in matches if match[2] != "Unavailable"]

        if selected_campaign != len(options):
            if filtered_matches:
                print("Connected agents (filtered):")
                for match in filtered_matches:
                    extension, ringinuse_status, call_status = match
                    colored_status = colorize_state(call_status)
                    print(f"    Extension: {extension}, State: {colored_status}")
            else:
                print(f"Agents Found:\n\n    No agent found online for Q{selected_campaign}.")
                

        if selected_campaign != len(options):
            if members_summary:
                print("\nQueue Members Summary:")
                for summary in members_summary:
                    print("\n   ", summary)
            else:
                print("\nNo members summary found.")
        else:
            print("\nQueue Members Summary:")
            for summary in members_summary:
                print(summary)

    except paramiko.SSHException as e:
        print(f"Connection error SSH: {e}")
    finally:
        ssh.close()
        print("\nConnection closed.")

while True:
    rasterisk, selected_campaign = question_calls()
    execute_query(rasterisk, selected_campaign)

    while True:
        repeat = input("Do you want to make another query? 1=yes ")
        if repeat == "1":
            break  
        else:
            print("Invalid input or option not allowed. Please enter 1 to continue.")