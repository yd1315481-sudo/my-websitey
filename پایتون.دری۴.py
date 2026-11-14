# -*- coding: utf-8 -*-
"""پایتونی دری: ویرایشگر و هستهٔ اجرای دستورهای دری."""
import os, sys, re, io, tokenize, tempfile, traceback
from pathlib import Path
from PySide6.QtCore import Qt, QProcess, QProcessEnvironment, QThread, Signal, QTimer
from PySide6.QtGui import QFont, QColor, QTextCharFormat, QSyntaxHighlighter, QTextCursor, QTextBlockFormat
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPlainTextEdit, QPushButton, QLabel, QFileDialog, QMessageBox,
    QDialog, QLineEdit, QInputDialog, QScrollArea, QFrame, QSizePolicy
)

واژه_ها = {
    # دستورهای کنترلی و ساختاری؛ هر دو شکل دری و پایتون پذیرفته می‌شوند.
    'اگر':'if', 'وگرنه_اگر':'elif', 'وگرنه':'else', 'اگرنه':'else',
    'برای':'for', 'در':'in', 'تا':'while', 'تا_وقتی':'while', 'هنگامی_که':'while',
    'تابع':'def', 'تعریف':'def', 'برگردان':'return', 'بازگردان':'return', 'کلاس':'class',
    'تلاش':'try', 'بکوش':'try', 'به_جز':'except', 'جز':'except', 'سرانجام':'finally', 'در_هر_صورت':'finally', 'ایجاد_خطا':'raise', 'خطا_بده':'raise',
    'با':'with', 'به_نام':'as', 'واردکن':'import', 'وارد_کن':'import', 'از':'from',
    'توقف':'break', 'بشکن':'break', 'ادامه':'continue', 'بگذر':'pass', 'هیچ_کار':'pass',
    'و':'and', 'یا':'or', 'نه':'not', 'حذف':'del', 'سراسری':'global',
    'غیرمحلی':'nonlocal', 'بررسی_کن':'assert', 'تابع_کوتاه':'lambda',
    'بازده':'yield', 'ناهمگام':'async', 'منتظر':'await',
    'همزمان':'with', 'همچون':'as', 'است':'is', 'همان':'is',
    'مطابقت':'match', 'حالت':'case'
}

پیشوند = r"""# -*- coding: utf-8 -*-
import math as _math, random as _random, statistics as _statistics
import decimal as _decimal, fractions as _fractions, json as _json
import time as _time, datetime as _datetime, os as _os, re as _re
import pathlib as _pathlib, collections as _collections, itertools as _itertools
import functools as _functools, operator as _operator, string as _string
import array as _array, sqlite3 as _sqlite3, zipfile as _zipfile
import logging as _logging, unittest as _unittest, urllib as _urllib
import urllib.request as _urlrequest, urllib.parse as _urlparse
import http as _http, socket as _socket, hashlib as _hashlib
import secrets as _secrets, csv as _csv, csv as _csv_module
import pickle as _pickle, shelve as _shelve, queue as _queue
import threading as _threading, concurrent.futures as _futures
import subprocess as _subprocess, shlex as _shlex, argparse as _argparse
import platform as _platform, sys as _sys, inspect as _inspect
import copy as _copy, pprint as _pprint, textwrap as _textwrap
import html as _html, xml as _xml, email as _email
import base64 as _base64, zlib as _zlib, gzip as _gzip
import hashlib as _hashlib_module, hmac as _hmac, uuid as _uuid
import typing as _typing, dataclasses as _dataclasses, enum as _enum
import contextlib as _contextlib, warnings as _warnings, traceback as _traceback
import difflib as _difflib, fnmatch as _fnmatch, glob as _glob
import tempfile as _tempfile, shutil as _shutil, io as _io

چاپ = print
نمایش = print
ورودی = input
ورودی_بگیر = input
درست = True
نادرست = False
هیچ = None
ریاضی = _math
تصادفی = _random
آمار = _statistics
اعشاری = _decimal
کسر = _fractions
جیسون = _json
زمان = _time
تاریخ = _datetime
سیستم_عامل = _os
عبارت_منظم = _re
مسیرها = _pathlib
مجموعه_داده = _collections
تکرارگرها = _itertools
ابزار_تابع = _functools
عملگرها = _operator
رشته_ها = _string
آرایه = _array
پایگاه_داده = _sqlite3
فایل_فشرده = _zipfile
ثبت_رویداد = _logging
آزمون = _unittest
شبکه = _urllib
درخواست_شبکه = _urlrequest
نشانی_وب = _urlparse
پروتکل_شبکه = _http
سوکت = _socket
رمزنگاری = _hashlib
رمزهای_امن = _secrets
جدول_داده = _csv
ذخیره_داده = _pickle
قفسه_داده = _shelve
صف = _queue
نخ = _threading
کارهای_همزمان = _futures
اجرای_فرمان = _subprocess
سیستم = _sys
سکوی_اجرا = _platform
بازرسی_کد = _inspect
کپی = _copy
چاپ_زیبا = _pprint
قالب_متن = _textwrap
اچ_تی_ام_ال = _html
اکس_ام_ال = _xml
پست_الکترونیک = _email
رمزگذاری_بنیادی = _base64
فشرده_سازی = _zlib
فشرده_سازی_فایل = _gzip
شناسه_جهانی = _uuid
نوع_داده = _typing
ساختار_داده = _dataclasses
شمارش_ثابت = _enum
مدیریت_زمینه = _contextlib
هشدارها = _warnings
گزارش_خطا = _traceback
مقایسه_متن = _difflib
الگوی_نام_فایل = _fnmatch
جستجوی_فایل = _glob
فایل_موقت = _tempfile
مدیریت_فایل = _shutil
ورودی_خروجی = _io
پی = _math.pi
ای = _math.e
ریشه = _math.sqrt
توان = pow
سینوس = _math.sin
کسینوس = _math.cos
تانژانت = _math.tan
فاکتوریل = _math.factorial
عدد_تصادفی = _random.random
عدد_تصادفی_صحیح = _random.randint
انتخاب_تصادفی = _random.choice
میانگین = _statistics.mean
میانه = _statistics.median
انحراف_معیار = _statistics.stdev
قدر_مطلق = abs
بیشینه = max
کمینه = min
جمع = sum
طول = len
عدد = int
اعشاری_کن = float
متن = str
فهرست = list
مجموعه = set
واژه_نامه = dict
دامنه = range
مرتب = sorted
معکوس = reversed
گرد = round
همه = all
هرکدام = any
شمارش = enumerate
همزمان_سازی = zip
نوع = type
شناسه = id
بازکن = open
کمک = help
نمونه_است = isinstance
زیرکلاس_است = issubclass
ویژگی_دارد = hasattr
ویژگی_بگیر = getattr
ویژگی_بگذار = setattr
متغیرهای_محیط = vars
نام‌ها = dir
پایه = super
قابل_تکرار = iter
بعدی = next
فیلتر = filter
نگاشت = map
گردآوری = repr
کدگذاری = ord
رمزگشایی = chr
کمینه_بزرگ = max
کمینه_کوچک = min
جمع_همه = sum
تبدیل_به_عدد = int
تبدیل_به_اعشاری = float
تبدیل_به_متن = str
تبدیل_به_فهرست = list
تبدیل_به_واژه_نامه = dict
تبدیل_به_مجموعه = set
باقی_مانده = _operator.mod
تقسیم = _operator.truediv
ضرب = _operator.mul
تفریق = _operator.sub
مربع = _operator.pow
ریشه_دوم = _math.sqrt
درجه_به_رادیان = _math.radians
رادیان_به_درجه = _math.degrees

# خطاهای رایج به زبان دری

def _پیام_خطا_دری(خطا):
    نام = type(خطا).__name__
    متن_خطا = str(خطا)
    نام‌ها = {
      'NameError':'نام ناشناخته است', 'TypeError':'نوع داده برای این کار مناسب نیست',
      'ValueError':'مقدار واردشده درست نیست', 'ZeroDivisionError':'تقسیم بر صفر امکان‌پذیر نیست',
      'IndexError':'شمارهٔ خانه بیرون از محدوده است', 'KeyError':'این کلید در واژه‌نامه وجود ندارد',
      'AttributeError':'این ویژگی یا تابع پیدا نشد', 'ImportError':'کتابخانه یا بخش درخواستی پیدا نشد',
      'ModuleNotFoundError':'کتابخانه پیدا نشد یا نصب نیست', 'FileNotFoundError':'فایل پیدا نشد',
      'PermissionError':'اجازهٔ دسترسی داده نشده است', 'AssertionError':'بررسی برنامه ناموفق بود',
      'RecursionError':'تابع بیش از اندازه خودش را فراخوانی کرده است', 'OverflowError':'عدد از محدودهٔ مجاز بزرگ‌تر است',
      'OSError':'در کار با سیستم یا فایل خطا رخ داد', 'EOFError':'ورودی دریافت نشد',
      'ZeroDivisionError':'تقسیم بر صفر امکان‌پذیر نیست', 'StopIteration':'مورد دیگری برای ادامه وجود ندارد'
    }
    پیام = نام‌ها.get(نام, 'خطای اجرا')
    if نام == 'NameError':
        m = re.search(r"name '(.+?)' is not defined", متن_خطا)
        if m: پیام += ': نام «' + m.group(1) + '» تعریف نشده است'
    elif نام in ('TypeError','ValueError','IndexError','KeyError','AttributeError','FileNotFoundError','ModuleNotFoundError'):
        پیام += ': ' + متن_خطا
    return پیام
"""

