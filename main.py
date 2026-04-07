from factories import ChainFactory, ContextFactory

def main():
    request = ContextFactory.get_request()
    handler = ChainFactory.get_chained_handler()

    handler.handle(request)

    print("hi")

if __name__ == '__main__':
    main()