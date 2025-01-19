import paramiko
import re
import os
from dotenv import load_dotenv
import mysql.connector


load_dotenv()
# Server Access Credentials
USER_SERVER = os.getenv('USER_SERVER')
PASSWORD_SERVER = os.getenv('PASSWORD_SERVER')
SERVER_ID = os.getenv('SERVER_ID')
# DB Access Credentials
USER_DB=os.getenv('USER_DB')
PASSWORD_DB=os.getenv('PASSWORD_DB')
SERVER_ID_DB=os.getenv('SERVER_ID_DB')

# Conect to BD
print("SERVER_ID_DB:", SERVER_ID_DB)



def get_user_info_by_extension(extension):
    conn = mysql.connector.connect(
        host=SERVER_ID_DB,
        user=USER_DB,
        password=PASSWORD_DB,
        database='miosv2-phone'
    )
    cursor = conn.cursor()
    consulta = "SELECT x.* FROM `miosv2-phone`.usersv2 x WHERE extension = %s"
    cursor.execute(consulta, (extension,))

    user_info = cursor.fetchone()
    # print(user_info)
    conn.close()

    return user_info

def get_call_info_by_user_id(user_id):
    conn = mysql.connector.connect(
        host=SERVER_ID_DB,
        user=USER_DB,
        password=PASSWORD_DB,
        database='miosv2-phone'
    )
    cursor = conn.cursor()
    consulta = "SELECT x.* FROM `miosv2-phone`.calls x WHERE user_id = %s ORDER BY x.`start` DESC"
    cursor.execute(consulta, (user_id,))

    user_info = cursor.fetchone()
    # print(user_info)
    conn.close()

    return user_info



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
    while True: 
        for i, option in enumerate(options, start=1):
            print(f"{i}. {option}")

        choice = input("Enter the number of the campaign you want to see: ")

        if choice.isdigit():  
            choice = int(choice)
            if 1 <= choice <= len(options): 
                print(f"You selected campaign number: {choice}")

                if choice == len(options):  
                    return "rasterisk -rx 'queue show' | sort", choice
                else:  
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
        elif "Ringing" in state:
            return f"\033[1;35m{state}\033[0m"  # Purple
        elif "Call in progress" in state:
            return f"\033[1;32m{state}\033[0m"  # Green
        else:
            return state
    def colorize_call_state(call_state):
        if call_state == "Call in progress":
            return f"\033[1;32m{call_state}\033[0m"  # Green
        elif call_state == "Call finished":
            return f"\033[1;31m{call_state}\033[0m"  # Red
        else:
            return call_state

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
                print(call)
        else:
            print("Calls in Queue:\n    No calls in queue found.\n")

        filtered_matches = [match for match in matches if match[2] != "Unavailable"]

        if selected_campaign != len(options):
            if filtered_matches:
                print(f"\nConnected agents (filtered):")
                for match in filtered_matches:
                    extension, ringinuse_status, call_status = match
                    
                    # Primera consulta: Información del usuario
                    user_info = get_user_info_by_extension(extension)
                    if user_info:
                        user_id = user_info[0]
                        name = user_info[8]
                        document = user_info[7]
                        
                        call_info = get_call_info_by_user_id(user_id)
                        
                        if call_info:
                            call_id = call_info[0]  
                            call_state = call_info[10]
                            
                            if call_state is None: call_state = "Call in progress"
                            else: call_state = "Call finished"

                            colored_status = colorize_state(call_status)
                            colored_call_state = colorize_call_state(call_state)
                            print(f"    Extension: {extension}, Name: {name}, Call ID: {call_id}, Call State: {colored_call_state}, State: {colored_status}")
                        else:
                            print(f"    Extension: {extension}, Name: {name}, Document: {document}, No call info found, State: {call_status}")
                    else:
                        print(f"    Extension: {extension}, State: {call_status}, User Info not found.")
            else:
                print(f"\nConnected agents (filtered):\n\n    No agents Connected")
                
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