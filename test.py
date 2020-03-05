import unittest
from multiprocess_chunks import map_list_as_chunks, map_list_in_chunks


class TestCase(unittest.TestCase):


    def test_map_list_as_chunks_1(self):
        l = range(0, 10)
        f = lambda chunk, ed: [c * ed for c in chunk]
        result = map_list_as_chunks(l, f, 5, 2)
        self.assertCountEqual(result[0], [0, 5, 10, 15, 20])
        self.assertCountEqual(result[1], [25, 30, 35, 40, 45])


    def test_map_list_as_chunks_2(self):
        l = range(0, 9)
        f = lambda chunk, ed: [c * ed for c in chunk]
        result = map_list_as_chunks(l, f, 5, 2)
        self.assertCountEqual(result[0], [0, 5, 10, 15, 20])
        self.assertCountEqual(result[1], [25, 30, 35, 40])


    def test_map_list_as_chunks_3(self):
        l = []
        f = lambda chunk, ed: [c * ed for c in chunk]
        result = map_list_as_chunks(l, f, 5, 2)
        self.assertEqual(result, [])


    def test_map_list_as_chunks_4(self):
        l = [1]
        f = lambda chunk, ed: [c * ed for c in chunk]
        result = map_list_as_chunks(l, f, 5, 2)
        self.assertEqual(result, [[5]])


    def test_map_list_in_chunks_1(self):
        l = range(0, 10)
        f = lambda item, ed: item * ed
        result = map_list_in_chunks(l, f, 5)
        self.assertCountEqual(result, [0, 5, 10, 15, 20, 25, 30, 35, 40, 45])


    def test_map_list_in_chunks_2(self):
        l = []
        f = lambda item, ed: item * ed
        result = list(map_list_in_chunks(l, f, 5))
        self.assertEqual(result, [])


    def test_map_list_in_chunks_3(self):
        l = [1]
        f = lambda item, ed: item * ed
        result = list(map_list_in_chunks(l, f, 5))
        self.assertEqual(result, [5])
