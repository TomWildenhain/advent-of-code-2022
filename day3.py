import os

def read_input(day):
    with open("input%d.txt" % day, "rt") as f:
        return f.read().replace('\r', '')

def get_inp_lines(day):
    return [l.strip() for l in read_input(day).strip().split('\n')]

def chunk(l, size=3):
    chunk = []
    for x in l:
        chunk.append(x)
        if len(chunk) == size:
            yield chunk
            chunk = []

def part1():
    from string import ascii_lowercase, ascii_uppercase
    priors = '*' + ascii_lowercase + ascii_uppercase
    def common_item_prior(l):
        h = len(l) // 2
        c = set(l[:h]).intersection(l[h:])
        assert len(c) == 1
        return priors.find(list(c)[0])

    print(sum(common_item_prior(l) for l in get_inp_lines(3)))

def part2():
    from string import ascii_lowercase, ascii_uppercase
    priors = '*' + ascii_lowercase + ascii_uppercase
    def common_item_prior(l):
        c = set(l[0]).intersection(l[1]).intersection(l[2])
        assert len(c) == 1
        return priors.find(list(c)[0])
    print(sum(common_item_prior(l) for l in chunk(get_inp_lines(3))))

part2()