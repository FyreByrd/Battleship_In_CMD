import statistics as stats

def minmax(data):
    min = data[0]
    max = data[0]
    for i in range(len(data)):
        if data[i] < min:
            min = data[i]
        elif data[i] > max:
            max = data[i]
    return (min,max)
def analyze(data, name):
    output = " "+str(name)+":\n"
    output += "      Mean: "+str(stats.fmean(data))+"\n"
    output += "    Median: "+str(stats.median(data))+"\n"
    output += "   Mode(s): "+str(stats.multimode(data))+"\n"
    output += " Deviation: "+str(stats.pstdev(data))+"\n"
    output += "     Range: "+str(minmax(data))+"\n"
    return output
