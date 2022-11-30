import collections
import sys
import ast

def main(*args):
    # for each of the args, combine into a single dictionary
    #print (args)
    circuitsToOutput = collections.defaultdict(list)
    toolList = []
    resultToMarkdownMap = {"Weakly Verified" : ":white_check_mark:", "Unsound" : ":x:", "Unverified" : ":question:", "Timeout" : ":alarm_clock:", "OtherError" : ":electric_plug:"}

    for arg in args[1:]:
        #print (arg)
        circuitToSpecificToolOutputDict = ast.literal_eval(arg)
        #print (currDict)
        # iterate through currDict and append to circuitsToOutput
        currentTool = next(iter(circuitToSpecificToolOutputDict.values()))["tool"]
        toolList.append(currentTool)
        for circuitInToolSpecificDict in circuitToSpecificToolOutputDict:
            circuitsToOutput[circuitInToolSpecificDict].append(circuitToSpecificToolOutputDict[circuitInToolSpecificDict])
    #print (circuitsToOutput)
    # Create the markdown output

    # This feels very fragile. I'm sure there's a better way to do this.
    markdownOutput = """\n| Circuit | """
    for tool in toolList:
        markdownOutput += tool + " | "
    markdownOutput += "\n| -------- | "
    for tool in toolList:
        markdownOutput += "---- | "
    for circuit in circuitsToOutput:
        markdownOutput+=('\n| ' + circuit + ' | ')

        for toolResults in circuitsToOutput[circuit]:
            toolResult = toolResults["result"]
            markdownOutput+=( resultToMarkdownMap[toolResult] + ' | ')

    print (markdownOutput)

if __name__ == "__main__":
    main(*sys.argv)