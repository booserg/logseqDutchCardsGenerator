import os
import pyttsx3
from unidecode import unidecode
import re

logseq_source_page = r"C:\Users\SergeyYevtushik\iCloudDrive\iCloud~com~logseq~logseq\flow\pages\Duolingo. Unit 1 phrases.md"
logseq_storage = r"C:\Users\SergeyYevtushik\iCloudDrive\iCloud~com~logseq~logseq\flow\assets"

assets_folder_name = logseq_source_page.split('\\')[-1]
assets_folder_name = assets_folder_name.split('.')[0]

folder_for_audio = os.path.join(logseq_storage, assets_folder_name)
if not os.path.isdir(folder_for_audio):
    os.mkdir(folder_for_audio)

phrase_separator = "<->"

output = []
with open(logseq_source_page, "r") as f:
    contents = f.readlines()

def precedingTabsCounter(line):
    tabs_count = 0
    for char in line:
        if char == "\t":
            tabs_count = tabs_count + 1
        else:
            return tabs_count

def isChild(possibleParent, possibleChild):
    parentTabsCount = precedingTabsCounter(possibleParent)
    childTabsCount = precedingTabsCounter(possibleChild)
    if childTabsCount > parentTabsCount and childTabsCount - parentTabsCount == 1:
        return True
    else:
        return False
    
def giveTabs(tabsNumber):
    result = ""
    for i in range(tabsNumber):
        result = result + "\t"
    return result

def processLine(line, next_line, output):
    output.append(line)
    if phrase_separator in line and not isChild(line, next_line):

        line_tabs_amount = precedingTabsCounter(line)
        question_prefix = giveTabs(line_tabs_amount + 1)
        answer_prefix = giveTabs(line_tabs_amount + 2)

        dutch_part = line.split(phrase_separator)[0][2:]
        english_part = line.split(phrase_separator)[1]

        if "\n" not in line:
            output.append("\n")

        audio_file_path = os.path.join(folder_for_audio, dutch_part.strip() + ".mp3")
        nl_engine.save_to_file(dutch_part, audio_file_path)
        nl_engine.runAndWait()

        audio_link = "![" + dutch_part + "](assets/" + assets_folder_name + "/" + dutch_part.strip() + ".mp3)"

        output.append(question_prefix + "- " + english_part + " #card \n")
        output.append(answer_prefix + "- " + dutch_part + " " + audio_link + " \n")

        output.append(question_prefix + "- " + audio_link + " #card \n")
        output.append(answer_prefix + "- " + english_part + "\n")

nl_engine = pyttsx3.init()
nl_engine.setProperty("rate", 110)
nl_engine.setProperty("voice", "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_nlNL_Frank")

is_started = False
line = ""
for next_line in contents:
    if is_started == False:
        is_started = True
        line = next_line
        continue
    processLine(line, next_line, output)
    line = next_line    

processLine(line, "empty", output)

with open(logseq_source_page, "w") as f:
    output = "".join(output)
    f.write(output)


