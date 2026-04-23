"""
Boolean Logic for Motor Interlock System
==========================================
Implements simplified Boolean switching logic
for industrial motor starter control.

Author: Maaz
Project: Industrial Logic & Systems Analysis
"""

import itertools


# ─── INTERLOCK LOGIC ───────────────────────────────────────
def motor_interlock(power: bool, emergency_stop: bool,
                    overload: bool, temp_ok: bool) -> tuple[bool, str]:
    """
    Simplified Boolean interlock for motor starter.

    Logic: START = Power AND (NOT E_Stop) AND (NOT Overload) AND Temp_OK

    Args:
        power         : Main power supply available
        emergency_stop: Emergency stop button pressed
        overload      : Overload relay tripped
        temp_ok       : Temperature within safe range

    Returns:
        (should_start, reason_message)
    """
    conditions = {
        "Power Available"    : power,
        "E-Stop Clear"       : not emergency_stop,
        "Overload Clear"     : not overload,
        "Temperature Safe"   : temp_ok,
    }

    failed = [name for name, state in conditions.items() if not state]

    if not failed:
        return True, "✅  MOTOR START — All interlock conditions satisfied"
    else:
        return False, f"🔴  MOTOR BLOCKED — Failed: {', '.join(failed)}"


# ─── TRUTH TABLE ───────────────────────────────────────────
def print_truth_table():
    """Print full truth table for all 16 input combinations."""
    headers = ["PWR", "E-STP", "OVLD", "TEMP_OK", "OUTPUT"]
    print("\n" + "─" * 50)
    print("  MOTOR INTERLOCK TRUTH TABLE")
    print("─" * 50)
    print(f"  {'  '.join(headers)}")
    print("─" * 50)

    for combo in itertools.product([0, 1], repeat=4):
        p, e, o, t = combo
        result, _ = motor_interlock(bool(p), bool(e), bool(o), bool(t))
        out = "1 (RUN)" if result else "0 (OFF)"
        print(f"  {p}    {e}      {o}     {t}       {out}")

    print("─" * 50)
    print("  PWR=Power  E-STP=EmergStop  OVLD=Overload\n")


# ─── SCENARIO TESTS ────────────────────────────────────────
def run_scenarios():
    """Test real-world fault scenarios."""
    scenarios = [
        {
            "name"   : "Normal Operation",
            "inputs" : (True, False, False, True),
            "expect" : True
        },
        {
            "name"   : "Emergency Stop Pressed",
            "inputs" : (True, True, False, True),
            "expect" : False
        },
        {
            "name"   : "Overload Relay Tripped",
            "inputs" : (True, False, True, True),
            "expect" : False
        },
        {
            "name"   : "Temperature Overheating",
            "inputs" : (True, False, False, False),
            "expect" : False
        },
        {
            "name"   : "Power Failure",
            "inputs" : (False, False, False, True),
            "expect" : False
        },
        {
            "name"   : "Multiple Faults (E-Stop + Overload)",
            "inputs" : (True, True, True, True),
            "expect" : False
        },
    ]

    print("\n" + "─" * 55)
    print("  SCENARIO TEST RESULTS")
    print("─" * 55)

    passed = 0
    for s in scenarios:
        result, msg = motor_interlock(*s["inputs"])
        status = "PASS ✓" if result == s["expect"] else "FAIL ✗"
        if result == s["expect"]:
            passed += 1
        print(f"  [{status}]  {s['name']}")
        print(f"          {msg}\n")

    print(f"  Tests passed: {passed}/{len(scenarios)}")
    print("─" * 55)


# ─── MAIN ──────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("  Boolean Logic — Motor Interlock System")
    print("=" * 55)

    print_truth_table()
    run_scenarios()
