import csv

MY_PHONE = "915783624"
PRICE_SMS = 5
PRICE_CALL = 1
FREE_CALL = 10


def csv_reader(file_obj):
    reader = csv.reader(file_obj)
    rows = []
    for row in reader:
        if len(row) < 5:
            continue
        if row[1] == MY_PHONE:
            rows.append(row)
    return rows


def tariff_call(k, t, t_free):
    t = float(t)
    if t > t_free:
        return (t - t_free) * k
    return 0


def tariff_sms(k, n):
    return int(n) * k


if __name__ == "__main__":
    csv_path = "data.csv"
    main_call = 0
    main_sms = 0
    with open(csv_path, "r") as f_obj:
        info = csv_reader(f_obj)
    for per in info:
        call = tariff_call(PRICE_CALL, per[3], FREE_CALL)
        main_call += call
        sms = tariff_sms(PRICE_SMS, per[4])
        main_sms += sms

        print("Phone: ", per[2])
        print("Price call:", call)
        print("Price sms:", sms)
    print(end="\n")
    print("Main call:", main_call)
    print("Main sms:", main_sms)