class مترجم:
    رقم‌ها = str.maketrans('۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩', '01234567890123456789')
    def تبدیل(self, source):
        source = source.translate(self.رقم‌ها).replace('،', ',').replace('؛', ';')
        # شکل کوتاه چاپ سلام / چاپ سلام دنیا نیز پذیرفته می‌شود.
        assigned = set(re.findall(r'^\s*([\w\u0600-\u06ff]+)\s*=', source, re.M))
        new_lines=[]
        for line in source.splitlines():
            # شکل کوتاه چاپ سلام را به چاپ("سلام") تبدیل می‌کنیم.
            m=re.match(r'^(\s*)چاپ\s+(.+?)\s*$', line)
            if m and not m.group(2).startswith('('):
                indent, rest=m.groups()
                if rest.startswith(('"', "'")) or re.match(r'^[\d+\-\[{(]', rest):
                    arg=rest
                elif re.fullmatch(r'[\w\u0600-\u06ff]+', rest) and rest in assigned:
                    arg=rest
                elif any(op in rest for op in (' + ', ' - ', ' * ', ' / ', ' == ', ' >= ', ' <= ')):
                    arg=rest
                else:
                    arg=repr(rest)
                line=indent+'چاپ('+arg+')'
            # شکل کوتاه ورودی نام = ورودی نام شما را هم می‌پذیریم.
            # مثال: نام = ورودی نامت چیست؟  -> نام = ورودی('نامت چیست؟')
            m_in=re.match(r'^(\s*(?:[\w\u0600-\u06ff]+\s*=\s*)?)ورودی\s+(.+?)\s*$', line)
            if m_in and not m_in.group(2).startswith('('):
                left, prompt=m_in.groups()
                line=left+'ورودی('+repr(prompt)+')'
            new_lines.append(line)
        source='\n'.join(new_lines)
        output=[]
        try:
            for t in tokenize.generate_tokens(io.StringIO(source).readline):
                value = واژه_ها.get(t.string, t.string) if t.type == tokenize.NAME else t.string
                output.append((t.type, value))
            return tokenize.untokenize(output)
        except (tokenize.TokenError, IndentationError):
            return source

def تبدیل_خطا(text):
    swaps = {
      'Traceback (most recent call last):':'گزارش خطا:', 'SyntaxError:':'خطای نوشتاری:',
      'IndentationError:':'خطای فاصله‌گذاری:', 'NameError:':'خطای نام:', 'TypeError:':'خطای نوع داده:',
      'ValueError:':'خطای مقدار:', 'ZeroDivisionError:':'خطای تقسیم بر صفر:', 'IndexError:':'خطای شمارهٔ خانه:',
      'KeyError:':'خطای کلید:', 'AttributeError:':'خطای ویژگی:', 'ModuleNotFoundError:':'خطای کتابخانه:',
      'ImportError:':'خطای واردکردن کتابخانه:', 'FileNotFoundError:':'خطای فایل:',
      'PermissionError:':'خطای اجازهٔ دسترسی:', 'line ':'خط '
    }
    for a,b in swaps.items(): text=text.replace(a,b)
    text=re.sub(r"name '(.+?)' is not defined",r'نام «\1» تعریف نشده است',text)
    return text

class هایلایتر(QSyntaxHighlighter):
    def __init__(self,doc):
        super().__init__(doc); self.rules=[]
        f=QTextCharFormat(); f.setForeground(QColor('#ffd166')); f.setFontWeight(QFont.Bold)
        for w in list(واژه_ها)+['چاپ','ورودی','درست','نادرست','هیچ','ریشه','دامنه','جمع','طول']:
            self.rules.append((re.compile(re.escape(w)),f))
        f2=QTextCharFormat(); f2.setForeground(QColor('#8bd49c'))
        self.rules.append((re.compile(r'(".*?"|\'.*?\')'),f2))
        f3=QTextCharFormat(); f3.setForeground(QColor('#75c7f0'))
        self.rules.append((re.compile(r'\b\d+(?:\.\d+)?\b'),f3))
    def highlightBlock(self,text):
        for pat,fmt in self.rules:
            for m in pat.finditer(text): self.setFormat(m.start(),m.end()-m.start(),fmt)

class _جریان_متن:
    """جریان متنی امن برای فرستادن خروجی برنامه به پنجرهٔ ترمینال."""
    def __init__(self, callback):
        self.callback = callback
    def write(self, text):
        if text:
            if hasattr(self.callback, "emit"):
                self.callback.emit(str(text))
            else:
                self.callback(str(text))
        return len(text)
    def flush(self):
        pass
    def isatty(self):
        return True

