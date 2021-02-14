for i in range(5):
    for j in range(12):
        print("{}-{}-{} * \"life\"".format(2010 + i, j+1, 1))
        print("  Assets:Cash -{} USD".format(1000 + j * 10))
        print("  Expenses:Life:General")

        print("{}-{}-{} * \"transportation\"".format(2010 + i, j+1, 1))
        print("  Assets:Cash -{} USD".format(100 + j * 21))
        print("  Expenses:Life:Transportation:Bus")

        print("{}-{}-{} * \"transportation\"".format(2010 + i, j+1, 1))
        print("  Assets:Cash -{} USD".format(500 + j * 21))
        print("  Expenses:Life:Transportation:Airplane")

print("2013-06-01 * \"travel\"")
print("  Assets:Cash -{} USD".format(10000))
print("  Expenses:Life:Travel")
