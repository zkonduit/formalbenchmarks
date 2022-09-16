import collections
import sys
import ast

def main(*args):
    # for each of the args, combine into a single dictionary
    print (args)
    circuitsToOutput = collections.defaultdict(list)
    for arg in args[1:]:
        print (arg)
        currDict = ast.literal_eval(arg)
        print (currDict)
        # iterate through currDict and append to circuitsToOutput

        for key in currDict:
            circuitsToOutput[key].append(currDict[key])
    
    # Create the markdown output
    markdownOutput = """\n| Circuit | Tool | Sound Constraints? |
| -------- | ---- | ---- | """
    for circuit in circuitsToOutput:
        markdownOut+=('\n| ' + circuit + ' | ')

        for toolResults in circuitsToOutput[circuit]:
            markdownOut+=(toolResults["tool"] + ' | ' + toolResults["result"] + ' |')

    print (markdownOutput)

if __name__ == "__main__":
    main(*sys.argv)