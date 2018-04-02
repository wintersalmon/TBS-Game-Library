import json
import os
from unittest import TestCase, main

from settings import FT_SCRIPT_DIR


class BaseFunctionalTestCase(TestCase):
    @staticmethod
    def load_json(package_name, file_name):
        load_file_name = os.path.join(FT_SCRIPT_DIR, package_name, file_name)

        with open(load_file_name, 'r', encoding='utf-8') as infile:
            return json.load(infile)


if __name__ == "__main__":
    main()
