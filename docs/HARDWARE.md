# Hardware

## Components

| Item | Notes |
|---|---|
| Raspberry Pi 4 Model B | Runs Gammu and the Python service |
| SIM800L (HW-748 board) | GSM modem. Firmware seen: `1418B04SIM800L24` |
| SIM card | Tested on Ooredoo Algeria (network name `Nedjma`) |
| Power supply for SIM800L | See below |
| Jumper wires | UART and ground |

## Serial port

The modem is reached through `/dev/serial0` (which points to `/dev/ttyS0` on this setup).

## Wiring

> **TODO (fill in from your real circuit before publishing).** Do not publish a guessed table.

| SIM800L pin | Connected to |
|---|---|
| TXD | Raspberry Pi RXD (GPIO15, physical pin 10) |
| RXD | Raspberry Pi TXD (GPIO14, physical pin 8), through a level shifter or divider |
| GND | Raspberry Pi GND **and** power-supply GND (common ground) |
| VCC | External supply, see below |

Rule: TX goes to RX and RX goes to TX (crossed). Verify the logic level of your board before connecting.

## Power

The SIM800L is the most common source of problems:

- Supply voltage: about **3.4 V to 4.4 V** (typically 4.0 V).
- It draws current bursts of **up to ~2 A** during transmission.
- Do **not** power it from the Pi's 3.3 V pin. The 5 V pin is also unsuitable without a proper regulator.
- Use a battery or a dedicated regulator able to supply the peaks, and add a large capacitor (about 470 µF to 1000 µF) near the module.
- Symptoms of weak power: random resets, no network registration, SMS sending failures.

Document your actual supply here: `TODO (battery / regulator model, voltage, capacitor)`.

## Verifying the modem

```bash
gammu identify
```

Expected: manufacturer `SIMCOM_Ltd`, model `SIM800L`.

## Enabling UART on Raspberry Pi OS

```bash
sudo raspi-config
# Interface Options > Serial Port
#   Login shell over serial: No
#   Serial port hardware enabled: Yes
```