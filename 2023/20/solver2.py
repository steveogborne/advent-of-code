import os
# Problem scope
'''
Pulse propagation
Modules are connected. Signals are sent. Modules have behaviours. Output signals need to be recorded and captured

Modules:
Button: fundamental input: sends one low pulse to the broadcaster.
Wait until all modules are stable before pressing again

Broadcaster: on recieving a pulse sends same pulse to all recipients

Flip-flop: starts off. Prefix %
Ignores high pulse
If recieves a low pulse: flips on/off.
If flipping on sends high pulse
If flipping off sends low pulse

Conjunction. Prefix &
Store last recieved signals to inputs. Defaults low
Recieved pulses get stored in memory then register is checked
If all memory is high: send low pulse, otherwise send high pulse
'''

# Solution sketch
'''
Preload machines by parsing input files and creating objects in an array.
Objects need templates and methods for simulating behaviours
Pulses need to be counted and tracked. Probably need an instruction stack read from top.
Can do 1000 presses or check for cycles and calculate full run (probably part 2)
'''
# Variables
with open("puzzle_input.txt") as file:
    input = file.read().splitlines()

# Functions

# modules = [{}, {}, ...]
# module = {name: xxx, state: [], outputs: []} # how to track inputs for conjunction?
# pulses = [("a", 0), ("b", 1), ...]
# lowpulses = 0
# highpulses = 0


class Broadcaster():
    def __init__(self, name="broadcaster", outputs=None, state=0) -> None:
        self.name = name
        self.outputs = outputs if outputs is not None else []
        self.state = state

    def __str__(self) -> str:
        return f"{self.name} -> {self.outputs}"

    def addTarget(self, output) -> None:
        self.outputs.append(output)

    def trigger(self, input: bool, source: str) -> None:
        return zip([self.name]*len(self.outputs), [input]*len(self.outputs), self.outputs)
        # for output in self.outputs:
        #     output.trigger(input)

class FlipFlop():
    def __init__(self, name: str, outputs=None) -> None:
        self.state = 0
        self.name = name
        self.outputs = outputs if outputs is not None else []

    def __str__(self) -> str:
        return f"{self.name} ({self.state}) -> {self.outputs}"

    def trigger(self, input: bool, source: str):
        match input:
            case 1:
                return None
            case 0:
                if self.state == 0:
                    self.state = 1
                    return zip([self.name]*len(self.outputs), [self.state]*len(self.outputs), self.outputs)
                elif self.state == 1:
                    self.state = 0
                    return zip([self.name]*len(self.outputs), [self.state]*len(self.outputs), self.outputs)
            case _:
                return ValueError

class Conjunction():
    def __init__(self, name: str, outputs: list = None, state: dict = None) -> None:
        self.name = name
        self.state = state if state is not None else {}
        self.outputs = outputs if outputs is not None else []

    def __str__(self) -> str:
        return f"{self.name} {self.state} -> {self.outputs}"

    def add_source(self, source: str) -> None:
        self.state[source] = 0

    def status(self) -> dict:
        return self.state

    def trigger(self, input: bool, source: str) -> bool:
        self.state[source] = input
        pulse = 0
        for state in self.state.values():
            if state == 0:
                pulse = 1
                break
        return zip([self.name]*len(self.outputs), [pulse]*len(self.outputs), self.outputs)


def preload(input: list):
    modules = []
    # Find broadcaster
    for line in input:
        if line[0] == "b":
            outputs = "".join(line.split("->")[1].split(" ")).split(",")
            modules.append(Broadcaster("broadcaster", outputs))

    # Load empty conjunctions
    for line in input:
        if line[0] == "&":
            name = line.split("->")[0].strip(" ")[1:]
            outputs = "".join(line.split("->")[1].split(" ")).split(",")
            modules.append(Conjunction(name, outputs))
            # print("Conjunction {} added".format(name))

    # Fill conjunctions with conjunction inputs
    for line in input:
        if line[0] == "&":
            name = line.split("->")[0].strip(" ")[1:]
            outputs = "".join(line.split("->")[1].split(" ")).split(",")
            for module in modules:
                if module.name in outputs:
                    module.add_source(name)
            # print("Conjunction {} added".format(name))

    # Load flipflops updating conjunction inputs
    flipflops_temp = []
    for line in input:
        if line[0] == "%":
            name = line.split("->")[0].strip(" ")[1:]
            outputs = "".join(line.split("->")[1].split(" ")).split(",")
            for module in modules:
                if module.name in outputs:
                    module.add_source(name)
            flipflops_temp.append(FlipFlop(name, outputs))
            # print("Flipflop {} added".format(name))

    for ff in flipflops_temp:
        modules.append(ff)

    # Check all modules created successfully
    if len(modules) == len(input): print("\nAll modules accounted for")
    else: print("\nModule count error\n")

    return modules

def print_history(history: list) -> None:
    print("\n--- Check records: ---")
    for line in history: print(f"{line[0]} -({line[1]})-> {line[2]}")

def print_module_states(modules: list) -> None:
    print("\n--- Module state: ---")
    for module in modules: print(type(module).__name__, module)

def get_state(modules: list) -> list:
    state = []
    for module in modules:
        state.append((module.name, module.state))
    return state

def check_end(history: list) -> int:
    rx_count = 0
    for line in history:
        if line[2] == "rx" and line[1] == 0:
            rx_count += 1
    return rx_count

# Main code
def main():
    # Create modules from puzzle input
    modules = preload(input)
    print_module_states(modules)

    # Set initial state and tracker
    presses = 0
    cycle_end = False
    history = []

    while not cycle_end:
        # Initialise signal queue
        queue = [("button", 0, "broadcaster")]
        presses += 1
        while len(queue) > 0:
            source = queue[0][0]
            pulse = queue[0][1]
            active_module = queue[0][2]
            history.append(queue.pop(0))
            # print(f"{source} -({pulse})-> {active_module}")
            for mod in modules:
                if mod.name == active_module:
                    outputs = mod.trigger(pulse, source)
                    if outputs:
                        for output in outputs: queue.append(output)
        # print_module_states(modules)

        # print_history(history)
        rx_count = check_end(history)
        #os.system('clear')
        if presses%1000==0 or rx_count is not 0:
            print(f"--- Button press {presses}, rx lows: {rx_count}")
        cycle_end = rx_count == 1
        history = []

    print("\nThe solution is:",presses)

main()
