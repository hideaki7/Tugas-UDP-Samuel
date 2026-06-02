import socket

PORT = 5000

def get_local_ip():
    """Trik untuk mendeteksi IP Address Wi-Fi/LAN laptop secara otomatis."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

print("="*40)
print("  PENGATURAN JARINGAN SERVER UDP")
print("="*40)
print("Pilih mode jaringan:")
print("1. Localhost")
print("2. Jaringan Publik / Wi-Fi")
pilihan = input("\nMasukkan pilihan (1 atau 2): ")

if pilihan == '2':
    HOST = '0.0.0.0'
    display_ip = get_local_ip()
    print(f"\n[*] Mode Jaringan Publik diaktifkan.")
    print(f"[*] KASIH TAHU CLIENT UNTUK MENGISI SERVER_HOST DENGAN: {display_ip}")
else:
    HOST = '127.0.0.1'
    display_ip = '127.0.0.1'
    print(f"\n[*] Mode Localhost diaktifkan.")
    print(f"[*] Client harus menggunakan SERVER_HOST: 127.0.0.1")

print("="*40)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))
clients = set()

print(f"\n[*] Server UDP sedang berjalan...")
print(f"[*] Menunggu pesan dari client...\n")

while True:
    try:
        data, address = server_socket.recvfrom(1024)
        
        if address not in clients:
            clients.add(address)
            print(f"[+] Client baru bergabung dari: {address}")

        message = data.decode('utf-8')
        print(f"Log Server -> Diterima dari {address}: {message}")

        for client in clients:
            if client != address:
                server_socket.sendto(data, client)
                
    except ConnectionResetError:
        pass
    except KeyboardInterrupt:
        print("\n[*] Server dimatikan.")
        break
    except Exception as e:
        print(f"[!] Error: {e}")