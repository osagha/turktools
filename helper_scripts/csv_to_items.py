import csv

contexts = ['context-low-bias', 'context-positive-bias', 'context-negative-bias']
answers = ['answer-high-certainty', 'answer-low-certainty', 'answer-reductive-answer', 'answer-exhaustive-answer', 'answer-non-answer']

# create prior items text file
out_file_lines = []
with open('stimuli/relevance_stimuli_all.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    item_counter = 1
    for row in reader:
        for c in contexts:
            out_file_lines.append('# target ' + str(item_counter) + ' ' + c)
            out_file_lines.append(row[c])
            out_file_lines.append(row["prompt-likelihood"])
            out_file_lines.append('')
        item_counter += 1

with open('stimuli/prior-items.txt', 'w') as outfile:
    with open('stimuli/prior-fillers.txt', 'r') as fillers:
        for line in fillers:
            outfile.write(line)
    outfile.write("\n")
    for line in out_file_lines:
        outfile.write('%s\n' % line)



# create posterior items text file
out_file_lines = []
with open('stimuli/relevance_stimuli_all.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    item_counter = 1
    for row in reader:
        for c in contexts:
            for a in answers:
                out_file_lines.append('# target ' + str(item_counter) + ' ' + c + ' ' + a)
                out_file_lines.append(row[c])
                out_file_lines.append(row["setup-posterior"])
                out_file_lines.append(row[a])
                out_file_lines.append(row["prompt-likelihood"])
                out_file_lines.append('')
        item_counter += 1

with open('stimuli/posterior-items.txt', 'w') as outfile:
    with open('stimuli/posterior-fillers.txt', 'r') as fillers:
        for line in fillers:
            outfile.write(line)
    outfile.write("\n")
    for line in out_file_lines:
        outfile.write('%s\n' % line)


# create helpfulness items text file
out_file_lines = []
with open('stimuli/relevance_stimuli_all.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    item_counter = 1
    for row in reader:
        for c in contexts:
            for a in answers:
                out_file_lines.append('# target ' + str(item_counter) + ' ' + c + ' ' + a)
                out_file_lines.append(row[c])
                out_file_lines.append(row["setup-relevance-your-turn"])
                out_file_lines.append(row["Question"])
                out_file_lines.append(row["name"] + " responds:")
                out_file_lines.append(row[a])
                out_file_lines.append(row["prompt-helpfulness"].format(name=row["name"]))
                out_file_lines.append('')
        item_counter += 1

with open('stimuli/helpfulness-items.txt', 'w') as outfile:
    with open('stimuli/helpfulness-fillers.txt', 'r') as fillers:
        for line in fillers:
            outfile.write(line)
    outfile.write("\n")
    for line in out_file_lines:
        outfile.write('%s\n' % line)



# create relevance items text file
out_file_lines = []
with open('stimuli/relevance_stimuli_all.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    item_counter = 1
    for row in reader:
        for c in contexts:
            for a in answers:
                out_file_lines.append('# target ' + str(item_counter) + ' ' + c + ' ' + a)
                out_file_lines.append(row[c])
                out_file_lines.append(row["setup-relevance-your-turn"])
                out_file_lines.append(row["Question"])
                out_file_lines.append(row["name"] + " responds:")
                out_file_lines.append(row[a])
                out_file_lines.append(row["prompt-relevance"].format(name=row["name"]))
                out_file_lines.append('')
        item_counter += 1

with open('stimuli/relevance-items.txt', 'w') as outfile:
    with open('stimuli/relevance-fillers.txt', 'r') as fillers:
        for line in fillers:
            outfile.write(line)
    outfile.write("\n")
    for line in out_file_lines:
        outfile.write('%s\n' % line)
