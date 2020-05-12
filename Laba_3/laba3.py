import laba1
import laba2

from fpdf import FPDF
from datetime import datetime

PDF_FILE = 'payment.pdf'


def pdf_common_line(pdf, font_size, text):
    pdf.write(font_size / 2, text)
    pdf.ln(font_size / 2)


def create_pdf(call_info, internet_info, bank_name, inn, kpp, bik, recipient, account_number1, account_number2,
               doc_number, date, provider,
               customer, reason):
    header = [['Банк получателя: ' + bank_name, 'БИК: ' + bik],
              ["ИНН: " + inn + "   " + "КПП: " + kpp, 'Сч. №' + account_number1],
              ['Получатель: ' + recipient, 'Сч. №' + account_number2]]
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', './DejaVuSansCondensed.ttf', uni=True)
    pdf.add_font('DejaVu', 'B', './DejaVuSansCondensed-Bold.ttf', uni=True)
    pdf.set_font('DejaVu', '', 12)

    # header
    col_width = pdf.w / 2.2
    row_height = pdf.font_size
    spacing = 2
    for row in header:
        for item in row:
            pdf.cell(col_width, row_height * spacing,
                     txt=item, border=1)
        pdf.ln(row_height * spacing)

    font_size = 16
    pdf.set_font('DejaVu', 'B', font_size)
    pdf.ln(font_size / 2)
    pdf_common_line(pdf, font_size, "Счёт на оплату №{} от {}г.".format(doc_number, date))
    pdf_common_line(pdf, font_size, "_" * 74)

    font_size = 12
    pdf.ln(font_size)
    pdf.set_font('DejaVu', '', font_size)
    pdf_common_line(pdf, font_size, "Поставщик")
    pdf_common_line(pdf, font_size, "(Исполнитель): {}".format(provider))
    pdf_common_line(pdf, font_size, "")
    pdf_common_line(pdf, font_size, "Покупатель")
    pdf_common_line(pdf, font_size, "(Заказчик): {}".format(customer))
    pdf_common_line(pdf, font_size, "")
    pdf_common_line(pdf, font_size, "Основание: {}".format(reason))
    pdf_common_line(pdf, font_size, "")

    # table
    font_size = 10
    row_height = pdf.font_size
    pdf.set_font('DejaVu', '', font_size)

    table = [['№', "Товары (работы, услуги)", "Кол-во", "Ед.", "Сумма"]]
    counter = 1

    # in calls
    for call in call_info:
        table.append([str(counter), "Исходящий звонок к {}".format(call[5]), "{} мин.".format(call[2]),
                      "{} руб.".format(PRICE_CALL), "{} руб.".format(call[1])])
        counter += 1

        table.append([str(counter), "Бесплатные минуты исходящих звонков", "{} мин.".format(call[0]), '',
                      "{} руб.".format(call[0] * PRICE_CALL * -1)])
        counter += 1

    # sms
    for sms in call_info:
        table.append([str(counter), "SMS для {}".format(sms[5]), "{} шт.".format(sms[4]),
                      "{} руб.".format(PRICE_SMS), "{} руб.".format(sms[3])])
        counter += 1

    # internet
    table.append([str(counter), "Интернет трафик (за КБ)", "{} КБ".format(internet_info[0]), "{} руб.".format(KB_PRICE),
                  "{} руб.".format(internet_info[1])])

    table.append(['', "ВСЕГО", '', '', "{} руб.".format(cost_tel)])

    one_part = pdf.w / 18
    for row in table:
        pdf.cell(one_part * 1, row_height * spacing, txt=row[0], border=1)  # number
        pdf.cell(one_part * 8, row_height * spacing, txt=row[1], border=1)  # title
        pdf.cell(one_part * 2, row_height * spacing, txt=row[2], border=1)  # count
        pdf.cell(one_part * 2, row_height * spacing, txt=row[3], border=1)  # cost per one
        pdf.cell(one_part * 3, row_height * spacing, txt=row[4], border=1)  # total cost
        pdf.ln(row_height * spacing)

    # footer
    font_size = 16
    pdf.set_font('DejaVu', 'B', font_size)
    pdf_common_line(pdf, font_size, "Всего к оплате: {} руб.".format(cost_tel))
    pdf_common_line(pdf, font_size, "")

    font_size = 8
    pdf.set_font('DejaVu', '', font_size)
    pdf_common_line(pdf, font_size, "Внимание!")
    pdf_common_line(pdf, font_size,
                    "Оплата данного счёта означает согласие с условиями поставки товара/предоставления услуг.")
    pdf_common_line(pdf, font_size, "")

    font_size = 16
    pdf.set_font('DejaVu', 'B', font_size)
    pdf.ln(font_size / 2)
    pdf_common_line(pdf, font_size, "_" * 74)
    font_size = 12
    pdf.set_font('DejaVu', '', font_size)
    pdf.ln(font_size / 2)
    pdf_common_line(pdf, font_size, "Руководитель " + "_" * 20 + " " * 25 + "Бухгалтер " + "_" * 20)

    pdf.output(name=PDF_FILE, dest='F').encode('utf-8')


# variant 14 mod 15 = 14
if __name__ == "__main__":
    # 1 lab
    MY_PHONE = "915783624"
    PRICE_SMS = 5
    PRICE_CALL = 1
    FREE_CALL = 10
    IP = "192.168.250.39"
    INTERNET_LIMIT = 1000
    KB_PRICE = 0.5

    call_info = laba1.get_lab_info(MY_PHONE, PRICE_SMS, PRICE_CALL, FREE_CALL)
    cost_tel = 0
    for i in call_info:
        cost_tel += i[1] + i[3] - i[0]

    # 2 lab
    internet_info = laba2.get_lab_info(IP, INTERNET_LIMIT, KB_PRICE)
    cost_tel += internet_info[1]

    # pdf
    print("Creating PDF file...")
    create_pdf(call_info=call_info, internet_info=internet_info, bank_name="Банк ООО", inn='123456789', kpp='0000000',
               bik='23456',
               recipient="Илья Сахно", account_number1="00001", account_number2="00002",
               doc_number="1", date=datetime.now().strftime("%d.%m.%Y"),
               provider="Провайдер", customer="Илья ({}, {})".format(IP, MY_PHONE), reason="День оплаты")
