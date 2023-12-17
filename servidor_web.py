import network
import socket
from time import sleep
import machine
from machine import Pin

ssid = 'tu_ssid'
password = 'tu_password'

CH1 = Pin(20, Pin.OUT)
CH2 = Pin(21, Pin.OUT)
CH3 = Pin(22, Pin.OUT)

def CH1_ON():
    CH1.value(1)
    
def CH1_OFF():
    CH1.value(0)

def CH2_ON():
    CH2.value(1)
    
def CH2_OFF():
    CH2.value(0)
    
def CH3_ON():
    CH3.value(1)
    
def CH3_OFF():
    CH3.value(0)

    
def conectar():
    red = network.WLAN(network.STA_IF)
    red.active(True)
    red.connect(ssid, password)
    while red.isconnected() == False:
        print('Conectando ...')
        sleep(1)
    ip = red.ifconfig()[0]
    print(f'Conectado con IP: {ip}')
    return ip
    
def open_socket(ip):
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

def pagina_web():
    html = f"""
            <!DOCTYPE html>
            <html>
            <head>
            </head>
            <body>
            <center>
            <table>
            <tr>
            <th>CH1</th>
            <th>CH2</th>
            <th>CH3</th>
            </tr>
            <tr>
            <td><form action="./CH1_ON">
            <input type="submit" value="ON" style="background-color: #FF0000; border-radius: 15px; height:120px; width:120px; border: none; color: white; padding: 16px 24px; margin: 4px 2px"/>
            </form></td>
            <td><form action="./CH2_ON">
            <input type="submit" value="ON" style="background-color: #FF0000; border-radius: 15px; height:120px; width:120px; border: none; color: white; padding: 16px 24px; margin: 4px 2px"/>
            </form></td>
            <td><form action="./CH3_ON">
            <input type="submit" value="ON" style="background-color: #FF0000; border-radius: 15px; height:120px; width:120px; border: none; color: white; padding: 16px 24px; margin: 4px 2px"/>
            </form></td>
            </tr>
            <tr>
            <td><form action="./CH1_OFF">
            <input type="submit" value="OFF" style="background-color: #04AA6D; border-radius: 15px; height:120px; width:120px; border: none; color: white; padding: 16px 24px; margin: 4px 2px"/>
            </form></td>
            <td><form action="./CH2_OFF">
            <input type="submit" value="OFF" style="background-color: #04AA6D; border-radius: 15px; height:120px; width:120px; border: none; color: white; padding: 16px 24px; margin: 4px 2px"/>
            </form></td>
            <td><form action="./CH3_OFF">
            <input type="submit" value="OFF" style="background-color: #04AA6D; border-radius: 15px; height:120px; width:120px; border: none; color: white; padding: 16px 24px; margin: 4px 2px"/>
            </form></td>
            </tr>
            </table>
            </center>
            </body>
            </html>
            """
    return str(html)

def serve(connection):
    while True:
        cliente = connection.accept()[0]
        peticion = cliente.recv(1024)
        peticion = str(peticion)
        try:
            peticion = peticion.split()[1]
        except IndexError:
            pass
        if peticion == '/CH1_ON?':
            CH1_ON()
        elif peticion =='/CH1_OFF?':
            CH1_OFF()
        elif peticion =='/CH2_ON?':
            CH2_ON()
        elif peticion =='/CH2_OFF?':
            CH2_OFF()
        elif peticion =='/CH3_ON?':
            CH3_ON()
        elif peticion =='/CH3_OFF?':
            CH3_OFF()
        html = pagina_web()
        cliente.send(html)
        cliente.close()

try:
    ip = conectar()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    pass

    