from request import start_parse
import argparse


# def main():
#     print(start_parse())


if __name__ == "__main__":
    parsargs = argparse.ArgumentParser(description="Practice parser")

    parsargs.add_argument("-u", "--url", dest="url", help="url сайта", type=str, required=True)
    parsargs.add_argument("-p", "--proxy", dest="proxyfile", help="ссылка на файл с прокси")

    args = parsargs.parse_args()
    print(args)
    # main()
    print(start_parse(args))
