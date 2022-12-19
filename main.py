from request import start_parse
import argparse


if __name__ == "__main__":
    parsargs = argparse.ArgumentParser(description="Practice parser")

    parsargs.add_argument("-u", "--url", dest="url",
                          help="url сайта", required=True)
    parsargs.add_argument("-p", "--proxy", dest="proxyfile",
                          help="ссылка на файл с прокси")
    parsargs.add_argument("-o", "--out", dest="outputfile",
                          help="файл в который запишется результат парсинга")

    args = parsargs.parse_args()
    # print(args)
    start_parse(args)