class _اجراگر(QThread):
    خروجی = Signal(str)
    پایان = Signal()
    درخواست_ورودی = Signal(str)
    def __init__(self, code, parent=None):
        super().__init__(parent)
        self.code = code
        self._بافر_خروجی = []
        import queue
        self._ورودی‌ها = queue.Queue()

    def _فرستادن_خروجی(self, text):
        # نگهداری خروجی در حافظه، تا اگر رابط اندروید سیگنال زنده را دیر دریافت کرد،
        # متن در پایان اجرا نیز قابل بازیابی باشد.
        text = str(text)
        if text:
            # متن هم در بافر نگه داشته می‌شود و هم فوراً با سیگنال Qt به ترمینال می‌رود.
            # تکیهٔ تنها بر زمان‌سنج/بافر در بعضی نسخه‌های اندروید باعث صفحهٔ سیاه خالی می‌شد.
            self._بافر_خروجی.append(text)
            self.خروجی.emit(text)
    def دادن_ورودی(self, text):
        self._ورودی‌ها.put(text)
    def توقف_ورودی(self):
        self._ورودی‌ها.put(None)
    def run(self):
        import builtins

        جریان = _جریان_متن(self._فرستادن_خروجی)

        def چاپ_برنامه(*values, sep=' ', end='\n', file=None, flush=False):
            # خروجی را مستقیم از نخ اجرا به پنجرهٔ ترمینال می‌فرستیم؛
            # از تغییر سراسری sys.stdout که در اندروید مشکل‌ساز می‌شود پرهیز می‌کنیم.
            if file is not None and file not in (sys.stdout, sys.stderr):
                try:
                    builtins.print(*values, sep=sep, end=end, file=file, flush=flush)
                    return
                except Exception:
                    pass
            buffer = io.StringIO()
            builtins.print(*values, sep=sep, end=end, file=buffer, flush=flush)
            جریان.write(buffer.getvalue())

        def ورودی_برنامه(prompt=''):
            self.درخواست_ورودی.emit(str(prompt or ''))
            answer = self._ورودی‌ها.get()
            if answer is None:
                raise EOFError('ورودی توسط کاربر بسته شد')
            return answer

        builtins_تازه = dict(vars(builtins))
        builtins_تازه['print'] = چاپ_برنامه
        builtins_تازه['input'] = ورودی_برنامه
        محیط = {
            '__builtins__': builtins_تازه,
            '__name__': '__main__',
            'print': چاپ_برنامه,
            'چاپ': چاپ_برنامه,
            'نمایش': چاپ_برنامه,
            'ورودی': ورودی_برنامه,
            'ورودی_بگیر': ورودی_برنامه,
        }
        try:
            try:
                exec(compile(پیشوند, '<هستهٔ پایتونی دری>', 'exec'), محیط, محیط)
                # پس از بارگذاری هسته، ورودی و چاپ را به جریان امن همین پنجره وصل نگه می‌داریم.
                محیط['print'] = چاپ_برنامه
                محیط['چاپ'] = چاپ_برنامه
                محیط['نمایش'] = چاپ_برنامه
                محیط['ورودی'] = ورودی_برنامه
                محیط['ورودی_بگیر'] = ورودی_برنامه
                exec(compile(self.code, '<برنامهٔ پایتونی دری>', 'exec'), محیط, محیط)
            except SyntaxError as e:
                پیام‌ها = {
                    'invalid syntax':'ساختار دستور درست نیست',
                    'expected an indented block':'پس از این خط باید دستور با فاصله نوشته شود',
                    'unexpected indent':'در ابتدای این خط فاصلهٔ اضافی وجود دارد',
                    'unindent does not match any outer indentation level':'فاصله‌گذاری با خط‌های پیشین برابر نیست',
                    'unterminated string literal':'نقل‌قول متن بسته نشده است',
                    'was never closed':'یک پرانتز، قلاب یا آکولاد بسته نشده است',
                    'invalid character':'در این خط نویسهٔ نامعتبر وجود دارد'
                }
                پیام = پیام‌ها.get(e.msg, e.msg)
                self._فرستادن_خروجی(f'خطای نوشتاری در پایتونی دری\nشمارهٔ خط: {e.lineno or 1}\nتوضیح: {پیام}\n')
                if e.text:
                    self._فرستادن_خروجی('دستور: ' + e.text.rstrip() + '\n')
            except BaseException as e:
                if isinstance(e, (KeyboardInterrupt, SystemExit)):
                    self._فرستادن_خروجی('اجرای برنامه متوقف شد.\n')
                else:
                    self._فرستادن_خروجی('خطا در برنامهٔ پایتونی دری\n' + _پیام_خطا_دری(e) + '\n')
                    tb = e.__traceback__
                    line = None
                    while tb:
                        if tb.tb_frame.f_code.co_filename == '<برنامهٔ پایتونی دری>':
                            line = tb.tb_lineno
                        tb = tb.tb_next
                    if line is not None:
                        self._فرستادن_خروجی(f'شمارهٔ خط: {line}\n')
        except BaseException as e:
            self._فرستادن_خروجی('خطا در آماده‌سازی برنامه: ' + _پیام_خطا_دری(e) + '\n')
        finally:
            self.پایان.emit()

