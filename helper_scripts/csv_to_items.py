import csv

contexts = ['context-low-bias', 'context-positive-bias', 'context-negative-bias']
answers = ['answer-high-certainty', 'answer-low-certainty', 'answer-reductive-answer', 'answer-exhaustive-answer', 'answer-non-answer']


out_file_lines = []

with open('../stimuli/raw-relevance-items-complete.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    item_counter = 1
    for row in reader:
        for c in contexts:
            for a in answers:
                # setup_posterior = row["setup-posterior"]
                # answer_text = row[a]
                out_file_lines.append('# target ' + str(item_counter) + ' ' + c + ' ' + a)
                out_file_lines.append(row[c])
                out_file_lines.append(row["setup-posterior"])
                out_file_lines.append(row[a])
                out_file_lines.append(row["prompt-likelihood"])
                out_file_lines.append('')
        item_counter += 1
print(item_counter)
print(out_file_lines)

with open('../stimuli/posterior-items.txt', 'w') as outfile:
    for line in out_file_lines:
        outfile.write('%s\n' % line)