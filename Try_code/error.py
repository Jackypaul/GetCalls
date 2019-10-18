def ret_neg():
    raise ValueError

i = 0
try:
    i = ret_neg()
except (ValueError):
    print "ok"

print ValueError