class ترمینال(QDialog):
    """ترمینال مستقل با پشتیبانی از ورودی واقعی و نمایش راست‌چین دری."""
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle('پایتونی دری — خروجی برنامه')
        self.resize(720, 520)
        self.setWindowModality(Qt.ApplicationModal)
        self.setLayoutDirection(Qt.RightToLeft)
        self.setStyleSheet("""
            QDialog { background:#000000; color:#ffffff; }
            QPlainTextEdit { background:#000000; color:#ffffff; border:0; font-size:18px; padding:12px; }
            QLineEdit { background:#171717; color:#ffffff; border:1px solid #555555; padding:10px; font-size:17px; }
        """)
        lay=QVBoxLayout(self); lay.setContentsMargins(8,12,8,8); lay.setSpacing(7)
        self.out=QPlainTextEdit(); self.out.setReadOnly(True)
        self.out.setFont(QFont('Noto Naskh Arabic', 17))
        self.out.setLayoutDirection(Qt.RightToLeft)
        # QPlainTextEdit برخلاف QTextEdit متد setAlignment ندارد؛ جهت راست‌چین با RTL و فونت تنظیم می‌شود.
        self.out.setContentsMargins(0, 8, 0, 0)
        self.out.setStyleSheet('QPlainTextEdit{background:#000000;color:#ffffff;border:0;font-size:18px;padding:18px 14px 14px 14px;selection-background-color:#394b60;}')
        self.out.setLineWrapMode(QPlainTextEdit.WidgetWidth)
        # خروجی در یک نوار پایین پنجره قرار می‌گیرد؛ فضای سیاه بالای آن دست‌نخورده می‌ماند.
        self.out.setMinimumHeight(120)
        self.out.setMaximumHeight(170)
        lay.addStretch(1)
        lay.addWidget(self.out,0)
        self.inp=QLineEdit(); self.inp.setPlaceholderText('')
        self.inp.setLayoutDirection(Qt.RightToLeft); self.inp.setEnabled(False)
        lay.addWidget(self.inp)
        self.runner=None
        self._output_index=0
        self._output_timer=QTimer(self)
        self._output_timer.setInterval(40)
        self._output_timer.timeout.connect(self._poll_output)
        self.inp.returnPressed.connect(self.sendinput)

    def start_code(self, code):
        self.out.clear()
        self.inp.clear(); self.inp.setEnabled(False)
        self._output_index=0
        self.runner=_اجراگر(code, self)
        # مسیر اصلی نمایش خروجی: هر نوشته با سیگنال Qt مستقیماً به پنجره می‌رسد.
        # زمان‌سنج بافر در بعضی نسخه‌های اندروید می‌توانست با سیگنال‌ها تداخل کند.
        self.runner.خروجی.connect(self._receive_output, Qt.ConnectionType.QueuedConnection)
        self.runner.درخواست_ورودی.connect(self.request_input, Qt.ConnectionType.QueuedConnection)
        self.runner.پایان.connect(self.execution_finished, Qt.ConnectionType.QueuedConnection)
        self._output_timer.stop()
        self.runner.start()

    def _receive_output(self, text):
        # خروجی فقط از مسیر سیگنال نمایش داده می‌شود تا متن تکراری یا گم نشود.
        self.add(text)

    def _poll_output(self):
        runner=self.runner
        if runner is None:
            return
        buffer=runner._بافر_خروجی
        while self._output_index < len(buffer):
            chunk=buffer[self._output_index]
            self._output_index += 1
            self.add(chunk)

    def request_input(self, prompt):
        if prompt:
            self.add(str(prompt))
        self.inp.setEnabled(True)
        self.inp.setFocus()

    def sendinput(self):
        if self.runner and self.runner.isRunning() and self.inp.isEnabled():
            answer=self.inp.text()
            self.add(answer + '\n')
            self.inp.clear(); self.inp.setEnabled(False)
            self.runner.دادن_ورودی(answer)

    def execution_finished(self):
        # خروجی از سیگنال مستقیم می‌رسد؛ بافر را دوباره چاپ نکن تا تکراری نشود.
        self._output_timer.stop()
        self.inp.setEnabled(False)

    def add(self, text):
        if not text:
            return
        cursor=self.out.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        block_format=cursor.blockFormat()
        block_format.setAlignment(Qt.AlignmentFlag.AlignRight)
        cursor.setBlockFormat(block_format)
        cursor.insertText(str(text))
        self.out.setTextCursor(cursor)
        self.out.ensureCursorVisible()

    def closeEvent(self, event):
        self._output_timer.stop()
        if self.runner and self.runner.isRunning():
            self.runner.توقف_ورودی()
            self.runner.wait(1200)
        parent=self.parentWidget()
        if parent is not None:
            parent.show(); parent.raise_(); parent.activateWindow()
        super().closeEvent(event)

