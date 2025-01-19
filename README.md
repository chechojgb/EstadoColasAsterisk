# Campaña de Monitoreo de Llamadas

Este script permite consultar el estado de las campañas de llamadas y agentes conectados en una infraestructura Asterisk, utilizando Python para realizar consultas SSH y acceder a una base de datos MySQL.

## Requisitos previos

<ol>
  <li>
    <strong>Instalación de dependencias</strong>
    <p>Asegúrate de tener instalados los siguientes módulos de Python:</p>
    <ul>
      <li><code>paramiko</code>: Para realizar conexiones SSH.</li>
      <li><code>mysql-connector-python</code>: Para conectarte a MySQL.</li>
      <li><code>python-dotenv</code>: Para cargar las credenciales desde un archivo <code>.env</code>.</li>
    </ul>
    <p>Instala las dependencias ejecutando:</p>
    <pre><code>pip install paramiko mysql-connector-python python-dotenv</code></pre>
  </li>
  <li>
    <strong>Archivo <code>.env</code></strong>
    <p>Crea un archivo <code>.env</code> en el directorio raíz del proyecto y define las siguientes variables:</p>
    <pre><code>
# Credenciales del servidor Asterisk
USER_SERVER=<tu_usuario_asterisk>
PASSWORD_SERVER=<tu_password_asterisk>
SERVER_ID=<tu_ip_asterisk>

# Credenciales de la base de datos
USER_DB=<tu_usuario_bd>
PASSWORD_DB=<tu_password_bd>
SERVER_ID_DB=<tu_ip_bd>
    </code></pre>
  </eso>
  <eso>
    <fuerte>Base de datos y tablas necesarias</fuerte>
    <PAG>Asegúrate de tener configuradas las tablas  usersv2  Y  LLAMADAS  en la base de datos  miosv2-phone . Este script asume las siguientes estructuras:</PAG>
    <ul>
      <eso><fuerte>Tabla  usersv2></fuerte>: Contiene información de los usuarios, identificados por su extensión.</eso>
      <eso><fuerte>Tabla  LLAMADAS></fuerte>: Registra las llamadas realizadas por los usuarios.</eso>
    </ul>
  </eso>
</viejo>

## Uso del script

<viejo>
  <eso>
    <fuerte>Seleccionar una campaña</fuerte>
    <PAG>Al ejecutar el script, se te mostrará una lista numerada de campañas. Ingresa el número correspondiente a la campaña que deseas consultar.</PAG>
  </eso>
  <eso>
    <fuerte>Estado de las campañas</fuerte>
    <PAG>El script mostrará los siguientes datos:</PAG>
    <ul>
      <eso><fuerte>Llamadas en cola</fuerte>: Llamadas pendientes por ser atendidas en la campaña seleccionada.</eso>
      <eso><fuerte>Agentes conectados</fuerte>: Usuarios conectados con información detallada sobre su estado de llamadas.</eso>
    </ul>
  </eso>
  <eso>
    <fuerte>Colores del estado</fuerte>
    <PAG>El estado de las llamadas y de los agentes se resalta en la terminal con colores para facilitar su visualización:</PAG>
    <ul>
      <eso><durar Estilo="color: verde;">Verde</durar>: <Código>No en uso</Código>, <Código>Llamada en curso</Código>.</eso>
      <eso><durar Estilo="color: amarillo;">Amarillo</durar>: <Código>En espera</Código>.</eso>
      <eso><durar Estilo="color: rojo;">Rojo</durar>: <Código>Ocupado</Código>, <Código>Llamada finalizada</Código>.</eso>
      <eso><durar Estilo="color: azul;">Azul</durar>: <Código>en llamada</Código>.</eso>
      <eso><durar Estilo="color: morado;">Morado</durar>: <Código>Zumbido</Código>.</eso>
    </ul>
  </eso>
  <eso>
    <fuerte>Hacer otra consulta</fuerte>
    <PAG>Al finalizar una consulta, el script te preguntará si deseas realizar otra. Ingresa <Código>1</Código> para continuar o cualquier otra tecla para salir.</PAG>
  </eso>
</viejo>
