def create_tuples(args):
    vals = []
    for field in args:
        a = (field,)
        b = a + (field,)
        vals.append(b)
    return vals