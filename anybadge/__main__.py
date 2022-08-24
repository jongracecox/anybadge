from .cli import main

if __name__ == "__main__":
    # ensure that `anybadge` shows in usage (not __main__.py)
    import sys

    sys.argv[0] = "anybadge"

    main()
