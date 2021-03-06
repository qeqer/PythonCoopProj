import unittest
from unittest.mock import patch
import os
from Palette import Palette
from Color import Color
from App import App
from Dict import load_dict

""" Just run this file to test then
    1) coverage run tests.py
    2) coverage report -m --omit tests.py
 """


class TestPalette(unittest.TestCase):
    def setUp(self):
        self.test_palette = Palette()

    def test_load1(self):
        # тестируем загрузку палитры из файла и не из файла
        self.test_palette.load(1)
        self.assertEqual(next(self.test_palette.palette), "#000040")
        self.assertEqual(self.test_palette.gradient, 0)
        self.assertEqual(next(self.test_palette.palette), "#00003D")

    def test_load_3(self):
        self.test_palette.load(-3)
        self.assertEqual(
            self.test_palette.colours,
            ([-420.0, 861.42857143, -438.61904762, 241.88095238],
                [-936.0, 2131.71428571, -1183.42857143, 212.35714286],
                [-726.0, 1891.71428571, -1152.69047619, 221.4047619]))
        self.assertEqual(next(self.test_palette), "#EABEC8")
        self.assertEqual(self.test_palette.gradient, 0.01953125)

    def test_load_4(self):
        self.test_palette.load(-4)
        self.assertEqual(
            self.test_palette.colours,
            ([344.19642857, -366.33928571, 250.46428571],
                [42.85714286, -42.71428571, 19.14285714],
                [47.32142857, -47.17857143, 20.07142857]))


class TestColor(unittest.TestCase):
    """Palette is used in color"""
    def setUp(self):
        self.color = Color()

    def test_color(self):
        self.assertEqual(self.color.code, "#969696")
        self.assertEqual(self.color.color_dif, 30)

    def test_color_decode(self):
        self.color.code = "#000000"
        self.color.decode()
        self.assertEqual([self.color.red, self.color.green, self.color.blue], [0, 0, 0])

    def test_color_next(self):
        self.assertEqual(next(self.color), "#969696")
        self.assertEqual(len(next(self.color)), 7)

    def test_color_mut(self):
        self.color.random_color = -2
        next(self.color)
        for i in range(10):
            self.assertLess(self.color.red, 181)
            self.assertLess(self.color.green, 181)
            self.assertLess(self.color.blue, 181)
            self.assertGreater(self.color.red, 119)
            self.assertGreater(self.color.green, 119)
            self.assertGreater(self.color.blue, 119)

    def test_define_palette(self):
        self.color.define_palette(1)
        self.assertEqual(next(self.color.palette), "#000040")
        self.assertEqual(next(self.color.palette), "#00003D")


class TestPaint(unittest.TestCase):

    def setUp(self):
        # тестовый стенд
        load_dict('English')
        self.root = App()
        self.update()

    def tearDown(self):
        self.root.destroy()

    def update(self):
        self.root.update()
        self.root.update_idletasks()

    def test_paint1(self):
        self.root.canv.event_generate('<B1-Motion>', when="tail", x=40, y=40)
        self.update()
        self.assertEqual(self.root.canv.find_all(), (1, 2, 3, 4, 5, 6, 7, 8))

    def test_figure_menu(self):
        self.root.brush_style.invoke(1)
        self.update()
        self.root.canv.event_generate('<B1-Motion>', when="tail", x=40, y=40)
        self.update()
        self.root.brush_style.invoke(2)
        self.update()
        self.root.canv.event_generate('<B1-Motion>', when="tail", x=40, y=40)
        self.update()
        self.root.brush_style.invoke(3)
        self.update()
        self.root.canv.event_generate('<B1-Motion>', when="tail", x=40, y=40)
        self.update()
        self.assertEqual(len(self.root.canv.find_all()), 3 * 8)

    def test_scale_menu(self):
        self.root.scale_choice.invoke(1)
        self.update()
        self.root.canv.event_generate('<B1-Motion>', when="tail", x=40, y=40)
        self.update()
        self.root.scale_choice.invoke(2)
        self.update()
        self.root.canv.event_generate('<B1-Motion>', when="tail", x=40, y=40)
        self.update()
        self.root.scale_choice.invoke(3)
        self.update()
        self.root.canv.event_generate('<B1-Motion>', when="tail", x=40, y=40)
        self.update()
        self.root.scale_choice.invoke(4)
        self.update()
        self.root.canv.event_generate('<B1-Motion>', when="tail", x=40, y=40)
        self.update()
        self.root.scale_choice.invoke(5)
        self.update()
        self.root.canv.event_generate('<B1-Motion>', when="tail", x=40, y=40)
        self.update()
        self.assertEqual(len(self.root.canv.find_all()), 5 * 8)

    def test_undo_redo(self):
        self.root.canv.event_generate('<Button-1>', when="tail", x=40, y=40)
        self.root.canv.event_generate('<B1-Motion>', when="tail", x=40, y=40)
        self.update()
        self.root.canv.event_generate('<Button-1>', when="tail", x=50, y=50)
        self.root.canv.event_generate('<B1-Motion>', when="tail", x=50, y=50)
        self.update()
        self.assertEqual(len(self.root.canv.find_all()), 2 * 8)
        self.root.main_menu.invoke(4)  # undo
        self.update()
        self.assertEqual(len(self.root.canv.find_all()), 1 * 8)
        self.root.main_menu.invoke(5)  # redo
        self.update()
        self.assertEqual(len(self.root.canv.find_all()), 2 * 8)

    def test_save_load(self):
        self.root.canv.event_generate('<Button-1>', when="tail", x=40, y=40)
        self.root.canv.event_generate('<B1-Motion>', when="tail", x=40, y=40)
        self.update()
        self.root.canv.event_generate('<Button-1>', when="tail", x=50, y=50)
        self.root.canv.event_generate('<B1-Motion>', when="tail", x=50, y=50)
        self.update()
        self.assertEqual(len(self.root.canv.find_all()), 2 * 8)
        path = os.path.join(os.getcwd(), 'temporary_test_file.kld')
        with patch('tkinter.filedialog.asksaveasfilename', return_value=path):
            self.root.file_menu.invoke(2)  # save
            self.update()
        self.root.main_menu.invoke(7)  # clean
        self.update()
        self.assertEqual(len(self.root.canv.find_all()), 0)
        with patch('tkinter.filedialog.askopenfilename', return_value=path):
            self.root.file_menu.invoke(1)  # load
            self.update()
        self.assertEqual(len(self.root.canv.find_all()), 2 * 8)
        os.remove(path)


if __name__ == "__main__":
    testSuite = unittest.TestSuite()
    testSuite.addTest(unittest.makeSuite(TestPalette))
    testSuite.addTest(unittest.makeSuite(TestColor))
    testSuite.addTest(unittest.makeSuite(TestPaint))
    runner = unittest.TextTestRunner()
    runner.run(testSuite)
