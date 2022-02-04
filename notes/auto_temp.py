import sys
import datetime

DEF_YTLINK = "https://www.youtube.com/playlist?list=PLLssT5z_DsK8HbD2sPcUIDfQ7zmBarMYv"

if(len(sys.argv) <= 2):
    print("Invalid input")
else:
    v_lec = int(sys.argv[1])
    v_tit = sys.argv[2]
    v_date = datetime.datetime.now().strftime("%d %B, %Y (%a)")
    if(len(sys.argv) == 3):
        v_link = DEF_YTLINK
    else:
        v_link = sys.argv[3]
    data = "NLP || Dan Jurafsky || Stanford University\n\nLecture: {lec}\nTitle: {tit}\nLink: {link}\nDate: {date}\n\n\n".format(lec = v_lec, tit = v_tit, link = v_link, date = v_date)
    filename = str(v_lec) + "_" + v_tit.replace(" ", "_") + ".txt"
    with open(filename, 'w') as f:
        f.write(data)
    print("Lecture file created (" + filename + ")")
