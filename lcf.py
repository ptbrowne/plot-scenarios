import re
import pandas as pd

def is_comment(line):
    return line[0] == '#'

multiple_space = re.compile('\s+')

def parse_line(l):
    return [float(x) for x in multiple_space.split(l.strip()) if x != '']

def parse_metadatum(l):
    # first character is #, second is space
    return multiple_space.split(l[2:], maxsplit=1)

def parse_lcf(filepath):
    with open(filepath) as f:
        lines = list(f.readlines())
        metadata = dict(parse_metadatum(l) for l in lines if is_comment(l))
        data = [parse_line(l) for l in lines if not is_comment(l)]
    column_metadata = [kv for kv in metadata.items() if kv[0].startswith('Column.')]
    column_labels = [kv[1].strip() for kv in sorted(column_metadata, key=lambda kv: kv[0])]
    data = pd.DataFrame.from_records(data, index=column_labels[0], columns=column_labels)
    return data

def main():
    data = parse_lcf('Nouzilly_subs/Zn_Nouzilly_subs_LCF_2refs_sc0.lcf')
    print data

if __name__ == '__main__':
    main()

