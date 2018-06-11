#coding=utf-8
import pandas as pd
import numpy as np
import xlwings as xw

wb = xw.Book(u'D:\\yun\\百度云\\FinExcels\\StockSel\\StocksSelRoe15_y16_13_16_D.xlsx')
#wb = xw.Book(u'D:\\yun\\百度云\\FinExcels\\reports\\StocksSelA_14_16_5_D.xlsx')
templ = wb.sheets['002749']
sht = wb.sheets['I']
row =2
for s in wb.sheets:
    if s.name != 'I':
        sht.range((row,2)).value = s.name
        formal = '=HYPERLINK(\"#\'{0}\'!B2\",\"{1}\")'.format(s.name, s.range('B2').value )
        sht.range((row,3)).value =  formal
        s.range('A1').value =  '=HYPERLINK(\"#\'{0}\'!C{2}\",\"{1}\")'.format(sht.name, 'Index', '{0}'.format(row) )
        s.range('A1').column_width = 20
        
        templ.range('A2:A146').api.Copy()
        s.range('A2:A146').api.PasteSpecial( -4104 )
        
        templ.range('A1:Z146').api.Copy()
        s.range('A1:Z146').api.PasteSpecial( -4122 )
        #s.range('B1:Z200').columns.autofit()
        s.range('B1:Z200').column_width = 7
        row=row+1

#wb.save()     
#wb.close()  