ok = ["j","h"]
l = ["u","j","h","k"]

for li in l:
    try:
        print ok.index(li)
    except (ValueError):
        print "eroor on : ", li
        continue
    print "good"
