#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'zhang'
__mtime__ = '9/15/2017'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
from win32com.client import Dispatch
import win32com.client
import os


class EasyExcel:
    """A utility to make it easier to get at Excel.  Remembering
    to save the data is your problem, as is  error handling.
    Operates on one workbook at a time."""
    def __init__(self, filename=None):
        self.xlApp = win32com.client.Dispatch('Excel.Application')
        if filename:
            self.filename = filename
            self.xlBook = self.xlApp.Workbooks.Open(filename)
        else:
            self.xlBook = self.xlApp.Workbooks.Add()
            self.filename = ''

    def save(self, new_filename=None):
        if new_filename:
            self.filename = new_filename
            self.xlBook.SaveAs(new_filename)
        else:
            self.xlBook.Save()

    def close(self):
        self.xlBook.Close(SaveChanges=0)
        del self.xlApp

    def get_cell(self, sheet, row, col):
        """Get value of one cell"""
        sht = self.xlBook.Worksheets(sheet)
        return sht.Cells(row, col).Value

    def set_cell(self, sheet, row, col, value):
        # "set value of one cell"
        sht = self.xlBook.Worksheets(sheet)
        sht.Cells(row, col).Value = value

    def get_range(self, sheet, row1, col1, row2, col2):
        """return a 2d array (i.e. tuple of tuples)"""
        sht = self.xlBook.Worksheets(sheet)
        return sht.Range(sht.Cells(row1, col1), sht.Cells(row2, col2)).Value

    def add_picture(self, sheet, pictureName, Left, Top, Width, Height):
        """Insert a picture in sheet"""
        sht = self.xlBook.Worksheets(sheet)
        sht.Shapes.AddPicture(pictureName, 1, 1, Left, Top, Width, Height)

    def cp_sheet(self, before):
        """copy sheet"""
        sheets = self.xlBook.Worksheets
        sheets(1).Copy(None, sheets(1))


def file_name(file_dir):
        file_list = []
        for root, dirs, files in os.walk(file_dir):
            for file in files:
                if os.path.splitext(file)[1] == '.xls' or os.path.splitext(file)[1] == '.xlsx':
                    file_list.append(os.path.join(root, file))
        return file_list


# "下面是一些测试代码。
if __name__ == "__main__":
    list1 = file_name('logs')
    for list2 in list1:
        # PNFILE = r'c:\screenshot.bmp'
        xls = EasyExcel(list1)
        xls.get_cell('Sheet1', 1, 1)
        # xls.addPicture('Sheet1', PNFILE, 20,20,1000,1000)
        # xls.cpSheet('Sheet1')
        # xls.save()
        xls.close()
