# TFG_-Surgical_Instrument_Server
SIS

Aquest projecte de Treball de Fi de Grau consisteix en el desenvolupament d’un sistema capaç de reconèixer objectes mitjançant visió artificial i controlar un robot UR3 utilitzant comandes de veu. El sistema integra reconeixement d’imatge, control robòtic via MODBUS i detecció d’ordres per micròfon, amb aplicació pensada per a entorns quirúrgics simulats.

Les ordres orals són captades per un micròfon i interpretades per un script Python, que actua com a servidor MODBUS. Si es detecta un objecte esperat (ex. pinces, tisores o ganivet), el sistema envia les coordenades de l’objecte al robot, que actua en conseqüència.

---

## Estructura del repositori

- `docs/`: Manuals d’instal·lació i ús amb imatges pas a pas.
- `media/`: Vídeos i captures de la demostració.
- `src/`: Scripts de Python (reconeixement d’objectes i veu, servidor MODBUS).
- `program_ur/`: Fitxers `.urp` per carregar al robot UR3.
- `README.md`: Aquest document.

---

## Requeriments

### Llenguatges i llibreries
- **Python 3.12**
- Llibreries:
  - `speech_recognition`
  - `pyaudio`
  - `opencv-python`
  - `modbus_tk` o `pymodbus`
  - `numpy`

### Hardware i entorns
- **Robot UR3** amb consola teach pendant.
- **Micròfon USB** o integrat.
- **Càmera** per a visió artificial.
- **Ordinador** amb entorn Python i ports oberts per MODBUS TCP.
- **Sistema operatiu**: Windows o Linux.

---

## Instal·lació

### 1. Carrega del programa al robot
- Inserir el fitxer `.urp` al robot mitjançant USB.
- Obrir el fitxer des de l’opció `Open > Program > usbdisk`.
- Fer clic sobre el `.urp` per carregar-lo al sistema.
- Inicialitzar el robot amb el botó `ON`, després `START`.

### 2. Configuració de xarxa
- Anar a `Settings > System > Network` al teach pendant.
- Assignar IP estàtica (ex. `84.88.129.176`) dins la mateixa subxarxa que l’ordinador.
- Comprovar que l'ordinador i el robot poden comunicar-se via ping.

### 3. Configuració MODBUS
- Anar a `Installation > Fieldbus > MODBUS`.
- Afegir unitats amb IP del servidor (ordinador) i assignar registres de sortida.
- Comprovar que els cercles de connexió apareixen en **verd** un cop el servidor està actiu.

---

## Llançament del sistema

1. Executar l’script `codi_final.py`:
    ```bash
    python codi_final.py
    ```
   - Ha d’aparèixer: `Servidor MODBUS activo...` i `Voice listening activated`.

2. Iniciar el programa `.urp` al teach pendant.
3. La càmera comença a buscar objectes, mentre el micròfon espera comandes de veu.

---

## Ús del sistema

- El sistema buscarà objectes com **"tijeras"**, **"pinzas"**, **"cuchillo"**.
- Si es detecta una paraula clau i un objecte associat, s'enviaran:
  - Les coordenades X, Y de l’objecte.
  - Un bit flag que activa el moviment del robot.
- Si el robot rep el senyal, es mourà cap a l’objecte detectat.

> 💡 Per assegurar que la connexió MODBUS està activa, revisa el camp `Fieldbus > MODBUS` del teach pendant. Els cercles verds indiquen connexió correcta.

---

## Finalització

- Pots interrompre el sistema en qualsevol moment tancant el terminal Python o desconnectant la sessió MODBUS.
- El robot es pot aturar manualment des del teach pendant.

---

## Autoria

**Nom**: NIL LESLIE BOKESA SALOMÓN  
**Grau**: Enginyeria Biomèdica  
**Universitat**: Universitat de Girona  
**Curs**: 2024–2025  
**Tutor/a**: Xavier Cufí Solé  
**Suport docent adicional**: Professor Esteve-Amadeu Hernandez Uptegrove i Arnau Oliver

---

## Llicència

Aquest projecte es distribueix sota la llicència MIT. Ets lliure de copiar, modificar i distribuir el codi sempre que es mantingui el crèdit a l’autor original.
