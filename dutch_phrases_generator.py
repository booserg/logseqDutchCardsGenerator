logseq_source_page = r"C:\Users\syevt\iCloudDrive\iCloud~com~logseq~logseq\flow\pages\Test page 1.md"
logseq_storage = r"C:\Users\syevt\iCloudDrive\iCloud~com~logseq~logseq\flow\assets"

with open(logseq_source_page, "r") as f:
    contents = f.readlines()

line_cnt = 0
for line in contents:
    if "<->" in line:
        card_prefix = ''
        tabs_count = line.count("\t")
        for i in range(tabs_count + 1):
            card_prefix = card_prefix + '\t'
        contents.insert(line_cnt + 1, card_prefix + "- card\n")
    line_cnt = line_cnt + 1    

with open(logseq_source_page, "w") as f:
    contents = "".join(contents)
    f.write(contents)


