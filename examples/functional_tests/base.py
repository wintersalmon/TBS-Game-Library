import json
import os
from unittest import TestCase, main


class BaseFunctionalTestCase(TestCase):
    def setUp(self):
        src_path = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(src_path, 'data')

    @staticmethod
    def load_json(file_dir, file_name):
        load_file_path = os.path.join(file_dir, file_name)
        with open(load_file_path, 'r', encoding='utf-8') as infile:
            return json.load(infile)


if __name__ == "__main__":
    main()
