import openpyxl
file = "input.xlsx"
new_row = ["data1", "data2", "data3", "data4"]

wb = openpyxl.load_workbook(filename=file)
ws = wb.get_sheet_by_name("Sheet1")
row = ws.get_highest_row() + 1

for col, entry in enumerate(new_row, start=1):
    ws.cell(row=row, column=col, value=entry)

wb.save(file)

'''
sorts = (
                ('s1', (900,660), application.sort, 0),
                ('s2', (980,660), application.sort, 1),
                ('s3', (1060,660), application.sort, 2),
                ('s4', (1140,660), application.sort, 3),
                ('s5', (1220,660), application.sort, 4),
                ('s6', (900,740), application.sort, 5),
                ('s7', (980,740), application.sort, 6),
                ('s8', (1060,740), application.sort, 7),
                ('s9', (1140,740), application.sort, 8),
                ('s10', (1220,740), application.sort, 9),
                '''