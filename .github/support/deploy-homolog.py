import sys
import re

errors = []

def parseBranches(payload):
    matches = re.search("##\s+branches\s*([^#]*)", payload, re.IGNORECASE + re.MULTILINE)

    # Strip matches by end line character and get an array of branches
    branches = [branch.strip() for branch in matches.group(1).splitlines()]

    # Remove empty branches
    branches = list(filter(None, branches))

    # strip whitespaces from each branch
    return [branch.strip() for branch in branches]

def getBranches(currentList, mergeList):
    currentList = currentList.split()

    # Strip matches by end line character and get an array of branches
    matches = re.search("##\s+branches\s*([^#]*)", mergeList, re.IGNORECASE + re.MULTILINE)
    branches = [branch.strip() for branch in matches.group(1).splitlines()]
    branches = list(filter(None, branches))

    # percorra branches e verifique as que contém _DELETE_ no nome. Adicione em deleteBranches e remova-as de branches
    deleteBranches = []
    for branch in branches:
        if '_DELETE_' in branch:
            deleteBranches.append(branch.replace('_DELETE_', '').strip())
        else:
            currentList.append(branch.strip())

    # remove from currentList the branches that are in deleteBranches
    for branch in deleteBranches:
        if branch in currentList:
            currentList.remove(branch)

    return currentList;

try:
    command = sys.argv[1]
    currentList = sys.argv[2]
    mergeList = sys.argv[3]

    if command == 'parse-branches':
        print('\n'.join(parseBranches(mergeList)))
        exit()

    if command == 'get-branches':
        print(getBranches(currentList, mergeList))
        exit()

    print('["invalid-command"]')

except IndexError as error:
    print('["error"]')
