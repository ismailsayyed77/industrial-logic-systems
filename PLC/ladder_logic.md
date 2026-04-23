# PLC Ladder Logic — Motor Starter Control

## Overview
This document describes the **ladder logic** used to control
an industrial motor starter using a PLC (Programmable Logic Controller).

The same Boolean logic from `boolean_logic.py` is represented
here in standard ladder diagram notation.

---

## I/O Mapping

| Tag          | Type   | Address | Description             |
|--------------|--------|---------|-------------------------|
| `PWR`        | Input  | I0.0    | Main power available    |
| `E_STOP`     | Input  | I0.1    | Emergency stop (N.C.)   |
| `OVERLOAD`   | Input  | I0.2    | Overload relay (N.C.)   |
| `TEMP_OK`    | Input  | I0.3    | Temp sensor within range|
| `START_PB`   | Input  | I0.4    | Start pushbutton (N.O.) |
| `STOP_PB`    | Input  | I0.5    | Stop pushbutton (N.C.)  |
| `MOTOR_RUN`  | Output | Q0.0    | Motor contactor coil    |
| `FAULT_LAMP` | Output | Q0.1    | Fault indicator lamp    |

---

## Ladder Logic Rungs

```
RUNG 1 — Motor Start / Self-Hold Circuit
──────────────────────────────────────────────────────────────
|                                                             |
|  [PWR]  [/E_STOP]  [/OVERLOAD]  [TEMP_OK]  [START_PB]     |
|───┤ ├────┤ /├────────┤ /├──────────┤ ├────────┤ ├──┐      |
|                                                    │  ( MOTOR_RUN )
|                                         [MOTOR_RUN]│      |
|─────────────────────────────────────────┤ ├────────┘      |
|   (Self-holding contact — latches motor ON after start)    |
──────────────────────────────────────────────────────────────

RUNG 2 — Fault Lamp (any fault condition lights the lamp)
──────────────────────────────────────────────────────────────
|                                                             |
|  [/PWR]                                                     |
|───┤ /├──────────────────────────────────────( FAULT_LAMP ) |
|                                                             |
|  [E_STOP]                                                   |
|───┤ ├───────────────────────────────────────( FAULT_LAMP ) |
|                                                             |
|  [OVERLOAD]                                                 |
|───┤ ├───────────────────────────────────────( FAULT_LAMP ) |
──────────────────────────────────────────────────────────────
```

**Legend:**
- `[ ]`  = Normally Open (NO) contact
- `[/]`  = Normally Closed (NC) contact
- `( )`  = Output coil

---

## Simplified Boolean Expression

```
MOTOR_RUN = PWR · (¬E_STOP) · (¬OVERLOAD) · TEMP_OK · (START_PB + MOTOR_RUN)
```

- `·` = AND
- `+` = OR
- `¬` = NOT

The `(START_PB + MOTOR_RUN)` part is the **self-holding latch**.
Once started, the motor keeps itself running without holding the start button.

---

## How to Simulate (Free Tool)

1. Download **OpenPLC Editor** → https://openplcproject.com/
2. Create a new project → choose "Ladder Diagram (LD)"
3. Map the I/O addresses from the table above
4. Draw each rung as shown
5. Compile and run simulation

No real PLC hardware needed!
