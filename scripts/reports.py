#!/usr/bin/env python3

import yaml
from dotmap import DotMap


# ------------------------------------------------------------------------------


def main(project):
    sdb_file = f'{project.build_dir}/{project.name}.sdb'

    symbols = [line for line in open(sdb_file) if line.startswith('[v')]
    symbols.sort(reverse=True, key=lambda s: int(s.split()[6]))

    rom = []
    ram = []

    for sym in symbols:
        parts = sym.split()[1:-1]

        if parts[2].startswith('`C'):
            rom.append(', '.join(parts))
        else:
            ram.append(', '.join(parts))

    open(f'{project.build_dir}/rom.csv', 'w').write('\n'.join(rom))
    open(f'{project.build_dir}/ram.csv', 'w').write('\n'.join(ram))

    enums = []
    enum = []
    active = False

    for line in open(sdb_file):
        if line.startswith('[e'):
            active = True
            enum = []

        if active:
            enum.append(line)

            if line.startswith(']'):
                active = False
                enums.append(''.join(enum))

    open(f'{project.build_dir}/enums.csv', 'w').write('\n'.join(enums))

    structs = []
    struct = []
    active = False

    for line in open(sdb_file):
        if line.startswith('[s') or line.startswith('[u'):
            active = True
            struct = []

        if active:
            struct.append(line)

            if line.startswith(']') or ']' in line:
                active = False
                structs.append(''.join(struct))

    open(f'{project.build_dir}/structs.csv', 'w').write('\n'.join(structs))

    counts = {}
    for line in open(sdb_file):
        if line.startswith('['):
            item = line[1:2]
            if item not in counts:
                counts[item] = 1
            else:
                counts[item] = counts[item] + 1

    print(counts)


if __name__ == "__main__":
    project = DotMap(yaml.full_load(open("project.yaml").read()))

    main(project)