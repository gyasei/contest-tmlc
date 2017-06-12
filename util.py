
def process_token(ent):
    enttype = ent.get('type')
    value = ent.get('value')
    if enttype == 'word' or enttype == 'letter':
        if value[0].isdigit():
            return '!'
        else:
            return value.lower()
    elif enttype == 'userMention':
        return '@'
    elif enttype == 'punctuation':
        return '#'
    elif enttype == 'number':
        return '!'
    elif enttype == 'hashtag':
        return '#'
    elif enttype == 'emoji':
        return '%'
    elif enttype == 'url':
        return '^'
    else:
        print ent

def Recover(text, entities):
    res = []
    for x, y in zip(text, entities):
        if y.get('type') == 'letter': # !!! only letter should be submitted
            value = y.get('value')
            if value.isdigit():
                res.append(value)
            elif value.isupper():
                res.append(x.capitalize())
            else:
                res.append(x)
    return res

def evaluate(outputs, targets, display=False):
    total, correct = 0, 0
    for output, target in zip(outputs, targets):
        t, c = len(target), 0
        if display:
            print 'TARGET: ', target
        for one_output in output:
            c = max(c, len([i for i in xrange(t) if i < len(one_output) and target[i]==one_output[i]]))
            if display:
                print 'PREDICT:', one_output
        if display:
            print c, '/', t, '  ',
        if display:
            print '\n================'
        total += t
        correct += c
    print '\n %d / %d. Final precision: %f' % (correct, total, float(correct)/total)

