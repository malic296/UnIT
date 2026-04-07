from factories import ContextFactory, ChainFactory

def main():
    req = ContextFactory.get_request()
    handler = ChainFactory.get_chained_handler()
    handler.handle(req)

if __name__ == "__main__":
    main()