class پنجره_کتابخانه(QDialog):
    """فهرست عمودی کتابخانه‌ها؛ بسته‌های بیرونی نیز از همین‌جا نصب می‌شوند."""
    def __init__(self,parent):
        super().__init__(parent)
        self.parent_window=parent
        self.setWindowTitle('کتابخانه‌های پایتونی دری')
        screen=QApplication.primaryScreen()
        if screen is not None:
            area=screen.availableGeometry()
            self.resize(max(320,area.width()-12),max(460,area.height()-12))
        else:
            self.resize(380,680)
        self.setMinimumSize(320,440)
        self.setLayoutDirection(Qt.LeftToRight)
        self.setStyleSheet("""
            QDialog{background:#f5f7fb;color:#172033;}
            QLabel{color:#172033;}
            QPushButton{background:#ffffff;color:#172033;border:1px solid #cbd3df;border-radius:8px;padding:8px;font-size:14px;}
            QPushButton:hover{background:#e8f1ff;border-color:#7da8e8;}
            QPlainTextEdit{background:#ffffff;color:#172033;border:1px solid #cbd3df;padding:8px;font-size:14px;}
            QLineEdit{background:#ffffff;color:#172033;border:1px solid #cbd3df;border-radius:7px;padding:8px;font-size:14px;}
        """)
        root=QVBoxLayout(self); root.setContentsMargins(10,10,10,10); root.setSpacing(8)
        title=QLabel('کتابخانه‌های پایتونی دری'); title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet('font-size:20px;font-weight:bold;'); root.addWidget(title)
        body=QVBoxLayout(); body.setSpacing(8); root.addLayout(body,1)
        self.list_scroll=QScrollArea(); self.list_scroll.setWidgetResizable(True)
        self.list_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.list_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.list_scroll.setMinimumHeight(220)
        self.list_scroll.setMaximumHeight(16777215)
        self.list_scroll.setLayoutDirection(Qt.LeftToRight)
        self.list_scroll.setStyleSheet('QScrollArea{background:transparent;border:1px solid #d5dce7;border-radius:8px;} QScrollBar:vertical{width:9px;background:#e8edf4;} QScrollBar::handle:vertical{background:#9aa8bc;border-radius:4px;min-height:24px;}')
        list_widget=QWidget(); self.list_layout=QVBoxLayout(list_widget)
        self.list_layout.setContentsMargins(5,5,5,5); self.list_layout.setSpacing(5); self.list_layout.setAlignment(Qt.AlignTop)
        self.list_scroll.setWidget(list_widget)
        detail_panel=QWidget(); detail_panel.setLayoutDirection(Qt.RightToLeft)
        detail_layout=QVBoxLayout(detail_panel); detail_layout.setContentsMargins(0,0,0,0); detail_layout.setSpacing(7)
        self.detail=QLabel('برای دیدن توضیح، یک کتابخانه را از فهرست انتخاب کن.')
        self.detail.setWordWrap(True); self.detail.setMinimumHeight(65); self.detail.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.detail.setStyleSheet('font-size:15px;font-weight:bold;padding:5px;background:#eaf0f8;border-radius:7px;')
        detail_layout.addWidget(self.detail)
        self.sample=QPlainTextEdit(); self.sample.setReadOnly(True); self.sample.setMinimumHeight(72); self.sample.setMaximumHeight(112)
        self.sample.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)
        self.sample.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.sample.setLayoutDirection(Qt.LeftToRight); self.sample.setFont(QFont('Noto Sans Mono',10)); detail_layout.addWidget(self.sample)
        self.status=QLabel('فهرست کتابخانه‌ها یک‌ردیفه و عمودی است. کتابخانه‌های استاندارد همراه پایتون‌اند؛ بسته‌های بیرونی باید جداگانه نصب و با اندروید سازگار باشند.')
        self.status.setWordWrap(True); self.status.setStyleSheet('color:#46546a;font-size:12px;'); detail_layout.addWidget(self.status)
        body.addWidget(self.list_scroll,5)
        body.addWidget(detail_panel,2)
        install_row=QHBoxLayout(); self.package_name=QLineEdit(); self.package_name.setPlaceholderText('نام بسته، مانند requests')
        self.install_btn=QPushButton('نصب بسته'); install_row.addWidget(self.package_name,1); install_row.addWidget(self.install_btn); root.addLayout(install_row)
        self.install_output=QPlainTextEdit(); self.install_output.setReadOnly(True); self.install_output.setMaximumHeight(62)
        self.install_output.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)
        self.install_output.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.install_output.setPlaceholderText('پیام‌های نصب در این‌جا نمایش داده می‌شوند.'); root.addWidget(self.install_output)
        actions=QHBoxLayout(); self.use=QPushButton('گذاشتن نمونه در ویرایشگر'); self.close_btn=QPushButton('بستن')
        actions.addWidget(self.use); actions.addWidget(self.close_btn); root.addLayout(actions)
        self.use.clicked.connect(self.insert_sample); self.close_btn.clicked.connect(self.accept)
        self.install_btn.clicked.connect(self.install_package); self.package_name.returnPressed.connect(self.install_package)
        self.current_sample=''; self.install_proc=None
        self.entries=[
          ('ریاضی — math','کتابخانهٔ استاندارد؛ ریشه، توان، پی، سینوس و فاکتوریل.','چاپ(ریشه(۹))\nچاپ(پی)\nچاپ(توان(۲، ۳))'),
          ('اعداد تصادفی — random','کتابخانهٔ استاندارد؛ ساخت عدد و انتخاب تصادفی.','چاپ(عدد_تصادفی_صحیح(۱، ۱۰))'),
          ('آمار — statistics','کتابخانهٔ استاندارد؛ میانگین، میانه و انحراف معیار.','چاپ(میانگین([۲، ۴، ۶]))'),
          ('اعشاری دقیق — decimal','کتابخانهٔ استاندارد؛ محاسبهٔ دقیق اعشاری.','چاپ(اعشاری.Decimal("0.1") + اعشاری.Decimal("0.2"))'),
          ('کسر دقیق — fractions','کتابخانهٔ استاندارد؛ کار با کسرها.','چاپ(کسر.Fraction(۱، ۳) + کسر.Fraction(۱، ۶))'),
          ('دادهٔ جیسون — json','کتابخانهٔ استاندارد؛ خواندن و نوشتن دادهٔ JSON.','چاپ(جیسون.dumps({"نام": "علی"}, ensure_ascii=False))'),
          ('زمان — time','کتابخانهٔ استاندارد؛ زمان و مکث.','چاپ(زمان.time())'),
          ('تاریخ و ساعت — datetime','کتابخانهٔ استاندارد؛ تاریخ و ساعت.','چاپ(تاریخ.datetime.now())'),
          ('مسیر فایل — pathlib','کتابخانهٔ استاندارد؛ مدیریت مسیر فایل‌ها.','چاپ(مسیرها.Path.cwd())'),
          ('سیستم‌عامل — os','کتابخانهٔ استاندارد؛ اطلاعات پوشه‌ها و سیستم‌عامل.','چاپ(سیستم_عامل.getcwd())'),
          ('جست‌وجوی الگو — re','کتابخانهٔ استاندارد؛ پیدا کردن الگو در متن.','چاپ(عبارت_منظم.findall("[0-9]+", "سن 15"))'),
          ('مجموعه‌داده — collections','کتابخانهٔ استاندارد؛ شمارش و گروه‌بندی داده‌ها.','شمارنده = مجموعه_داده.Counter(["سیب", "سیب", "ناک"])\nچاپ(شمارنده)'),
          ('تکرارگرها — itertools','کتابخانهٔ استاندارد؛ ترکیب و تکرار داده‌ها.','چاپ(فهرست(تکرارگرها.chain([۱، ۲], [۳، ۴])))'),
          ('ابزار تابع — functools','کتابخانهٔ استاندارد؛ ابزار ساخت و ترکیب تابع‌ها.','چاپ(ابزار_تابع.reduce(جمع, [۱، ۲، ۳]))'),
          ('عملگرها — operator','کتابخانهٔ استاندارد؛ عملیات عددی و مقایسه‌ای.','چاپ(عملگرها.add(۲، ۳))'),
          ('رشته‌ها — string','کتابخانهٔ استاندارد؛ ابزارهای کار با متن.','چاپ(رشته_ها.ascii_letters[:۱۰])'),
          ('آرایه‌ها — array','کتابخانهٔ استاندارد؛ نگهداری عددهای هم‌نوع.','داده = آرایه.array("i", [۱، ۲، ۳])\nچاپ(داده)'),
          ('فایل فشرده — zipfile','کتابخانهٔ استاندارد؛ کار با فایل‌های ZIP.','چاپ(فایل_فشرده.__name__)'),
          ('پایگاه داده — sqlite3','کتابخانهٔ استاندارد؛ پایگاه دادهٔ SQLite.','پایگاه = پایگاه_داده.connect(":memory:")\nچاپ("پایگاه داده آماده است")'),
          ('شبکه — urllib','کتابخانهٔ استاندارد؛ ابزارهای درخواست و نشانی وب.','چاپ(نشانی_وب.urlparse("https://example.com/path"))'),
          ('آزمون برنامه — unittest','کتابخانهٔ استاندارد؛ آزمودن برنامه‌ها.','چاپ(آزمون.__name__)'),
          ('ثبت رویداد — logging','کتابخانهٔ استاندارد؛ ثبت پیام‌ها و خطاها.','چاپ(ثبت_رویداد.__name__)'),
          ('پردازش چندگانه — multiprocessing','کتابخانهٔ استاندارد؛ اجرای کارها در چند فرایند.','چاپ("کتابخانه آماده است")'),
          ('رمزنگاری — hashlib','کتابخانهٔ استاندارد؛ ساخت اثر انگشت رمزنگاری‌شده از متن.','چاپ(رمزنگاری.sha256("سلام".encode()).hexdigest())'),
          ('جدول داده — csv','کتابخانهٔ استاندارد؛ خواندن و نوشتن داده‌های جدولی CSV.','چاپ(جدول_داده.__name__)'),
          ('ذخیرهٔ داده — pickle','کتابخانهٔ استاندارد؛ ذخیره‌سازی ساختارهای دادهٔ پایتون.','چاپ(ذخیره_داده.__name__)'),
          ('مدیریت نخ‌ها — threading','کتابخانهٔ استاندارد؛ اجرای وظیفه‌ها در نخ‌های جداگانه.','چاپ(نخ.current_thread().name)'),
          ('سوکت شبکه — socket','کتابخانهٔ استاندارد؛ ارتباط شبکه در سطح سوکت.','چاپ(سوکت.__name__)'),
          ('رمزهای امن — secrets','کتابخانهٔ استاندارد؛ تولید مقدارهای تصادفی امن.','چاپ(رمزهای_امن.token_hex(8))'),
          ('مدیریت فایل — shutil','کتابخانهٔ استاندارد؛ کپی و مدیریت فایل‌ها و پوشه‌ها.','چاپ(مدیریت_فایل.__name__)'),
          ('فایل موقت — tempfile','کتابخانهٔ استاندارد؛ ساخت فایل‌ها و پوشه‌های موقت.','چاپ(فایل_موقت.gettempdir())'),
          ('ورودی و خروجی — io','کتابخانهٔ استاندارد؛ کار با جریان‌های متن و بایت.','چاپ(ورودی_خروجی.StringIO("سلام").getvalue())'),
          ('مدیریت زمینه — contextlib','کتابخانهٔ استاندارد؛ ساخت و مدیریت زمینه‌های اجرایی.','چاپ(مدیریت_زمینه.__name__)'),
          ('هشدارها — warnings','کتابخانهٔ استاندارد؛ نمایش و مدیریت هشدارهای برنامه.','چاپ(هشدارها.__name__)'),
          ('گزارش خطا — traceback','کتابخانهٔ استاندارد؛ بررسی و نمایش جزئیات خطاها.','چاپ(گزارش_خطا.__name__)'),
          ('مقایسهٔ متن — difflib','کتابخانهٔ استاندارد؛ مقایسهٔ رشته‌ها و پیدا کردن تفاوت‌ها.','چاپ(مقایسه_متن.__name__)'),
          ('الگوی نام فایل — fnmatch','کتابخانهٔ استاندارد؛ بررسی نام فایل با الگو.','چاپ(الگوی_نام_فایل.fnmatch("برنامه.py", "*.py"))'),
          ('جست‌وجوی فایل — glob','کتابخانهٔ استاندارد؛ پیدا کردن فایل‌ها با الگو.','چاپ(جستجوی_فایل.__name__)'),
          ('نوع‌نویسی — typing','کتابخانهٔ استاندارد؛ نوشتن راهنمای نوع داده برای کد.','چاپ(نوع_داده.__name__)'),
          ('ساختار داده — dataclasses','کتابخانهٔ استاندارد؛ تعریف کلاس‌های داده‌ای ساده‌تر.','چاپ(ساختار_داده.__name__)'),
          ('نوع‌های ثابت — enum','کتابخانهٔ استاندارد؛ تعریف مجموعه‌ای از مقدارهای نام‌دار.','چاپ(شمارش_ثابت.__name__)'),
          ('رمزگذاری پایه — base64','کتابخانهٔ استاندارد؛ تبدیل بایت‌ها به متن Base64.','چاپ(رمزگذاری_بنیادی.b64encode("سلام".encode()).decode())'),
          ('فشرده‌سازی داده — zlib','کتابخانهٔ استاندارد؛ فشرده‌سازی و بازکردن داده‌ها.','چاپ(فشرده_سازی.decompress(فشرده_سازی.compress(b"hello")))'),
          ('فشرده‌سازی فایل — gzip','کتابخانهٔ استاندارد؛ خواندن و نوشتن دادهٔ فشردهٔ gzip.','چاپ(فشرده_سازی_فایل.__name__)'),
          ('شناسهٔ یکتا — uuid','کتابخانهٔ استاندارد؛ ساخت شناسه‌های یکتا.','چاپ(شناسه_جهانی.uuid4())'),
          ('اجرای فرمان — subprocess','کتابخانهٔ استاندارد؛ اجرای فرایندهای بیرونی؛ با احتیاط استفاده شود.','چاپ(اجرای_فرمان.__name__)'),
          ('درخواست شبکه — requests','بستهٔ بیرونی؛ درخواست به وب و دریافت پاسخ.','واردکن requests\nچاپ(requests.__version__)'),
          ('آرایه‌های عددی — numpy','بستهٔ بیرونی؛ محاسبه با آرایه‌های عددی.','واردکن numpy as نامپای\nچاپ(نامپای.array([۱، ۲، ۳]))'),
          ('تحلیل داده — pandas','بستهٔ بیرونی؛ جدول‌ها و تحلیل داده.','واردکن pandas as پاندا\nچاپ(پاندا.__version__)'),
          ('رسم نمودار — matplotlib','بستهٔ بیرونی؛ ساخت نمودار.','واردکن matplotlib.pyplot as نمودار\nچاپ("کتابخانهٔ نمودار آماده است")'),
          ('کار با تصویر — Pillow','بستهٔ بیرونی؛ بازکردن و ویرایش تصویر.','واردکن PIL\nچاپ(PIL.__version__)'),
          ('یادگیری ماشین — scikit-learn','بستهٔ بیرونی؛ ابزارهای یادگیری ماشین؛ سازگاری اندروید باید بررسی شود.','واردکن sklearn\nچاپ(sklearn.__version__)'),
          ('بازی‌سازی — pygame','بستهٔ بیرونی؛ ساخت بازی‌های دوبعدی.','چاپ("برای استفاده، بستهٔ pygame باید نصب باشد.")'),
          ('وب‌سرور — flask','بستهٔ بیرونی؛ ساخت وب‌سایت و سرویس وب.','واردکن flask\nچاپ(flask.__version__)'),
          ('رابط وب — streamlit','بستهٔ بیرونی؛ ساخت برنامهٔ وب.','چاپ("برای استفاده، بستهٔ streamlit باید نصب باشد.")'),
          ('ساخت API — fastapi','بستهٔ بیرونی؛ ساخت API وب.','واردکن fastapi\nچاپ(fastapi.__version__)'),
          ('خواندن صفحهٔ وب — beautifulsoup4','بستهٔ بیرونی؛ خواندن و بررسی HTML.','واردکن bs4\nچاپ(bs4.__version__)'),
          ('پردازش تصویر — opencv-python','بستهٔ بیرونی؛ ابزارهای پردازش تصویر؛ نصب روی اندروید ممکن است محدود باشد.','واردکن cv2\nچاپ(cv2.__version__)'),
          ('مدل‌های زبانی — transformers','بستهٔ بیرونی؛ نصب این بسته به‌تنهایی مدل هوش مصنوعی را دریافت نمی‌کند.','چاپ("مدل زبانی جداگانه و فضای ذخیره‌سازی نیاز دارد.")'),
          ('یادگیری عمیق — torch','بستهٔ بیرونی بزرگ؛ ممکن است روی Pydroid/اندروید نصب نشود.','چاپ("پیش از نصب، سازگاری بسته با اندروید را بررسی کن.")'),
          ('پردازش صدا — librosa','بستهٔ بیرونی؛ تحلیل صدا؛ ممکن است وابستگی‌های اضافی لازم داشته باشد.','چاپ("پیش از نصب، سازگاری بسته با اندروید را بررسی کن.")'),
        ]
        self.package_map={
          'درخواست شبکه — requests':'requests',
          'آرایه‌های عددی — numpy':'numpy',
          'تحلیل داده — pandas':'pandas',
          'رسم نمودار — matplotlib':'matplotlib',
          'کار با تصویر — Pillow':'Pillow',
          'یادگیری ماشین — scikit-learn':'scikit-learn',
          'بازی‌سازی — pygame':'pygame',
          'وب‌سرور — flask':'flask',
          'رابط وب — streamlit':'streamlit',
          'ساخت API — fastapi':'fastapi',
          'خواندن صفحهٔ وب — beautifulsoup4':'beautifulsoup4',
          'پردازش تصویر — opencv-python':'opencv-python',
          'مدل‌های زبانی — transformers':'transformers',
          'یادگیری عمیق — torch':'torch',
          'پردازش صدا — librosa':'librosa',
        }
        # Pydroid Repository Plugin یک افزونهٔ اندرویدی است، نه بستهٔ pip؛ نصب آن از این فهرست انجام نمی‌شود.
        self.entries.append(('افزونهٔ مخزن Pydroid','برای بعضی کتابخانه‌های دارای کد بومی در اندروید لازم است. این مورد افزونهٔ خود اندروید است، نه بستهٔ pip.','چاپ("برای بسته‌های دارای کد بومی، سازگاری با Pydroid و افزونهٔ مخزن آن را بررسی کن.")'))
        self.library_buttons={}
        seen_names=set()
        for n,d,e in self.entries:
            if n in seen_names:
                continue
            seen_names.add(n)
            row=QWidget(); row.setLayoutDirection(Qt.RightToLeft)
            row_lay=QHBoxLayout(row); row_lay.setContentsMargins(0,0,0,0); row_lay.setSpacing(6)
            b=QPushButton(n); b.setMinimumHeight(44); b.setMaximumHeight(44); b.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed)
            b.setStyleSheet('text-align:right;padding:7px 10px;font-size:14px;')
            b.clicked.connect(lambda checked=False,name=n,desc=d,example=e:self.show_library(name,desc,example))
            row_lay.addWidget(b,1)
            package=self.package_map.get(n)
            if n == 'افزونهٔ مخزن Pydroid':
                install=QPushButton('✓ افزونه')
                install.setEnabled(False)
                install.setToolTip('این افزونهٔ اندرویدی جدا از pip است؛ گفتی که آن را نصب کرده‌ای.')
            else:
                install=QPushButton('⬇ نصب' if package else '✓ آماده')
            install.setFixedSize(82,44)
            if package:
                install.setStyleSheet('QPushButton{background:#21865b;color:white;font-weight:bold;border-radius:7px;} QPushButton:hover{background:#176b46;}')
                install.clicked.connect(lambda checked=False,pkg=package:self.install_named_package(pkg))
            elif n != 'افزونهٔ مخزن Pydroid':
                install.setEnabled(False)
                install.setToolTip('این کتابخانه همراه پایتون است یا بخش توضیحی است و نصب جداگانه ندارد.')
            row_lay.addWidget(install)
            self.library_buttons[n]=(b,install)
            self.list_layout.addWidget(row)
        self.show_library(*self.entries[0])
    def show_library(self,n,d,e):
        self.detail.setText(n+' — '+d); self.current_sample=e; self.sample.setPlainText(e)
    def insert_sample(self):
        if self.current_sample and self.parent_window:
            self.parent_window.editor.insertPlainText(self.current_sample); self.parent_window.show(); self.parent_window.activateWindow(); self.accept()
    def install_named_package(self, package):
        self.package_name.setText(package)
        self.install_package()

    def install_package(self):
        name=self.package_name.text().strip()
        if not name:
            self.status.setText('اول نام بسته را بنویس؛ مثلاً requests.'); return
        if not re.fullmatch(r'[A-Za-z0-9_.-]+',name):
            self.status.setText('نام بسته معتبر نیست؛ از حروف انگلیسی، عدد، نقطه، خط زیر یا خط تیره استفاده کن.'); return
        if self.install_proc and self.install_proc.state()!=QProcess.NotRunning:
            self.status.setText('یک نصب دیگر هنوز در جریان است؛ صبر کن.'); return
        self.install_output.clear()
        self.install_output.appendPlainText('بسته: '+name)
        self.install_output.appendPlainText('مفسر فعال: '+sys.executable)
        try:
            import site
            paths = site.getsitepackages()
            if paths: self.install_output.appendPlainText('محل نصب همین محیط: '+str(paths[0]))
            else: self.install_output.appendPlainText('محل نصب: محیط فعال پایتون')
        except Exception:
            self.install_output.appendPlainText('محل نصب: محیط فعال پایتون')
        self.install_output.appendPlainText('در حال نصب در همین محیط پایتون…')
        self.install_btn.setEnabled(False)
        self.install_proc=QProcess(self); self.install_proc.setProcessChannelMode(QProcess.MergedChannels)
        self.install_proc.readyReadStandardOutput.connect(self._read_install_output); self.install_proc.finished.connect(self._install_finished)
        env=QProcessEnvironment.systemEnvironment(); env.insert('PYTHONUNBUFFERED','1'); env.insert('PYTHONIOENCODING','utf-8'); self.install_proc.setProcessEnvironment(env)
        self.install_proc.start(sys.executable,['-m','pip','install','--disable-pip-version-check',name])
        if not self.install_proc.waitForStarted(5000):
            self.install_output.appendPlainText('فرایند نصب آغاز نشد: '+تبدیل_خطا(self.install_proc.errorString())); self.install_btn.setEnabled(True)
    def _read_install_output(self):
        if self.install_proc: self.install_output.appendPlainText(bytes(self.install_proc.readAllStandardOutput()).decode('utf-8','replace'))
    def _install_finished(self,code,status):
        self._read_install_output(); self.install_btn.setEnabled(True)
        if code==0: self.status.setText('نصب بسته پایان یافت؛ اگر با نسخهٔ اندروید سازگار باشد، آمادهٔ استفاده است.')
        else: self.status.setText('نصب انجام نشد؛ پیام خطا را در کادر پایین بخوان. بعضی بسته‌ها ابزارهای اضافی می‌خواهند.')
