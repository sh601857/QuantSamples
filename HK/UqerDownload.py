from uqer import Client

uqer = Client(token='48B9E996F14993A47556D43B263D1FC7')

files = uqer.list_data()
print(files)
uqer.download_data(filename='HKQuotes/h00998.txt')

