# sudo apt update
# sudo apt install pigpio
# sudo systemctl start pigpiod

import pigpio
import pynmea2
import time

# Software-UART-Pins definieren
RX_PIN = 21  # GPIO21 (Pin 40)
TX_PIN = 20  # GPIO20 (Pin 38)

# Baudrate des GPS-Moduls (in der Regel 9600)
BAUD_RATE = 9600

# Verbindung zu pigpio starten
pi = pigpio.pi()
if not pi.connected:
    print("Fehler: pigpio Daemon nicht gestartet.")
    exit()

# Software-UART auf den definierten Pins öffnen
pi.bb_serial_read_open(RX_PIN, BAUD_RATE)
print(f"Software UART auf RX: GPIO{RX_PIN}, TX: GPIO{TX_PIN} gestartet.")

try:
    while True:
        # GPS-Daten vom RX-Pin lesen
        (count, data) = pi.bb_serial_read(RX_PIN)
        if count > 0:
            try:
                # GPS-Daten in ASCII dekodieren
                message = data.decode("ascii", errors="replace")
                
                # NMEA-Datensätze verarbeiten
                for line in message.splitlines():
                    if line.startswith("$GPGGA"):  # GGA-Datensatz enthält Standortdaten
                        parsed = pynmea2.parse(line)
                        print(f"Latitude: {parsed.latitude}, Longitude: {parsed.longitude}, Höhe: {parsed.altitude}m")
            except pynmea2.ParseError as e:
                print(f"Fehler beim Parsen: {e}")
        
        # Kurze Pause, um die CPU-Auslastung zu reduzieren
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nBeende Programm...")

finally:
    # Software-UART schließen und Ressourcen freigeben
    pi.bb_serial_read_close(RX_PIN)
    pi.stop()
    print("Software UART beendet.")
