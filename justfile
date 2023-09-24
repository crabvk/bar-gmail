build:
    poetry build

install:
    pip install -e .

uninstall:
    pip uninstall -y bar-gmail

publish:
    poetry publish
