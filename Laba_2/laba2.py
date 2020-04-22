import csv
import matplotlib.pyplot as plt
import dateutil.parser

CLIENT = "192.168.250.39"
LIMIT = 1000
PRICE = 0.5


def csv_reader(file_obj):
    reader = csv.reader(file_obj)
    rows = []
    for row in reader:
        if len(row) < 48:
            continue
        if row[3] == CLIENT or row[4] == CLIENT:
            rows.append(row)
    return rows


def get_traffic(data):
    traff = 0
    for row in data:
        traff += int(row[12])
    return traff


def draw_graphic(data):
    time = [dateutil.parser.parse(tmp[0]) for tmp in data]
    capacity = [tmp[1] for tmp in data]

    plt.plot(time, capacity)
    plt.savefig("myplot.png", dpi=800)
    plt.show()


def write_csv(data):
    f = open("myscv.csv", "w")
    q = csv.writer(f)
    for line in data:
        q.writerow(line)


def summ_traff(data):
    new_traff = {}
    for line in data:
        if line[0] in new_traff:
            new_traff[line[0]] += int(line[12])
            continue
        new_traff.update({line[0]: int(line[12])})
    return new_traff


def cost_traff(traff):
    # traff in bytes
    traff = traff / 1024
    # traff in Kb
    cost = (traff - LIMIT) * PRICE
    return cost


file = open("2.csv", "r")
data = csv_reader(file)
traff = get_traffic(data)
cost = cost_traff(traff)
print('Cost of services for using the Internet: ', round(cost, 3))

new_data = summ_traff(data)
list = [(k, v) for k, v in new_data.items()]
list.sort()

draw_graphic(list)
# write_csv(list)