class برنامه(QMainWindow):
    def __init__(self):
        super().__init__(); self.setWindowTitle('پایتونی دری'); self.resize(900,700); self.path=None; self.fontsize=17
        self.setStyleSheet('QMainWindow{background:#101722;} QWidget{color:#e8edf5;} QPushButton{background:#263448;color:#f5f7fb;border:0;border-radius:7px;padding:9px 12px;} QPushButton:hover{background:#354a63;} QLabel{color:#c9d5e5;}')
        central=QWidget(); self.setCentralWidget(central); root=QVBoxLayout(central); root.setContentsMargins(10,10,10,8); root.setSpacing(8)
        bar=QHBoxLayout(); bar.setSpacing(7)
        for label,fn in [('☰',self.menu),('📂',self.open_file),('＋',self.new_file),('💾',self.save_file),('📚',self.libraries),('⚙',self.settings)]:
            b=QPushButton(label); b.setFixedSize(43,42); b.clicked.connect(fn); bar.addWidget(b)
        bar.addStretch(1); run=QPushButton('▶'); run.setFixedSize(54,42); run.setStyleSheet('QPushButton{background:#f6c85f;color:#101722;font-size:23px;font-weight:bold;border-radius:8px;} QPushButton:hover{background:#ffda78;}'); run.clicked.connect(self.run_code); bar.addWidget(run); root.addLayout(bar)
        self.editor=QPlainTextEdit(); self.editor.setFont(QFont('Noto Naskh Arabic',self.fontsize)); self.editor.setLayoutDirection(Qt.LeftToRight)
        self.editor.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)
        self.editor.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.editor.setTabStopDistance(self.editor.fontMetrics().horizontalAdvance('    '))
        # صفحهٔ اصلی ویرایش کد به رنگ خاکستری برمی‌گردد؛ ترمینال سیاه باقی می‌ماند.
        self.editor.setStyleSheet('QPlainTextEdit{background:#303844;color:#f2f5fa;border:1px solid #566273;border-radius:8px;padding:10px;font-size:17px;selection-background-color:#526985;selection-color:#ffffff;}')
        self.editor.setPlaceholderText('برنامهٔ دری خود را این‌جا بنویسید…'); self.editor.clear(); self.highlighter=هایلایتر(self.editor.document()); root.addWidget(self.editor,1)
        footer=QLabel('پایتونی دری'); footer.setAlignment(Qt.AlignCenter); footer.setStyleSheet('color:#f6c85f;font-size:13px;font-weight:bold;padding-top:3px;'); root.addWidget(footer)
    def new_file(self): self.editor.clear(); self.path=None; self.setWindowTitle('پایتونی دری')
    def _file_dialog(self, title, mode, default_name='', filters='همهٔ فایل‌ها (*)'):
        start_path = str(Path.home() / default_name) if default_name else str(Path.home())
        dialog=QFileDialog(self, title, start_path)
        dialog.setOption(QFileDialog.Option.DontUseNativeDialog, True)
        dialog.setLayoutDirection(Qt.LeftToRight)
        dialog.setMinimumSize(320, 420)
        dialog.setStyleSheet("""
            QFileDialog, QWidget { background:#f5f7fb; color:#172033; }
            QLabel { color:#172033; }
            QTreeView, QListView, QTableView { background:#ffffff; color:#172033; selection-background-color:#cfe2ff; selection-color:#172033; }
            QLineEdit, QComboBox { background:#ffffff; color:#172033; border:1px solid #aeb9c9; padding:5px; }
            QPushButton { background:#e6edf7; color:#172033; border:1px solid #b9c5d5; border-radius:5px; padding:6px 10px; }
        """)
        dialog.setNameFilter(filters)
        if mode == 'open':
            dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
            dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        else:
            dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
            dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        screen = QApplication.primaryScreen()
        if screen is not None:
            dialog.setGeometry(screen.availableGeometry())
        if dialog.exec():
            files=dialog.selectedFiles()
            return files[0] if files else ''
        return ''
    def open_file(self):
        path=self._file_dialog('بازکردن برنامه','open','', 'برنامه‌های دری (*.dari *.py *.txt);;همهٔ فایل‌ها (*)')
        if path:
            try:
                self.editor.setPlainText(Path(path).read_text(encoding='utf-8'))
                self.path=path
            except Exception as e:
                QMessageBox.critical(self,'خطای بازکردن','فایل باز نشد:\n'+تبدیل_خطا(str(e)))
    def save_file(self):
        path=self.path
        if not path:
            path=self._file_dialog('ذخیرهٔ برنامه','save','برنامه_من.dari','برنامهٔ دری (*.dari);;فایل متنی (*.txt)')
        if path:
            try:
                Path(path).write_text(self.editor.toPlainText(),encoding='utf-8')
                self.path=path
            except Exception as e:
                QMessageBox.critical(self,'خطای ذخیره','فایل ذخیره نشد:\n'+تبدیل_خطا(str(e)))
    def libraries(self):
        dialog=پنجره_کتابخانه(self)
        dialog.setWindowState(Qt.WindowState.WindowFullScreen)
        dialog.exec()
    def settings(self):
        value,ok=QInputDialog.getInt(self,'تنظیمات','اندازهٔ نوشته‌ها:',self.fontsize,10,40)
        if ok: self.fontsize=value; f=self.editor.font(); f.setPointSize(value); self.editor.setFont(f)
    def menu(self):
        item,ok=QInputDialog.getItem(self,'منو','یک بخش را انتخاب کنید:',['برنامهٔ نو','بازکردن فایل','ذخیرهٔ فایل','کتابخانه‌ها','تنظیمات','آموزش کوتاه'],0,False)
        if ok: {'برنامهٔ نو':self.new_file,'بازکردن فایل':self.open_file,'ذخیرهٔ فایل':self.save_file,'کتابخانه‌ها':self.libraries,'تنظیمات':self.settings,'آموزش کوتاه':self.help}[item]()
    def help(self):
        QMessageBox.information(self,'آموزش کوتاه','چاپ("سلام") یا حتی چاپ سلام برای نمایش متن\nنام = "علی" برای ساخت متغیر\n\nاگر سن >= ۱۸:\n    چاپ("بزرگسال")\nوگرنه:\n    چاپ("کمتر از ۱۸")\n\nتابع جمع_دو(الف، ب):\n    برگردان الف + ب\n\nبرای عدد در دامنه(۵):\n    چاپ(عدد)\n\nبرای دریافت پاسخ: نام = ورودی("نامت چیست؟ ")')
    def run_code(self):
        source=self.editor.toPlainText()
        if not source.strip():
            QMessageBox.information(self,'برنامه خالی است','اول یک دستور بنویس؛ مثلاً چاپ("سلام")')
            return
        try:
            code=مترجم().تبدیل(source)
        except Exception as e:
            self._terminal_dialog=ترمینال(self)
            self._terminal_dialog.add('خطا هنگام آماده‌سازی برنامه به دری:\n'+تبدیل_خطا(str(e))+'\n')
            self.hide(); self._terminal_dialog.showFullScreen(); return
        try:
            self._terminal_dialog=ترمینال(self)
            self._terminal_dialog.setAttribute(Qt.WA_DeleteOnClose,True)
            self._terminal_dialog.finished.connect(self._terminal_closed)
            self._pending_program=code
            self.hide()
            self._terminal_dialog.showFullScreen()
            self._terminal_dialog.raise_()
            self._terminal_dialog.activateWindow()
            # اجرای کد پس از ساخته‌شدن پنجره؛ خطای شروع نیز در خود ترمینال نشان داده می‌شود.
            QTimer.singleShot(250, self._start_pending_program)
        except Exception as e:
            self.show()
            QMessageBox.critical(self,'خطای اجرای برنامه','پنجرهٔ اجرا ساخته نشد:\n'+تبدیل_خطا(str(e)))

    def _start_pending_program(self):
        dialog=getattr(self,'_terminal_dialog',None)
        if dialog is None:
            self.show()
            return
        try:
            dialog.start_code(getattr(self,'_pending_program',''))
        except Exception as e:
            dialog.add('خطا هنگام آغاز اجرا:\n'+تبدیل_خطا(str(e))+'\n')

    def _terminal_closed(self):
        if not self.isVisible():
            self.show()
            self.raise_()
            self.activateWindow()

if __name__=='__main__':
    try:
        app=QApplication(sys.argv); app.setApplicationName('پایتونی دری'); window=برنامه(); window.show(); sys.exit(app.exec())
    except Exception:
        try: Path.home().joinpath('paitooni_dari_error.txt').write_text(traceback.format_exc(),encoding='utf-8')
        except Exception: pass
        raise
