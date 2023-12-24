# Problem scope
'''
Parts need sorting
Parts have 4 ratings: x,m,a,s. A list of parts to sort is the second half of puzzle input
Parts get sorted through workflows. A list of workflows is the first half of puzzle input
Workflows have rules corresponding to the part ratings and either:
> send the part to another workflow, accept or reject the part.
All parts that are accepted are given a rating which is the sum of their individual ratings
The answer is the sum of all the total ratings of all accpeted parts
'''

# Solution sketch
'''
Turn parts list into list of dictionaries
Turn works flows into list of functions, store as a python file and import

Aim of work flow parser:
turn px{a<2006:qkq,m>2090:A,rfg} into:

def px(part):
    if part[a]<2006: return qkq(part)
    elif part[m]>2090: return "A"
    else: return rfg(part)

Observations:
# lines are separated by ,
# : followed by function call or "A" or "R"
# final term is function call or "A" or "R"
# function call is always 2 or more characters so can do conditionals based onstring length

Elements of parsing:
A add "def " at the start
B "{" -> "(part): if "
C "*}" -> "; else: return " + "A" | "R" | "xyz(part)" depending on *
D "*<" -> "part[*]<"
E "*>" -> "part[*]>"
F all other "," -> "; elif "
G following :* += "return "A"" | "return "B"" | "return *(part)" depending on *

Steps in parsing:
1) first remove trailing }, then split by "," then for each sub-split by ":" (last item not split)
    px{a<2006:qkq,m>2090:A,rfg} goes to:
    [["px{a<2006", "qkq"], --open clause
    ["m>2090", "A"] -- middle clause(s)
    ["rfg"] -- close clause -> want "; else: return *" where * is "A", "B", or rfg(part)
2) for first item in 1): A, B, G
3) for last item in 1): C
4) If there are middle items: prepend with F, and D, E, G
5) Join items with ""
'''
# Variables
with open("puzzle_input.txt") as file:
    input = file.read().split("\n\n")
    workflow_list = input[0].splitlines()
    part_list = input[1].splitlines()

    # for line in workflow_list: print(line)
    # for line in part_list: print(line)

# Functions
def end_resolution(snippet):
    if len(snippet) ==1: return "\n    else: return '"+snippet+"'"
    else: return "\n    else: return "+snippet+"(part)"

def resolution(snippet):
    if len(snippet) ==1: return ": return '"+snippet+"'"
    else: return ": return "+snippet+"(part)"

def comparison(snippet):
    return "part['"+snippet[0]+"']"+snippet[1:]

def line_to_workflow(line):
    if line[0:2] == "in": line = "part_in"+line[2:]
    line_clauses = [clause.split(":") for clause in line[0:-1].split(",")] # step 1
    open_clause = "def "+line_clauses[0][0].split("{")[0]+"(part): \n    if "+comparison(line_clauses[0][0].split("{")[1])+resolution(line_clauses[0][1])
    if len(line_clauses) >2:
        middle_clauses = line_clauses[1:-1]
        middle_clauses = ["\n    elif "+comparison(clause[0])+resolution(clause[1]) for clause in middle_clauses]
        middle_clauses = "".join(middle_clauses)
    else: middle_clauses = ""
    close_clause = end_resolution(line_clauses[-1][0])
    result = open_clause+middle_clauses+close_clause
    return result

with open("workflows.py","w") as file2:
        for line in workflow_list: file2.write(line_to_workflow(line)+"\n")
import workflows

# Main code
def main():
    part = {"x":302,"m":140,"a":650,"s":1288}
    print(workflows.part_in(part))
    # print(line_in(part))
    # answer = "Undefined"
    # print("The solution is:",answer)

main()
