import socket
import threading
import sys

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

username = input("Masukkan username kamu: ")

def receive_messages():
    """Fungsi ini berjalan di background untuk terus mendengarkan pesan masuk."""
    while True:
        try:
            data, _ = client_socket.recvfrom(1024)
            sys.stdout.write('\r' + ' ' * 50 + '\r') 
            print(f"{data.decode('utf-8')}")
            sys.stdout.write("Pesan: ") 
            sys.stdout.flush()
        except Exception as e:
            print(f"\n[!] Koneksi terputus. Detail: {e}")
            break

intro_message = f"--- {username} telah bergabung ke obrolan ---"
client_socket.sendto(intro_message.encode('utf-8'), (SERVER_HOST, SERVER_PORT))

receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True
receive_thread.start()

print("Terhubung ke server! Ketik 'exit' untuk keluar.\n")

while True:
    try:
        message = input("Pesan: ")
        
        if message.lower() == 'exit':
            exit_msg = f"--- {username} telah meninggalkan obrolan ---"
            client_socket.sendto(exit_msg.encode('utf-8'), (SERVER_HOST, SERVER_PORT))
            break
            
        full_message = f"[{username}]: {message}"
        client_socket.sendto(full_message.encode('utf-8'), (SERVER_HOST, SERVER_PORT))
        
    except KeyboardInterrupt:
        break

print("Keluar dari program.")
client_socket.close()
sys.exit()