import socket
import sys
import time
import struct
import datetime


'''
Clase de bot de mirai
'''
class miraibot:
    
    BUFF_SIZE = 1024

    def __init__(self,server,port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        self.port = port
    
    # Conectar y hacer el handshake
    def connect(self):
        try:
            self.socket.connect((self.server, self.port))
            # handshake
            self.socket.send(b"\x00\x00\x00\x01")
            time.sleep(0.2)
            self.socket.send(b"\x00")
            return 0
        except Exception as e:
            print("Error:", e)
            return 1
    
    # Ping al servidor
    def ping(self):
        try:
            self.socket.send(b"\x00\x00")
            time.sleep(0.2)
            ping = self.socket.recv(2)
            # Si es un ping normal
            if ping == b"\x00\x00":
                return 0
            else:
                data = self.socket.recv(self.BUFF_SIZE)
                return data
        except Exception as e:
            print("Error:", e)
            return -1

    def parseResponse(self,data):
        # Leer la duración (uint32_t)
        duration = struct.unpack("!I", data[:4])[0]
        data = data[4:]

        # Leer el tipo de ataque (uint8_t)
        attack_type = struct.unpack("!B", data[:1])[0]
        data = data[1:]

        # Leer el número de objetivos (uint8_t)
        num_targets = struct.unpack("!B", data[:1])[0]
        data = data[1:]

        targets = []
        # Leer los objetivos
        for _ in range(num_targets):
            target = {}
            target["addr"] = struct.unpack("!I", data[:4])[0]
            target["netmask"] = struct.unpack("!B", data[4:5])[0]
            targets.append(target)
            data = data[5:]

        # Leer el número de opciones (uint8_t)
        num_options = struct.unpack("!B", data[:1])[0]
        data = data[1:]

        options = []
        # Leer las opciones
        for _ in range(num_options):
            option = {}
            option["key"] = struct.unpack("!B", data[:1])[0]
            data = data[1:]
            #Size of data
            aux_size = struct.unpack("!B", data[:1])[0]
            data = data[1:]
            #Get data
            option["val"] = data[:aux_size].decode()
            data = data[aux_size:]
            options.append(option)

        # Imprimir los resultados
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(" Timestamp:   {}".format(timestamp))
        print(" Duration:    ", duration)
        print(" Type:        ", self._getTypeAttack(attack_type))
        print(" Obj number:  ", num_targets)
        for target in targets:
            print("    IP:      ", socket.inet_ntoa(struct.pack("!I", target['addr'])))
            print("    Netmask:", target['netmask'])
        print(" Opt number:  ", num_options)
        for opt in options:
            print(f"    > {self._getTypeOpt(opt['key'])}: {opt['val']}")
    

    def _getTypeAttack(self,numero):
        switcher = {
            0: "ATK_VEC_UDP (Straight up UDP flood)",
            1: "ATK_VEC_VSE (Valve Source Engine query flood)",
            2: "ATK_VEC_DNS (DNS water torture)",
            3: "ATK_VEC_SYN (SYN flood with options)",
            4: "ATK_VEC_ACK (ACK flood)",
            5: "ATK_VEC_STOMP (ACK flood to bypass mitigation devices)",
            6: "ATK_VEC_GREIP (GRE IP flood)",
            7: "ATK_VEC_GREETH (GRE Ethernet flood)",
            8: "ATK_VEC_PROXY (Proxy knockback connection)",
            9: "ATK_VEC_UDP_PLAIN (Plain UDP flood optimized for speed)",
            10: "ATK_VEC_TCP_RANDSIZE (TCP time variable-sized packets)",
            11: "ATK_VEC_UDP_RANDSIZE (UDP time variable-sized packets)",
            12: "ATK_VEC_TCP_STREAM (TCP strema custom)",
            13: "ATK_VEC_TCP_ACK_CUSTOM (TCP custom flex)",
            14: "ATK_VEC_TCP_SSH (TCP ssh attack)",
            15: "ATK_VEC_HTTP (HTTP layer 7 flood)",
            16: "ATK_VEC_UDP_CUSTOM (UDP whith IP spoof)",
            17: "ATK_VEC_TCP_FRAG (TCP fragmentation)"
            }
        return switcher.get(numero, "[NOT FOUND]")

    def _getTypeOpt(self,numero):
        switcher = {
            0: "ATK_OPT_PAYLOAD_SIZE",
            1: "ATK_OPT_PAYLOAD_RAND",
            2: "ATK_OPT_IP_TOS",
            3: "ATK_OPT_IP_IDENT",
            4: "ATK_OPT_IP_TTL",
            5: "ATK_OPT_IP_DF",
            6: "ATK_OPT_SPORT",
            7: "ATK_OPT_DPORT",
            8: "ATK_OPT_DOMAIN",
            9: "ATK_OPT_DNS_HDR_ID",
            11: "ATK_OPT_URG",
            12: "ATK_OPT_ACK",
            13: "ATK_OPT_PSH",
            14: "ATK_OPT_RST",
            15: "ATK_OPT_SYN",
            16: "ATK_OPT_FIN",
            17: "ATK_OPT_SEQRND",
            18: "ATK_OPT_ACKRND",
            19: "ATK_OPT_GRE_CONSTIP",
            20: "ATK_OPT_METHOD",
            21: "ATK_OPT_POST_DATA",
            22: "ATK_OPT_PATH",
            23: "ATK_OPT_HTTPS",
            24: "ATK_OPT_CONNS",
            25: "ATK_OPT_SOURCE",
            }
        return switcher.get(numero, "[NOT FOUND]")

class CargandoBonito:

    def __init__(self):
        self.width = 50
        self.position = 0
        self.direction = 1

    def ping(self):
        sys.stdout.write("\r [{}{}]".format('-' * self.position, '█' + '-' * (self.width - self.position - 1)))  # Imprimir la barra de carga
        sys.stdout.flush()  # Forzar la salida inmediata

        # Actualizar la posición del bloque
        self.position += self.direction
        if self.position >= self.width - 1:
            self.direction = -1
        elif self.position <= 0:
            self.direction = 1


def banner(server, port):
    print("\n\033[1;31m")
    print(" ----------------------------------------------\033[0m\033[1;36m")
    print("    ___  ____           _ _____             ")
    print("    |  \\/  (_)         (_)  ___|            ")
    print("    | .  . |_ _ __ __ _ _\\ `--. _ __  _   _ ")
    print("    | |\\/| | | '__/ _` | |`--. \\ '_ \\| | | |")
    print("    | |  | | | | | (_| | /\\__/ / |_) | |_| |")
    print("    \\_|  |_/_|_|  \\__,_|_\\____/| .__/ \\__, |")
    print("                               | |     __/ |")
    print("                               |_|    |___/ ")
    print("\033[0m\033[1;31m ----------------------------------------------")
    print("\033[0m                                     @DannyDB")
    print("")
    print(" [-] Ip:   {}".format(server))
    print(" [-] Port: {}".format(port))
    print("\n")

def main(server, port):

    bot = miraibot(server, port)
    #bot.parseResponse(cadena_hex)
    #bot.parseResponse(data)
    #return

    #El cargador bonito
    car = CargandoBonito()
    #Banner
    banner(server, port)
    # Instancia el bot
    bot = miraibot(server, port)
    # Conexion
    print(" [*] Conectado a {}:{}".format(server, port))
    if bot.connect() == 1:
        sys.exit(-1)
    print(" [-] Conectado!")
    print("")
    while 1:
        # Ping
        data = bot.ping()
        if data == -1:
            sys.exit(-1)
        elif data == 0:
            pass #just a ping
        else:
            print ("\n")
            print(" [!] NEW DATA!!")
            print(" -----------------------------------------------")
            bot.parseResponse(data)
            print(" -----------------------------------------------")
            print(" Raw: ",data.hex())
            print(" -----------------------------------------------")
            print("\n")
        # Espera
        for _ in range(20):
            car.ping()
            time.sleep(0.5)
    


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python script.py <server_addr> [port]")
        sys.exit(1)
    
    server = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 21425

    main(server, port)
