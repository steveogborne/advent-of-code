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
    def __init__(self, name="broadcaster", outputs=None) -> None:
        self.name = name
        self.outputs = outputs if outputs is not None else []

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
    def __init__(self, name: str, outputs: list = None, memory: dict = None) -> None:
        self.name = name
        self.memory = memory if memory is not None else {}
        self.outputs = outputs if outputs is not None else []

    def __str__(self) -> str:
        return f"{self.name} {self.memory} -> {self.outputs}"

    def add_source(self, source: str) -> None:
        self.memory[source] = 0

    def status(self) -> dict:
        return self.memory

    def trigger(self, input: bool, source: str) -> bool:
        self.memory[source] = input
        pulse = 0
        for state in self.memory.values():
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

    # Load flipflops updating conjunction inputs
    for line in input:
        if line[0] == "%":
            name = line.split("->")[0].strip(" ")[1:]
            outputs = "".join(line.split("->")[1].split(" ")).split(",")
            for module in modules:
                if module.name in outputs:
                    module.add_source(name)
            modules.append(FlipFlop(name, outputs))
            # print("Flipflop {} added".format(name))

    # Check all modules created successfully
    if len(modules) == len(input): print("\nAll modules accounted for\n")
    else: print("\nModule count error\n")

    return modules



# Main code
def main():
    modules = preload(input)
    for module in modules: print(type(module).__name__, module)

    queue = [("button", 0, "broadcaster")]
    history = []
    lows = 1
    highs = 0

    print("\nPress button once, singals propagate...\n")

    while len(queue) > 0:
        source = queue[0][0]
        pulse = queue[0][1]
        active_module = queue[0][2]
        history.append(queue.pop(0))
        print(f"{source} -({pulse})-> {active_module}")
        for mod in modules:
            if mod.name == active_module:
                outputs = mod.trigger(pulse, source)
                if outputs:
                    for output in outputs: queue.append(output)



    answer = "Undefined"
    print("\nThe solution is:",answer)

main()
