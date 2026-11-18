#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
پایتون دری  (Dari Python) — نسخهٔ ۱٫۰
==========================================

یک زبان برنامه‌نویسی با دستورهای دری/فارسی که روی «پایتون ۳» اجرا می‌شود.
هر برنامه‌ای که به دری بنویسید، به پایتون ۳ اصلی ترجمه و با همان اجرا می‌شود؛
بنابراین «همهٔ کتابخانه‌های پایتون» (requests، flask، numpy، torch، pyserial، ...)
با همان نام اصلی‌شان کار می‌کنند. شما می‌توانید با آن نرم‌افزار، چت‌بات، پیام‌رسان،
هوش مصنوعی و برنامهٔ سخت‌افزاری بنویسید.

فقط از کتابخانهٔ استاندارد پایتون استفاده شده — نصب چیزی لازم نیست.
محیط برنامه‌نویسی در مرورگرِ همان دستگاه (به‌صورت محلی و آفلاین) باز می‌شود، پس
خط فارسی درست و متصل نمایش داده می‌شود (بدون تیکنتر و کیوی).

روش استفاده
-----------
    python3 dari_python.py                 ← باز کردن محیط برنامه‌نویسی
    python3 dari_python.py ide [پوشه]      ← محیط با پوشهٔ دلخواه
    python3 dari_python.py run برنامه.dpy  ← اجرای یک فایل دری
    python3 dari_python.py shell           ← پوستهٔ تعاملی دری
    python3 dari_python.py translate برنامه.dpy   ← دیدن کد پایتونِ معادل

پسوند فایل‌های دری: .dpy
"""

import builtins
import code as _code
import codecs
import hmac
import importlib.abc
import importlib.machinery
import importlib.util
import io
import json
import keyword
import linecache
import os
import re
import secrets
import shutil
import socket
import subprocess
import sys
import threading
import time
import tokenize
import traceback
import types
import urllib.parse
import hashlib
import webbrowser
import http.server

__version__ = "1.0"

# ════════════════════════════════════════════════════════════════════
#  ۱. واژگان زبان
# ════════════════════════════════════════════════════════════════════

_DUPS = []


def _pairs(text, name=""):
    d = {}
    for tok in text.split():
        fa, en = tok.split("=", 1)
        en = en.replace("~", " ")
        if fa in d:
            _DUPS.append((name, fa))
        d[fa] = en
    return d


KEYWORDS = _pairs("""
درست=True نادرست=False هیچ=None
و=and یا=or نه=not نیست=is~not است=is در=in
اگر=if وگرنه_اگر=elif وگرنه=else
برای=for تا_وقتی=while تا_وقتی_که=while تا_زمانی=while تا_زمانی_که=while
بشکن=break ادامه=continue بگذر=pass
تابع=def برگردان=return کلاس=class لامبدا=lambda تولید=yield تولید_از=yield~from
بیازما=try بجز=except سرانجام=finally بیانداز=raise ادعا=assert
با=with بنام=as به_عنوان=as وارد_کن=import از=from
سراسری=global غیرمحلی=nonlocal حذف=del ناهمگام=async انتظار=await
""", "keywords")

SOFT = {"تطبیق": "match", "حالت": "case"}

BUILTINS = _pairs("""
چاپ=print ورودی=input طول=len دامنه=range صحیح=int اعشاری=float متن=str منطقی=bool
فهرست=list قاموس=dict چندتایی=tuple مجموعه=set مجموعه_ثابت=frozenset نوع=type
نمونه_است=isinstance زیرکلاس_است=issubclass بازکن=open مجموع=sum کمترین=min بیشترین=max
قدرمطلق=abs گرد=round مرتب=sorted معکوس=reversed شمارش=enumerate جفت=zip نگاشت=map
پالایش=filter هرکدام=any همه=all نویسه=chr کد_نویسه=ord شانزده=hex دودویی=bin هشت=oct
توان=pow خارج_قسمت=divmod شناسه=id هش_مقدار=hash ویژگی_ها=dir متغیرها=vars
ویژگی_بگیر=getattr ویژگی_بگذار=setattr ویژگی_دارد=hasattr ویژگی_حذف=delattr
فراخوانی_پذیر=callable تکرارگر=iter بعدی=next شیء=object والد=super ویژگی=property
متد_ایستا=staticmethod متد_کلاس=classmethod قالب=format نمایش=repr ارزیابی=eval اجرا=exec
ترجمه_کد=compile سراسری_ها=globals محلی_ها=locals بایت_ها=bytes آرایه_بایت=bytearray
مختلط=complex برش=slice راهنما=help خروج=exit ترک=quit
استثنا=Exception استثنای_پایه=BaseException خطای_مقدار=ValueError خطای_نوع=TypeError
خطای_نام=NameError خطای_اندیس=IndexError خطای_کلید=KeyError خطای_صفر=ZeroDivisionError
خطای_ویژگی=AttributeError خطای_وارد_کردن=ImportError خطای_ماژول=ModuleNotFoundError
خطای_فایل=FileNotFoundError خطای_سیستم=OSError خطای_اجرا=RuntimeError
پایان_تکرار=StopIteration وقفه_کاربر=KeyboardInterrupt خطای_ادعا=AssertionError
خطای_پیاده_نشده=NotImplementedError خطای_دسترسی=PermissionError خطای_زمان=TimeoutError
خطای_سرریز=OverflowError خطای_بازگشت=RecursionError خطای_نحو=SyntaxError
خطای_یونیکد=UnicodeError خطای_اتصال=ConnectionError خطای_پایان_ورودی=EOFError
خروج_سیستم=SystemExit پیاده_نشده=NotImplemented
""", "builtins")

DUNDERS = _pairs("""
__آغاز__=__init__ __متن__=__str__ __نمایش__=__repr__ __طول__=__len__ __نام__=__name__
__فراخوانی__=__call__ __گرفتن_مورد__=__getitem__ __گذاشتن_مورد__=__setitem__
__حذف_مورد__=__delitem__ __تکرار__=__iter__ __بعدی__=__next__ __ورود__=__enter__
__خروج__=__exit__ __جمع__=__add__ __تفریق__=__sub__ __ضرب__=__mul__ __تقسیم__=__truediv__
__برابر__=__eq__ __کوچکتر__=__lt__ __بزرگتر__=__gt__ __شامل__=__contains__ __حذف__=__del__
__توضیح__=__doc__ __فایل__=__file__ __قاموس__=__dict__ __کلاس__=__class__ __منطقی__=__bool__
__هش__=__hash__
""", "dunders")

KWARGS = _pairs("""
جداکننده=sep پایان=end فایل=file تخلیه=flush کلید=key وارونه=reverse کدگذاری=encoding
حالت=mode خط_جدید=newline پیش_فرض=default شروع=start مهلت=timeout پس_زمینه=daemon
هدف=target آرگومان_ها=args تورفتگی=indent فقط_اسکی=ensure_ascii
""", "kwargs")

ATTRS = _pairs("""
افزودن=append گسترش=extend درج=insert برداشتن=remove درآوردن=pop پاک_کردن=clear
جایگاه=index تعداد=count مرتب_کردن=sort وارونه_کردن=reverse رونوشت=copy
بزرگ_کردن=upper کوچک_کردن=lower حذف_فاصله=strip حذف_فاصله_چپ=lstrip حذف_فاصله_راست=rstrip
تقسیم=split پیوند=join جایگزین=replace پیدا_کردن=find شروع_با=startswith پایان_با=endswith
قالب_بندی=format رقم_است=isdigit حرف_است=isalpha حرف_یا_رقم_است=isalnum
عنوان_کردن=title بزرگ_اول=capitalize کدگذاری_کردن=encode کدگشایی=decode خط_ها=splitlines
صفرپر=zfill وسط_چین=center چپ_چین=ljust راست_چین=rjust بزرگ_است=isupper کوچک_است=islower
کلیدها=keys مقدارها=values موردها=items بگیر=get بروزرسانی=update پیش_فرض_بگذار=setdefault
اضافه_کردن=add دور_انداختن=discard اجتماع=union اشتراک=intersection تفاضل=difference
زیرمجموعه_است=issubset
خواندن=read نوشتن=write یک_خط_بخوان=readline خط_ها_بخوان=readlines بستن=close
تخلیه_کن=flush برو_به=seek
جذر=sqrt سینوس=sin کسینوس=cos تانژانت=tan عدد_پی=pi عدد_نپر=e کف=floor سقف=ceil
لگاریتم=log لگاریتم_ده=log10 نمایی=exp فاکتوریل=factorial بزرگترین_مقسوم_علیه=gcd
رادیان=radians درجه=degrees وتر=hypot بی_نهایت=inf قطع=trunc آرک_تانژانت=atan توان=pow
تصادفی_اعشاری=random عدد_تصادفی=randint انتخاب=choice چند_انتخاب=choices بر_زدن=shuffle
یکنواخت=uniform بذر=seed نمونه_گیری=sample بازه_تصادفی=randrange
بخواب=sleep ثانیه_کنونی=time قالب_زمان=strftime زمان_محلی=localtime
شمارنده_دقیق=perf_counter تبدیل_زمان=strptime
تاریخ_زمان=datetime اکنون=now امروز=today تاریخ=date بازه_زمانی=timedelta سال=year
ماه=month روز=day ساعت=hour دقیقه=minute ثانیه=second
فهرست_پوشه=listdir ساخت_پوشه=mkdir ساخت_پوشه_ها=makedirs حذف_فایل=remove حذف_پوشه=rmdir
تغییر_نام=rename پوشه_جاری=getcwd رفتن_به_پوشه=chdir دستور_سیستم=system محیط=environ
متغیر_محیط=getenv مسیر=path وجود_دارد=exists فایل_است=isfile پوشه_است=isdir
نام_پایه=basename پوشه_والد=dirname مسیر_کامل=abspath جداکننده_مسیر=sep
آرگومان_های_برنامه=argv خروج=exit پلتفرم=platform نسخه=version ورودی_استاندارد=stdin
خروجی_استاندارد=stdout خطای_استاندارد=stderr ماژول_ها=modules
بارگذاری_متن=loads متن_جیسون=dumps بارگذاری=load ذخیره_جیسون=dump
تطبیق_ابتدا=match جستجوی_الگو=search همه_یافته_ها=findall جایگزینی_الگو=sub
کامپایل_الگو=compile
سوکت=socket اتصال_به_پورت=bind گوش_بده=listen بپذیر=accept وصل_شو=connect
بفرست=send همه_را_بفرست=sendall دریافت=recv مهلت_سوکت=settimeout
نخ=Thread شروع_کن=start قفل=Lock رویداد=Event
اتصال_پایگاه=connect نشانگر=cursor ثبت=commit همه_را_بگیر=fetchall یکی_را_بگیر=fetchone
شمارنده=Counter قاموس_پیش_فرض=defaultdict صف_دوطرفه=deque قاموس_مرتب=OrderedDict
میانگین=mean میانه=median انحراف_معیار=stdev
اجرای_برنامه=run خروجی_دستور=check_output مسیر_فایل=Path
خواننده=reader نویسنده=writer کاهش=reduce
جایگشت_ها=permutations ترکیب_ها=combinations ضرب_دکارتی=product
حروف_کوچک=ascii_lowercase حروف_بزرگ=ascii_uppercase ارقام=digits
""", "attrs")
# «اجرا» به‌عنوان متد (sqlite3 و ...) → execute
ATTRS["اجرا"] = "execute"

MODULES = _pairs("""
ریاضی=math تصادفی=random زمان=time تاریخ_زمان=datetime سیستم_عامل=os سیستم=sys
جیسون=json عبارت_منظم=re سوکت=socket نخ_ها=threading پایگاه_داده=sqlite3
رشته_ها=string مجموعه_ها=collections تکرارگرها=itertools ابزار_توابع=functools
مسیرها=pathlib آمار=statistics زیرپردازش=subprocess هش=hashlib فایل_سی_اس_وی=csv
گزارش_گیری=logging نوع_ها=typing کپی_برداری=copy ابزار_فایل=shutil
فایل_موقت=tempfile مرورگر=webbrowser شناسه_یکتا=uuid
""", "modules")


# ── واژگان تکمیلی: همهٔ نام‌های استانداردِ باقی‌مانده ─────────────────
BUILTINS.update(_pairs("""
خطای_حسابی=ArithmeticError خطای_جستجو=LookupError خطای_حافظه=MemoryError
خطای_تورفتگی=IndentationError خطای_تب=TabError خطای_سیستمی=SystemError
خطای_فایل_موجود=FileExistsError خطای_پوشه_است=IsADirectoryError
خطای_پوشه_نیست=NotADirectoryError خطای_قطع_اتصال=ConnectionResetError
خطای_رد_اتصال=ConnectionRefusedError خطای_لوله_شکسته=BrokenPipeError
خطای_مرجع=ReferenceError خطای_متغیر_محلی=UnboundLocalError
خطای_رمزگشایی=UnicodeDecodeError خطای_رمزگذاری=UnicodeEncodeError
خطای_اعشاری=FloatingPointError خطای_ورودی_خروجی=IOError خطای_محیط=EnvironmentError
خطای_بافر=BufferError خطای_فرایند=ChildProcessError خطای_وقفه=InterruptedError
خطای_مسدود=BlockingIOError خطای_فرایند_یافت_نشد=ProcessLookupError
پایان_مولد=GeneratorExit پایان_تکرار_ناهمگام=StopAsyncIteration
هشدار=Warning هشدار_کاربر=UserWarning هشدار_منسوخ=DeprecationWarning
هشدار_آینده=FutureWarning هشدار_اجرا=RuntimeWarning هشدار_نحو=SyntaxWarning
هشدار_منابع=ResourceWarning هشدار_یونیکد=UnicodeWarning گروه_استثنا=ExceptionGroup
سه_نقطه=Ellipsis ازبین_رفتن_تکرارگر=aiter بعدی_ناهمگام=anext اسکی=ascii
نقطه_توقف=breakpoint نمای_حافظه=memoryview مجوز=license حق_نشر=copyright
""", "builtins2"))

ATTRS.update(_pairs("""
حروف_کوچک_کامل=casefold گسترش_تب=expandtabs قالب_نگاشتی=format_map اسکی_است=isascii
ده_دهی_است=isdecimal شناسه_است=isidentifier عددی_است=isnumeric چاپ_پذیر_است=isprintable
فاصله_است=isspace عنوان_است=istitle جدول_ترجمه=maketrans بخش_بندی=partition
حذف_پیشوند=removeprefix حذف_پسوند=removesuffix پیدا_از_راست=rfind جایگاه_از_راست=rindex
بخش_بندی_از_راست=rpartition تقسیم_از_راست=rsplit جابجایی_حروف=swapcase ترجمه_متن=translate
از_کلیدها=fromkeys آخرین_مورد_را_بردار=popitem
به_روزرسانی_تفاضل=difference_update به_روزرسانی_اشتراک=intersection_update
جدا_از_هم_است=isdisjoint ابرمجموعه_است=issuperset تفاضل_متقارن=symmetric_difference
به_روزرسانی_تفاضل_متقارن=symmetric_difference_update
نسبت_صحیح=as_integer_ratio تعداد_بیت=bit_count طول_بیت=bit_length مزدوج=conjugate
مخرج=denominator از_بایت=from_bytes خیالی=imag صورت=numerator حقیقی=real
به_بایت=to_bytes صحیح_است=is_integer از_شانزده=fromhex شانزده_ای=hex
""", "attrs2"))

MODULES.update(_pairs("""
وب=dari_web هوش_مصنوعی=dari_ai
ریاضیات=math عدد_مختلط=cmath اعشار=decimal کسر=fractions
بایگانی_زیپ=zipfile بایگانی_تار=tarfile فشرده_سازی_گزیپ=gzip فشرده_سازی=zlib
ورودی_خروجی=io رمزنگاری=secrets رمز_هش=hmac کدگذاری_پایه=base64 دودویی_ساخت=struct
شیء_ذخیره=pickle قفسه=shelve پایگاه_داده_ساده=dbm
وب_سرور=http ای_میل=email اس_ام_تی_پی=smtplib
آدرس_ها=urllib فایل_های_سی_اس_وی=csv جیسون_ساده=json پارس_اکس_ام_ال=xml
اچ_تی_ام_ال=html ابزار_سوکت=socket ورودی_خروجی_ناهمگام=asyncio
انتخاب_کننده=selectors سیگنال=signal فرایندها=multiprocessing همزمانی=concurrent
صف=queue ابزار_زمان=sched تقویم=calendar منطقه_زمانی=zoneinfo
زبان_محلی=locale ترجمه_زبانی=gettext آرگومان_ها=argparse گزینه_ها=getopt
پیکربندی=configparser پارس_توکن=tokenize ابزار_کد=code آنالیز_نحو=ast
بررسی=inspect واحدآزمون=unittest آزمون_مستند=doctest اشکال_زدا=pdb
زمان_سنجی=timeit نمایه_سازی=cProfile پشته=traceback هشدارها=warnings
بازیافت_حافظه=gc بخش_داده=dataclasses شمارشی=enum انتزاعی=abc
زمینه=contextlib ابزار_عملگر=operator ابزار_توابع_بالا=functools
قطعه_بندی=textwrap مقایسه_متن=difflib ابزار_متن=string
یونیکد=unicodedata الگو_نام_فایل=fnmatch جستجوی_مسیر=glob
فایل_و_پوشه=shutil وضعیت_فایل=stat مقایسه_فایل=filecmp
پلتفرم_سیستم=platform ابزار_سیستم=sysconfig 
رنگ=colorsys تصویر_ساده=turtle 
صدا=wave صفحه_کلید=curses رابط_ساده=tkinter
دو_بخشی=bisect هیپ=heapq آرایه=array وزن_داده=weakref
نمونه_تصادفی=random آمار_ساده=statistics ماژول_وارد_کن=importlib
بسته_ها=pkgutil راه_انداز=runpy سیستم_فایل_مجازی=zipimport
""", "modules2"))

_USER_VOCAB_LOADED = set()


def load_user_vocab(directory):
    """واژگان شخصی: فایل «واژگان.json» در پوشهٔ برنامه (اختیاری)."""
    try:
        p = os.path.join(directory, "واژگان.json")
        if p in _USER_VOCAB_LOADED or not os.path.isfile(p):
            return
        _USER_VOCAB_LOADED.add(p)
        with open(p, encoding="utf-8-sig") as f:
            data = json.load(f)
        tables = {"keywords": KEYWORDS, "builtins": BUILTINS, "attrs": ATTRS,
                  "modules": MODULES, "kwargs": KWARGS, "dunders": DUNDERS}
        for k, tab in tables.items():
            if isinstance(data.get(k), dict):
                tab.update({str(a): str(b) for a, b in data[k].items()})
    except Exception:
        pass


# ════════════════════════════════════════════════════════════════════
#  ۲. مترجم: دری ← پایتون ۳
# ════════════════════════════════════════════════════════════════════

NAME, OP, NEWLINE = tokenize.NAME, tokenize.OP, tokenize.NEWLINE
INDENT, DEDENT, ENDMARKER, STRING = (tokenize.INDENT, tokenize.DEDENT,
                                     tokenize.ENDMARKER, tokenize.STRING)
_OPEN = ("(", "[", "{")
_CLOSE = (")", "]", "}")
_ASSIGN_OPS = {"=", "+=", "-=", "*=", "/=", "//=", "%=", "**=", ">>=", "<<=",
               "&=", "|=", "^=", "@=", ":="}
_EN_KW = set(keyword.kwlist)

_MAP = {}
for _i, _c in enumerate("۰۱۲۳۴۵۶۷۸۹"):
    _MAP[ord(_c)] = str(_i)
for _i, _c in enumerate("٠١٢٣٤٥٦٧٨٩"):
    _MAP[ord(_c)] = str(_i)
_MAP.update({
    ord("،"): ",", ord("؛"): ";", ord("٫"): ".", 0x200C: "_", 0x200F: "",
    0x200E: "", ord("ي"): "ی", ord("ك"): "ک", ord("ى"): "ی", ord("ـ"): "",
    0x00A0: " ", 0xFEFF: "",
})
_QMAP = {"“": '"', "”": '"', "‘": "'", "’": "'"}


def _syntax_error(msg, row=1, col=0, text=None):
    e = SyntaxError(msg)
    e.lineno, e.offset, e.text = row, col, text
    return e


def _normalize(src):
    """یکسان‌سازی نویسه‌ها بیرون از رشته‌ها و توضیحات:
    رقم‌های فارسی، ویرگول فارسی، نیم‌فاصله، «ي/ك» عربی، گیومهٔ هوشمند و «...»."""
    src = src.replace("\r\n", "\n").replace("\r", "\n")
    out = []
    i, n = 0, len(src)
    while i < n:
        c = src[i]
        if c == "#":
            j = src.find("\n", i)
            j = n if j < 0 else j
            out.append(src[i:j])
            i = j
            continue
        if c in "\"'“”‘’":
            smart = c in _QMAP
            q = _QMAP.get(c, c)
            triple = (not smart) and src[i:i + 3] == c * 3
            delim = q * 3 if triple else q
            out.append(delim)
            i += 3 if triple else 1
            while i < n:
                ch = src[i]
                if ch == "\\":
                    out.append(src[i:i + 2])
                    i += 2
                    continue
                if triple:
                    if src.startswith(delim, i):
                        out.append(delim)
                        i += 3
                        break
                else:
                    if ch == q or (smart and _QMAP.get(ch) == q):
                        out.append(q)
                        i += 1
                        break
                    if ch == "\n":
                        break
                out.append(ch)
                i += 1
            continue
        if c == "«":
            j = src.find("»", i + 1)
            k = src.find("\n", i + 1)
            if j > 0 and (k < 0 or j < k):
                body = src[i + 1:j].replace("\\", "\\\\").replace('"', '\\"')
                out.append('"' + body + '"')
                i = j + 1
                continue
        out.append(_MAP.get(ord(c), c) if ord(c) in _MAP else c)
        i += 1
    return "".join(out)


class _Tk(object):
    __slots__ = ("type", "s", "a", "b", "row")

    def __init__(self, type_, s, a, b, row):
        self.type, self.s, self.a, self.b, self.row = type_, s, a, b, row


def _lex(src):
    starts = [0]
    for line in src.split("\n")[:-1]:
        starts.append(starts[-1] + len(line) + 1)
    toks = []
    try:
        for tk in tokenize.generate_tokens(io.StringIO(src).readline):
            if tk.type in (tokenize.COMMENT, tokenize.NL):
                continue
            (r, c), (r2, c2) = tk.start, tk.end
            toks.append(_Tk(tk.type, tk.string, starts[r - 1] + c, starts[r2 - 1] + c2, r))
    except tokenize.TokenError as e:
        row = 1
        try:
            row = e.args[1][0]
        except Exception:
            pass
        raise _syntax_error(str(e.args[0]), row)
    return toks


def _kw(t):
    return KEYWORDS.get(t.s, t.s) if t.type == NAME else None


def _merge(toks, src):
    """عبارت‌های چندکلمه‌ای مثل «وگرنه اگر» و «تا وقتی» و «وارد کن» را یکی می‌کند."""
    out, i, n = [], 0, len(toks)
    while i < n:
        t = toks[i]
        done = False
        if t.type == NAME:
            for L in (3, 2):
                if i + L <= n:
                    seq = toks[i:i + L]
                    if (all(x.type == NAME and x.row == t.row for x in seq) and
                            all(not src[seq[k].b:seq[k + 1].a].strip() for k in range(L - 1))):
                        key = "_".join(x.s for x in seq)
                        if key in KEYWORDS:
                            out.append(_Tk(NAME, key, seq[0].a, seq[-1].b, t.row))
                            i += L
                            done = True
                            break
        if not done:
            out.append(t)
            i += 1
    return out


def _isop(t, *ss):
    return t is not None and t.type == OP and t.s in ss


def _collect(toks):
    """نام‌هایی که خود برنامه‌نویس تعریف کرده (تا با واژه‌های آمادهٔ زبان قاطی نشود)."""
    user, dattr = set(), set()
    n = len(toks)
    depth = 0
    chunk = []
    for i, t in enumerate(toks):
        prev = toks[i - 1] if i else None
        nxt = toks[i + 1] if i + 1 < n else None
        if t.type == OP:
            if t.s in _OPEN:
                depth += 1
            elif t.s in _CLOSE:
                depth = max(0, depth - 1)
            elif depth == 0 and t.s in (";", ":"):
                chunk = []
            elif depth == 0 and t.s in _ASSIGN_OPS:
                user.update(chunk)
                chunk = []
            continue
        if t.type in (NEWLINE, INDENT, DEDENT):
            chunk = []
            continue
        if t.type != NAME:
            continue
        k = _kw(t)
        if prev is not None and prev.type == NAME and _kw(prev) in ("def", "class"):
            user.add(t.s)
            dattr.add(t.s)
        if _isop(prev, "."):
            if nxt is not None and nxt.type == OP and nxt.s in _ASSIGN_OPS:
                dattr.add(t.s)
            continue
        if k == "def":
            j = i + 1
            while j < n and not _isop(toks[j], "(") and toks[j].type != NEWLINE:
                j += 1
            d = 0
            while j < n:
                tj = toks[j]
                if tj.type == OP:
                    if tj.s in _OPEN:
                        d += 1
                    elif tj.s in _CLOSE:
                        d -= 1
                        if d == 0:
                            break
                elif tj.type == NAME and d == 1 and _isop(toks[j - 1], "(", ",", "*", "**"):
                    user.add(tj.s)
                j += 1
        elif k == "lambda":
            j, d = i + 1, 0
            while j < n and toks[j].type != NEWLINE:
                tj = toks[j]
                if tj.type == OP:
                    if tj.s in _OPEN:
                        d += 1
                    elif tj.s in _CLOSE:
                        d -= 1
                    elif tj.s == ":" and d == 0:
                        break
                elif tj.type == NAME and d == 0 and (
                        _kw(toks[j - 1]) == "lambda" or _isop(toks[j - 1], ",", "*", "**")):
                    user.add(tj.s)
                j += 1
        elif k == "for":
            j, d = i + 1, 0
            while j < n and toks[j].type != NEWLINE:
                tj = toks[j]
                if tj.type == OP:
                    if tj.s in _OPEN:
                        d += 1
                    elif tj.s in _CLOSE:
                        d -= 1
                elif tj.type == NAME:
                    if _kw(tj) == "in" and d == 0:
                        break
                    if not _isop(toks[j - 1], "."):
                        user.add(tj.s)
                j += 1
        elif k == "as":
            if nxt is not None and nxt.type == NAME:
                user.add(nxt.s)
        elif (depth == 0 and t.s not in KEYWORDS and k not in _EN_KW and
              not (nxt is not None and nxt.type == OP and nxt.s in ("(", "[", "."))):
            chunk.append(t.s)
    return user, dattr


def _line_ends_colon(toks, i):
    n = len(toks)
    j = i
    while j < n and toks[j].type not in (NEWLINE, ENDMARKER):
        j += 1
    if not (j > i and toks[j - 1].type == OP and toks[j - 1].s == ":"):
        return False
    nxt = toks[i + 1] if i + 1 < n else None
    return not (nxt is not None and nxt.type == OP and nxt.s in ("=", ".", ",", ")", ":", "("))


def _import(toks, i, edits):
    """ترجمهٔ دستورهای «وارد کن» و «از ... وارد کن»؛ نام فارسی ماژول به‌عنوان نام مستعار می‌ماند."""
    n = len(toks)
    e = i + 1
    while e < n and toks[e].type not in (NEWLINE, ENDMARKER) and not _isop(toks[e], ";"):
        e += 1
    for t in toks[i:e]:
        if t.type == NAME and t.s in KEYWORDS:
            edits.append((t.a, t.b, KEYWORDS[t.s]))
    if _kw(toks[i]) == "import":
        k = i + 1
        while k < e:
            comps = []
            while k < e and toks[k].type == NAME and _kw(toks[k]) != "as":
                comps.append(toks[k])
                k += 1
                if k < e and _isop(toks[k], "."):
                    k += 1
                else:
                    break
            alias = False
            if k < e and _kw(toks[k]) == "as":
                alias = True
                k += 2
            if comps:
                first = comps[0]
                eng = MODULES.get(first.s)
                if eng:
                    edits.append((first.a, first.b, eng))
                for c in comps[1:]:
                    if c.s in ATTRS:
                        edits.append((c.a, c.b, ATTRS[c.s]))
                if eng and not alias:
                    if len(comps) == 1:
                        edits.append((comps[0].b, comps[0].b, " as " + first.s))
                    else:
                        edits.append((comps[-1].b, comps[-1].b, ", %s as %s" % (eng, first.s)))
            if k < e and _isop(toks[k], ","):
                k += 1
            elif not comps:
                k += 1
    else:  # from
        m = i + 1
        while m < e and _kw(toks[m]) != "import":
            m += 1
        comps = [t for t in toks[i + 1:m] if t.type == NAME]
        if comps and toks[i + 1].type == NAME:
            eng = MODULES.get(comps[0].s)
            if eng:
                edits.append((comps[0].a, comps[0].b, eng))
            for c in comps[1:]:
                if c.s in ATTRS:
                    edits.append((c.a, c.b, ATTRS[c.s]))
        k = m + 1
        while k < e:
            t = toks[k]
            if t.type == NAME and _kw(t) != "as" and t.s not in KEYWORDS:
                has_alias = k + 1 < e and _kw(toks[k + 1]) == "as"
                eng = ATTRS.get(t.s) or MODULES.get(t.s)
                if eng:
                    edits.append((t.a, t.b, eng))
                    if not has_alias:
                        edits.append((t.b, t.b, " as " + t.s))
                k += 3 if has_alias else 1
            else:
                k += 1
    return e


def _tr_expr(head, names):
    if not head.strip():
        return head
    try:
        res = _translate(_normalize("(" + head + ")"), names)
        return res.rstrip("\n")[1:-1]
    except SyntaxError:
        return head


def _fbody(s, names):
    out, i, n = [], 0, len(s)
    while i < n:
        c = s[i]
        if c == "\\" and s[i + 1:i + 3] == "N{":
            j = s.find("}", i)
            j = n - 1 if j < 0 else j
            out.append(s[i:j + 1])
            i = j + 1
            continue
        if c == "{":
            if s[i + 1:i + 2] == "{":
                out.append("{{")
                i += 2
                continue
            j, depth, quote = i + 1, 0, None
            while j < n:
                ch = s[j]
                if quote:
                    if ch == quote:
                        quote = None
                elif ch in "\"'":
                    quote = ch
                elif ch in "([{":
                    depth += 1
                elif ch in ")]":
                    depth -= 1
                elif ch == "}":
                    if depth == 0:
                        break
                    depth -= 1
                elif depth == 0 and ch == "!" and s[j + 1:j + 2] != "=":
                    break
                elif depth == 0 and ch == ":":
                    break
                j += 1
            expr = s[i + 1:j]
            mm = re.match(r"^(.*?)(\s*=\s*)$", expr, re.S)
            if mm and not re.search(r"[=!<>]$", mm.group(1)):
                head, tail = mm.group(1), mm.group(2)
            else:
                head, tail = expr, ""
            out.append("{" + _tr_expr(head, names) + tail)
            k, d = j, 0
            while k < n:
                if s[k] == "{":
                    d += 1
                elif s[k] == "}":
                    if d == 0:
                        break
                    d -= 1
                k += 1
            spec = s[j:k]
            out.append(_fbody(spec, names) if "{" in spec else spec)
            out.append("}")
            i = k + 1
            continue
        if c == "}" and s[i + 1:i + 2] == "}":
            out.append("}}")
            i += 2
            continue
        out.append(c)
        i += 1
    return "".join(out)


def _fstr(s, names):
    m = re.match(r"""([A-Za-z]*)(\"\"\"|'''|"|')""", s)
    if not m or "f" not in m.group(1).lower():
        return s
    q = m.group(2)
    if len(s) < m.end() + len(q) or not s.endswith(q):
        return s
    try:
        return s[:m.end()] + _fbody(s[m.end():len(s) - len(q)], names) + q
    except Exception:
        return s


def _translate(src, names=None):
    if not src.endswith("\n"):
        src += "\n"
    toks = _merge(_lex(src), src)
    if names is None:
        names = _collect(toks)
    user, dattr = names
    edits = []
    n, i, depth, at_start = len(toks), 0, 0, True
    while i < n:
        t = toks[i]
        ty = t.type
        if ty in (NEWLINE, INDENT, DEDENT):
            at_start = True
            i += 1
            continue
        if ty == ENDMARKER:
            break
        if ty == OP:
            if t.s in _OPEN:
                depth += 1
            elif t.s in _CLOSE:
                depth = max(0, depth - 1)
            elif t.s == ";" and depth == 0:
                at_start = True
                i += 1
                continue
            at_start = False
            i += 1
            continue
        if ty == STRING:
            ns = _fstr(t.s, names)
            if ns != t.s:
                edits.append((t.a, t.b, ns))
            at_start = False
            i += 1
            continue
        if ty == NAME:
            if at_start and _kw(t) in ("import", "from"):
                i = _import(toks, i, edits)
                at_start = False
                continue
            prev = toks[i - 1] if i > 0 else None
            nxt = toks[i + 1] if i + 1 < n else None
            s = t.s
            repl = None
            if _isop(prev, "."):
                if s in DUNDERS:
                    repl = DUNDERS[s]
                elif s in ATTRS and s not in dattr:
                    repl = ATTRS[s]
            elif s in KEYWORDS:
                repl = KEYWORDS[s]
            elif s in SOFT and at_start and _line_ends_colon(toks, i):
                repl = SOFT[s]
            elif s in DUNDERS:
                repl = DUNDERS[s]
            elif (depth > 0 and s in KWARGS and s not in user and _isop(prev, "(", ",") and
                  _isop(nxt, "=")):
                repl = KWARGS[s]
            elif s in BUILTINS and s not in user:
                repl = BUILTINS[s]
            if repl is not None:
                edits.append((t.a, t.b, repl))
        at_start = False
        i += 1
    for a, b, txt in sorted(edits, key=lambda e: (e[0], e[1]), reverse=True):
        src = src[:a] + txt + src[b:]
    return src


def transpile(src):
    """متن برنامهٔ دری را به متن پایتون ۳ تبدیل می‌کند (شمارهٔ خط‌ها حفظ می‌شود)."""
    if src.startswith("﻿"):
        src = src[1:]
    return _translate(_normalize(src))


# ════════════════════════════════════════════════════════════════════
#  ۳. خطاها به زبان دری، اجرا، وارد کردن فایل‌های dpy
# ════════════════════════════════════════════════════════════════════

ERR_FA = {en: fa for fa, en in BUILTINS.items() if en[:1].isupper()}

_MSG = [
    (r"name '(.+)' is not defined", r"نام «\1» تعریف نشده است"),
    (r"division by zero", "تقسیم بر صفر ممکن نیست"),
    (r"integer division or modulo by zero", "تقسیم بر صفر ممکن نیست"),
    (r"invalid literal for int\(\) with base 10: (.+)", r"عدد صحیح معتبر نیست: \1"),
    (r"could not convert string to float: (.+)", r"عدد اعشاری معتبر نیست: \1"),
    (r"(.+) index out of range", r"اندیس \1 خارج از محدوده است"),
    (r"'(.+)' object has no attribute '(.+)'", r"شیء از نوع «\1» ویژگی «\2» ندارد"),
    (r"module '(.+)' has no attribute '(.+)'", r"ماژول «\1» چیزی به نام «\2» ندارد"),
    (r"\[Errno 2\] No such file or directory: (.+)", r"فایل یا پوشه پیدا نشد: \1"),
    (r"\[Errno 13\] Permission denied: (.+)", r"اجازهٔ دسترسی وجود ندارد: \1"),
    (r"No module named '(.+)'", r"ماژول «\1» پیدا نشد (از بخش «کتابخانه» نصبش کنید)"),
    (r"can only concatenate str \(not \"(.+)\"\) to str", r"نمی‌توان متن را با «\1» جمع کرد"),
    (r"unsupported operand type\(s\) for (.+): '(.+)' and '(.+)'",
     r"عملگر \1 برای «\2» و «\3» ممکن نیست"),
    (r"'(.+)' object is not callable", r"شیء از نوع «\1» قابل فراخوانی نیست"),
    (r"'(.+)' object is not subscriptable", r"شیء از نوع «\1» اندیس‌پذیر نیست"),
    (r"'(.+)' object is not iterable", r"شیء از نوع «\1» تکرارپذیر نیست"),
    (r"'(.+)' object does not support item assignment", r"شیء از نوع «\1» تغییرپذیر نیست"),
    (r"(.+)\(\) takes (.+) positional arguments? but (.+) w(?:as|ere) given",
     r"تابع \1 به \2 ورودی نیاز دارد ولی \3 ورودی داده شد"),
    (r"(.+)\(\) missing (\d+) required positional arguments?: (.+)",
     r"تابع \1 به \2 ورودی لازم دیگر نیاز دارد: \3"),
    (r"invalid syntax\. Perhaps you forgot a comma\?", "نحو نادرست؛ شاید ویرگول جا افتاده"),
    (r"invalid syntax", "نحو نادرست"),
    (r"unterminated string literal.*", "رشته (متن بین نقل‌قول) بسته نشده است"),
    (r"EOF in multi-line string", "رشتهٔ چندخطی بسته نشده است"),
    (r"EOF in multi-line statement", "دستور ناتمام مانده (پرانتز یا کروشه بسته نشده)"),
    (r"expected ':'", "علامت «:» لازم است"),
    (r"unexpected indent", "تورفتگی نابجا"),
    (r"unindent does not match any outer indentation level", "تورفتگی با سطح‌های بالاتر نمی‌خواند"),
    (r"expected an indented block.*", "بعد از این خط باید تورفتگی (۴ فاصله) بیاید"),
    (r"'(.)' was never closed", r"«\1» باز شد ولی بسته نشد"),
    (r"unmatched '(.)'", r"«\1» اضافی است"),
    (r"cannot assign to (.+)", r"به \1 نمی‌توان مقدار داد"),
    (r"'return' outside function", "«برگردان» فقط درون تابع کار می‌کند"),
    (r"'break' outside loop", "«بشکن» فقط درون حلقه کار می‌کند"),
    (r"'continue' not properly in loop", "«ادامه» فقط درون حلقه کار می‌کند"),
    (r"maximum recursion depth exceeded.*", "عمق بازگشت از حد مجاز گذشت"),
    (r"Connection refused", "اتصال رد شد (سرور روشن نیست؟)"),
    (r"\[Errno 98\] Address already in use", "این درگاه (پورت) قبلاً در حال استفاده است"),
]


def _fa_msg(etype, value):
    msg = getattr(value, "msg", None) if isinstance(value, SyntaxError) else None
    if msg is None:
        msg = str(value)
    if etype is KeyError and value.args:
        return "کلید %r پیدا نشد" % (value.args[0],)
    for pat, rep in _MSG:
        if re.fullmatch(pat, msg, re.S):
            return re.sub(pat, rep, msg, flags=re.S)
    return msg


def _fa_error_line(etype, value):
    name = ERR_FA.get(etype.__name__, etype.__name__)
    if issubclass(etype, SyntaxError) and not issubclass(etype, IndentationError):
        name = "خطای_نحو"
    elif issubclass(etype, IndentationError):
        name = "خطای_تورفتگی"
    msg = _fa_msg(etype, value)
    return "%s: %s" % (name, msg) if msg else name


def _short(fn):
    return fn if fn.startswith("<") else os.path.basename(fn)


def format_traceback(etype, value, tb):
    me = os.path.abspath(__file__)
    lines = ["ردیابی خطا (آخرین مورد در پایین):"]
    for fr in traceback.extract_tb(tb):
        try:
            if os.path.abspath(fr.filename) == me:
                continue
        except Exception:
            pass
        name = "<برنامه>" if fr.name == "<module>" else fr.name
        lines.append("  فایل «%s»، خط %s، در %s" % (_short(fr.filename), fr.lineno, name))
        if fr.line:
            lines.append("      " + fr.line.strip())
    lines.append(_fa_error_line(etype, value))
    return "\n".join(lines) + "\n"


def format_syntax_error(e, filename, lines):
    ln = getattr(e, "lineno", None) or 1
    text = ""
    if lines and 0 < ln <= len(lines):
        text = lines[ln - 1].strip()
    out = ["خطای نحوی — فایل «%s»، خط %s" % (_short(filename), ln)]
    if text:
        out.append("      " + text)
    kind = "تورفتگی" if isinstance(e, IndentationError) else "نحو"
    out.append("خطای_%s: %s" % (kind, _fa_msg(type(e), e)))
    return "\n".join(out) + "\n"


# ════════════════════════════════════════════════════════════════════
#  کتابخانه‌های همراه: «وب» و «هوش_مصنوعی» (با نام فارسی)
# ════════════════════════════════════════════════════════════════════
_LIBS = {
    "dari_web": r'''# کتابخانهٔ «وب» پایتون دری: ساخت برنامهٔ وب با چند خط (فقط با کتابخانهٔ استاندارد)
import html as _html
import json as _json
import socket as _socket
import urllib.parse as _up
from http.server import BaseHTTPRequestHandler as _Base, ThreadingHTTPServer as _Server

_CSS = """
*{box-sizing:border-box}body{margin:0;font-family:Tahoma,"Vazirmatn",sans-serif;background:#f3f6fb;color:#172033}
header{background:#164e9b;color:#fff;padding:16px;font-size:20px;font-weight:bold}
main{max-width:720px;margin:0 auto;padding:16px}
input,textarea,select{width:100%;padding:12px;margin:6px 0 12px;border:1px solid #c8d1df;border-radius:10px;font:inherit}
button,.دکمه{display:inline-block;padding:12px 18px;border:0;border-radius:10px;background:#087b59;color:#fff;font:inherit;text-decoration:none;cursor:pointer}
.کارت{background:#fff;border-radius:14px;padding:16px;margin:12px 0;box-shadow:0 4px 18px #14295010}
"""


def متن_امن(متن):
    # جلوگیری از اجرای کد HTML ورودی کاربر
    return _html.escape(str(متن))


def صفحه_html(عنوان, بدنه):
    return ('<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>%s</title><style>%s</style></head><body><header>%s</header><main>%s</main></body></html>'
            % (متن_امن(عنوان), _CSS, متن_امن(عنوان), بدنه))


class درخواست:
    def __init__(خود, روش, مسیر, پرسش, فرم, سرآیندها):
        خود.روش = روش
        خود.آدرس_صفحه = مسیر
        خود.پرسش = پرسش
        خود.فرم = فرم
        خود.سرآیندها = سرآیندها

    def پارامتر(خود, نام, پیش_فرض=""):
        if نام in خود.فرم:
            return خود.فرم[نام]
        return خود.پرسش.get(نام, پیش_فرض)


class برنامه:
    def __init__(خود, نام="برنامهٔ دری"):
        خود.نام = نام
        خود.مسیرها = {}

    def صفحه(خود, مسیر, روش_ها=("GET", "POST")):
        def تزئین(تابع):
            خود.مسیرها[مسیر] = (تابع, tuple(روش_ها))
            return تابع
        return تزئین

    def _پاسخ(خود, نتیجه):
        if isinstance(نتیجه, tuple):
            کد, نتیجه = نتیجه
        else:
            کد = 200
        if isinstance(نتیجه, (dict, list)):
            return کد, "application/json; charset=utf-8", _json.dumps(نتیجه, ensure_ascii=False).encode("utf-8")
        متن = "" if نتیجه is None else str(نتیجه)
        if "<html" not in متن[:200].lower():
            متن = صفحه_html(خود.نام, متن)
        return کد, "text/html; charset=utf-8", متن.encode("utf-8")

    def راه_اندازی(خود, درگاه=8000, میزبان="127.0.0.1"):
        برنامه_ = خود

        class _مدیر(_Base):
            def log_message(خود2, *a):
                pass

            def _انجام(خود2, روش):
                آدرس = _up.urlparse(خود2.path)
                مسیر_ = _up.unquote(آدرس.path)
                پرسش = {k: v[0] for k, v in _up.parse_qs(آدرس.query).items()}
                فرم = {}
                if روش == "POST":
                    طول = int(خود2.headers.get("Content-Length", "0") or 0)
                    خام = خود2.rfile.read(طول).decode("utf-8", "replace")
                    if "json" in خود2.headers.get("Content-Type", ""):
                        try:
                            فرم = _json.loads(خام or "{}")
                        except ValueError:
                            فرم = {}
                    else:
                        فرم = {k: v[0] for k, v in _up.parse_qs(خام).items()}
                مورد = برنامه_.مسیرها.get(مسیر_)
                if not مورد or روش not in مورد[1]:
                    کد, نوع, بدنه = برنامه_._پاسخ((404, "<div class='کارت'>صفحه پیدا نشد</div>"))
                else:
                    try:
                        کد, نوع, بدنه = برنامه_._پاسخ(مورد[0](درخواست(روش, مسیر_, پرسش, فرم, dict(خود2.headers))))
                    except Exception as خطا:
                        کد, نوع, بدنه = برنامه_._پاسخ((500, "<div class='کارت'>خطا: %s</div>" % متن_امن(خطا)))
                خود2.send_response(کد)
                خود2.send_header("Content-Type", نوع)
                خود2.send_header("Content-Length", str(len(بدنه)))
                خود2.end_headers()
                خود2.wfile.write(بدنه)

            def do_GET(خود2):
                خود2._انجام("GET")

            def do_POST(خود2):
                خود2._انجام("POST")

        سرور = None
        for د in (درگاه, درگاه + 1, درگاه + 2, 0):
            try:
                سرور = _Server((میزبان, د), _مدیر)
                break
            except OSError:
                continue
        if سرور is None:
            raise OSError("هیچ درگاهی آزاد نبود")
        print("🌐 برنامهٔ وب «%s» آماده است: http://127.0.0.1:%d" % (خود.نام, سرور.server_address[1]), flush=True)
        try:
            سرور.serve_forever()
        except KeyboardInterrupt:
            pass
''',
    "dari_ai": r'''# کتابخانهٔ «هوش_مصنوعی» پایتون دری: گفتگو با مدل‌های هوش مصنوعی از راه اینترنت
# کلید (API key) خودتان را لازم دارید؛ در برنامه ننویسید و از متغیر محیطی یا ورودی بگیرید.
import json as _json
import os as _os
import urllib.request as _rq
import urllib.error as _er


class خطای_هوش_مصنوعی(Exception):
    pass


def _ارسال(آدرس, سرآیندها, داده, مهلت=90):
    درخواست = _rq.Request(آدرس, data=_json.dumps(داده).encode("utf-8"),
                          headers=dict(سرآیندها, **{"Content-Type": "application/json"}), method="POST")
    try:
        with _rq.urlopen(درخواست, timeout=مهلت) as پاسخ:
            return _json.loads(پاسخ.read().decode("utf-8"))
    except _er.HTTPError as e:
        try:
            جزئیات = e.read().decode("utf-8", "replace")[:300]
        except Exception:
            جزئیات = ""
        if e.code in (401, 403):
            raise خطای_هوش_مصنوعی("کلید نادرست است یا اجازه ندارد (کد %d)" % e.code)
        raise خطای_هوش_مصنوعی("خطای سرویس (کد %d): %s" % (e.code, جزئیات))
    except Exception as e:
        raise خطای_هوش_مصنوعی("ارتباط با اینترنت برقرار نشد: %s" % e)


class دستیار:
    """گفتگوی چندمرحله‌ای که تاریخچه را نگه می‌دارد.

    ارائه_دهنده: "anthropic" یا "openai" (هر سرویس سازگار با openai هم با آدرس= کار می‌کند)
    """

    def __init__(خود, کلید_دسترسی=None, ارائه_دهنده="anthropic", مدل=None, سیستم=None, آدرس=None, حداکثر_واژه=1024):
        خود.ارائه_دهنده = ارائه_دهنده
        خود.سیستم = سیستم
        خود.حداکثر_واژه = حداکثر_واژه
        خود.تاریخچه = []
        if ارائه_دهنده == "anthropic":
            خود.کلید = کلید_دسترسی or _os.environ.get("ANTHROPIC_API_KEY", "")
            خود.مدل = مدل or "claude-sonnet-5-5"
            خود.آدرس = آدرس or "https://api.anthropic.com/v1/messages"
        else:
            خود.کلید = کلید_دسترسی or _os.environ.get("OPENAI_API_KEY", "")
            خود.مدل = مدل or "gpt-4o-mini"
            خود.آدرس = آدرس or "https://api.openai.com/v1/chat/completions"
        if not خود.کلید:
            raise خطای_هوش_مصنوعی("کلید داده نشده است (کلید_دسترسی=... یا متغیر محیطی ANTHROPIC_API_KEY / OPENAI_API_KEY)")

    def بپرس(خود, متن):
        خود.تاریخچه.append({"role": "user", "content": متن})
        try:
            if خود.ارائه_دهنده == "anthropic":
                بدنه = {"model": خود.مدل, "max_tokens": خود.حداکثر_واژه, "messages": خود.تاریخچه}
                if خود.سیستم:
                    بدنه["system"] = خود.سیستم
                پاسخ = _ارسال(خود.آدرس, {"x-api-key": خود.کلید, "anthropic-version": "2023-06-01"}, بدنه)
                جواب = "".join(ب.get("text", "") for ب in پاسخ.get("content", []) if ب.get("type") == "text")
            else:
                پیام‌ها = ([{"role": "system", "content": خود.سیستم}] if خود.سیستم else []) + خود.تاریخچه
                پاسخ = _ارسال(خود.آدرس, {"Authorization": "Bearer " + خود.کلید},
                              {"model": خود.مدل, "messages": پیام‌ها, "max_tokens": خود.حداکثر_واژه})
                جواب = پاسخ["choices"][0]["message"]["content"]
        except Exception:
            خود.تاریخچه.pop()
            raise
        خود.تاریخچه.append({"role": "assistant", "content": جواب})
        return جواب

    def پاک_کن(خود):
        خود.تاریخچه = []


def بپرس(متن, کلید_دسترسی=None, **گزینه‌ها):
    # یک پرسش تکی بدون تاریخچه
    return دستیار(کلید_دسترسی=کلید_دسترسی, **گزینه‌ها).بپرس(متن)
''',
}


class _LibFinder(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    def find_spec(self, name, path=None, target=None):
        if name in _LIBS:
            return importlib.machinery.ModuleSpec(name, self)
        return None

    def create_module(self, spec):
        return None

    def exec_module(self, module):
        exec(compile(_LIBS[module.__name__], "<%s>" % module.__name__, "exec"), module.__dict__)


def _install_libs():
    if not any(isinstance(f, _LibFinder) for f in sys.meta_path):
        sys.meta_path.insert(0, _LibFinder())


def run_source(src, filename="<دری>", argv=None):
    """اجرای متن برنامهٔ دری. کد خروج را برمی‌گرداند."""
    _install_libs()
    lines = src.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    try:
        py = transpile(src)
        co = compile(py, filename, "exec", dont_inherit=True)
    except SyntaxError as e:
        sys.stderr.write(format_syntax_error(e, filename, lines))
        sys.stderr.flush()
        return 1
    linecache.cache[filename] = (len(src), None, [l + "\n" for l in lines], filename)
    mod = types.ModuleType("__main__")
    mod.__file__ = filename
    sys.modules["__main__"] = mod
    sys.argv = [filename] + list(argv or [])
    try:
        exec(co, mod.__dict__)
        return 0
    except SystemExit as e:
        c = e.code
        if c is None:
            return 0
        if isinstance(c, int):
            return c
        sys.stderr.write(str(c) + "\n")
        return 1
    except KeyboardInterrupt:
        sys.stderr.write("\nاجرا با وقفهٔ کاربر متوقف شد.\n")
        return 130
    except BaseException:
        et, ev, tb = sys.exc_info()
        sys.stderr.write(format_traceback(et, ev, tb))
        sys.stderr.flush()
        return 1


class _DariLoader(importlib.machinery.SourceFileLoader):
    def source_to_code(self, data, path, *, _optimize=-1):
        src = data.decode("utf-8-sig") if isinstance(data, (bytes, bytearray)) else data
        return compile(transpile(src), path, "exec", dont_inherit=True, optimize=_optimize)


class _DariFinder(importlib.abc.MetaPathFinder):
    """اجازه می‌دهد فایل‌های «.dpy» مثل ماژول‌های معمولی وارد شوند."""

    def find_spec(self, fullname, path, target=None):
        name = fullname.rpartition(".")[2]
        for d in (path if path is not None else sys.path):
            if not isinstance(d, str):
                continue
            f = os.path.join(d or ".", name + ".dpy")
            if os.path.isfile(f):
                return importlib.util.spec_from_file_location(
                    fullname, f, loader=_DariLoader(fullname, f))
        return None


def install_import_hook():
    if not any(isinstance(f, _DariFinder) for f in sys.meta_path):
        sys.meta_path.append(_DariFinder())


def run_file(path, argv=None):
    path = os.path.abspath(path)
    try:
        with open(path, encoding="utf-8-sig") as f:
            src = f.read()
    except OSError as e:
        sys.stderr.write("فایل «%s» باز نشد: %s\n" % (path, e))
        return 2
    d = os.path.dirname(path)
    try:
        os.chdir(d)
    except OSError:
        pass
    if d not in sys.path:
        sys.path.insert(0, d)
    load_user_vocab(d)
    install_import_hook()
    return run_source(src, path, argv)


class _DariConsole(_code.InteractiveConsole):
    def runsource(self, source, filename="<دری>", symbol="single"):
        try:
            py = transpile(source).rstrip("\n")
        except SyntaxError:
            return True if source.strip() and source.rstrip().endswith((",", "(", "[", "{", "\\")) else self._syntax(source)
        return super().runsource(py, filename, symbol)

    def _syntax(self, source):
        try:
            transpile(source)
        except SyntaxError as e:
            sys.stderr.write(format_syntax_error(e, "<دری>", source.split("\n")))
        return False

    def showtraceback(self):
        et, ev, tb = sys.exc_info()
        sys.stderr.write(format_traceback(et, ev, tb))

    def showsyntaxerror(self, filename=None, **kw):
        et, ev, tb = sys.exc_info()
        sys.stderr.write(format_syntax_error(ev, "<دری>", []))


def cmd_shell():
    install_import_hook()
    banner = "پایتون دری %s — پوستهٔ تعاملی. برای خروج: خروج()  یا Ctrl-D" % __version__
    _DariConsole(filename="<دری>").interact(banner=banner, exitmsg="خدانگهدار!")
    return 0


# ════════════════════════════════════════════════════════════════════
#  ۴. نمونه برنامه‌ها
# ════════════════════════════════════════════════════════════════════

EXAMPLES = {}

EXAMPLES["سلام.dpy"] = r'''# پایتون دری — اولین برنامه
نام = ورودی("نام شما چیست؟ ")
چاپ("سلام،", نام, "! به پایتون دری خوش آمدید.")

برای شماره در دامنه(1, 4):
    چاپ("شمارهٔ", شماره)
'''

EXAMPLES["شرط_و_حلقه.dpy"] = r'''عدد = 7
اگر عدد % 2 == 0:
    چاپ(عدد, "زوج است")
وگرنه:
    چاپ(عدد, "فرد است")

مجموع = 0
برای i در دامنه(1, 11):
    مجموع += i
چاپ("مجموع ۱ تا ۱۰:", مجموع)

میوه_ها = ["سیب", "انار", "انگور"]
میوه_ها.افزودن("توت")
برای میوه در مرتب(میوه_ها):
    چاپ("-", میوه)
چاپ("تعداد میوه‌ها:", طول(میوه_ها))
'''

EXAMPLES["کلاس.dpy"] = r'''کلاس حساب:
    تابع __آغاز__(خود, صاحب, موجودی=0):
        خود.صاحب = صاحب
        خود.موجودی = موجودی

    تابع واریز(خود, مبلغ):
        اگر مبلغ <= 0:
            بیانداز خطای_مقدار("مبلغ باید مثبت باشد")
        خود.موجودی += مبلغ

    تابع __متن__(خود):
        برگردان f"{خود.صاحب}: {خود.موجودی} افغانی"


الف = حساب("احمد", 1000)
الف.واریز(500)
چاپ(الف)

بیازما:
    الف.واریز(-5)
بجز خطای_مقدار به_عنوان خطا:
    چاپ("خطا:", خطا)
'''

EXAMPLES["ماشین_حساب.dpy"] = r'''تابع محاسبه(الف, عملگر, ب):
    اگر عملگر == "+":
        برگردان الف + ب
    وگرنه_اگر عملگر == "-":
        برگردان الف - ب
    وگرنه_اگر عملگر == "*":
        برگردان الف * ب
    وگرنه_اگر عملگر == "/":
        اگر ب == 0:
            برگردان "تقسیم بر صفر ممکن نیست"
        برگردان الف / ب
    وگرنه:
        برگردان "عملگر نامعتبر"


چاپ("ماشین حساب — مثال: 3 + 4   (برای پایان بنویسید: خروج)")
تا_وقتی درست:
    ورودی_متن = ورودی("> ")
    اگر ورودی_متن == "خروج":
        بشکن
    اجزا = ورودی_متن.تقسیم()
    اگر طول(اجزا) != 3:
        چاپ("شکل درست: عدد عملگر عدد")
        ادامه
    بیازما:
        چاپ("نتیجه:", محاسبه(اعشاری(اجزا[0]), اجزا[1], اعشاری(اجزا[2])))
    بجز خطای_مقدار:
        چاپ("لطفاً عدد معتبر وارد کنید")
'''

EXAMPLES["چت_بات.dpy"] = r'''# یک چت‌بات ساده بر پایهٔ واژهٔ کلیدی
پاسخ_ها = {
    "سلام": "سلام! چطور می‌توانم کمکتان کنم؟",
    "اسم": "من یک چت‌بات ساده هستم که با پایتون دری نوشته شده‌ام.",
    "حال": "خوبم، ممنون که پرسیدید!",
    "ساعت": "برای دیدن ساعت از ماژول «زمان» استفاده کنید 😊",
    "خداحافظ": "به امید دیدار!",
}


تابع جواب_بده(پیام):
    برای کلیدواژه, جواب در پاسخ_ها.موردها():
        اگر کلیدواژه در پیام:
            برگردان جواب
    برگردان "متوجه نشدم؛ می‌توانید دوباره بگویید؟"


چاپ("چت‌بات آماده است. برای پایان بنویسید: خداحافظ")
تا_وقتی درست:
    پیام = ورودی("شما: ").حذف_فاصله()
    پاسخ = جواب_بده(پیام)
    چاپ("بات:", پاسخ)
    اگر "خداحافظ" در پیام:
        بشکن
'''

EXAMPLES["هوش_مصنوعی.dpy"] = r'''# یک نورون مصنوعی (پرسپترون) که تابع «یا» را یاد می‌گیرد — بدون هیچ کتابخانه‌ای
# برای شبکه‌های بزرگ‌تر کتابخانه‌هایی مثل numpy و torch را نصب کنید؛
# آن‌ها با همین نام‌های اصلی در دری هم کار می‌کنند.
داده = [((0, 0), 0), ((0, 1), 1), ((1, 0), 1), ((1, 1), 1)]
وزن = [0.0, 0.0]
بایاس = 0.0
نرخ = 0.1


تابع پیش_بینی(ورودی_ها):
    مجموع_وزنی = وزن[0] * ورودی_ها[0] + وزن[1] * ورودی_ها[1] + بایاس
    برگردان 1 اگر مجموع_وزنی > 0 وگرنه 0


برای دوره در دامنه(20):
    برای (x1, x2), هدف در داده:
        خطا = هدف - پیش_بینی((x1, x2))
        وزن[0] += نرخ * خطا * x1
        وزن[1] += نرخ * خطا * x2
        بایاس += نرخ * خطا

چاپ("وزن‌های یادگرفته‌شده:", وزن, " بایاس:", بایاس)
برای (x1, x2), هدف در داده:
    چاپ(x1, "یا", x2, "=", پیش_بینی((x1, x2)))
'''

EXAMPLES["پیام_رسان_سرور.dpy"] = r'''# سرور پیام‌رسان ساده (ابتدا این را اجرا کنید، بعد «پیام_رسان_مشتری»)
وارد_کن سوکت
از نخ_ها وارد_کن نخ

میزبان = "0.0.0.0"
درگاه = 5000
مشتری_ها = []


تابع پخش(پیام, فرستنده):
    برای م در مشتری_ها:
        اگر م != فرستنده:
            بیازما:
                م.بفرست(پیام)
            بجز استثنا:
                بگذر


تابع مدیریت(اتصال, نشانی):
    چاپ("متصل شد:", نشانی)
    مشتری_ها.افزودن(اتصال)
    بیازما:
        تا_وقتی درست:
            داده = اتصال.دریافت(1024)
            اگر نه داده:
                بشکن
            چاپ(نشانی, ":", داده.کدگشایی("utf-8"))
            پخش(داده, اتصال)
    سرانجام:
        مشتری_ها.برداشتن(اتصال)
        اتصال.بستن()
        چاپ("قطع شد:", نشانی)


سرور = سوکت.سوکت(سوکت.AF_INET, سوکت.SOCK_STREAM)
سرور.setsockopt(سوکت.SOL_SOCKET, سوکت.SO_REUSEADDR, 1)
سرور.اتصال_به_پورت((میزبان, درگاه))
سرور.گوش_بده()
چاپ("سرور روی درگاه", درگاه, "منتظر است...")
تا_وقتی درست:
    اتصال, نشانی = سرور.بپذیر()
    نخ(هدف=مدیریت, آرگومان_ها=(اتصال, نشانی), پس_زمینه=درست).شروع_کن()
'''

EXAMPLES["پیام_رسان_مشتری.dpy"] = r'''# مشتری پیام‌رسان (بعد از روشن شدن سرور اجرا کنید)
وارد_کن سوکت
از نخ_ها وارد_کن نخ

نام = ورودی("نام شما: ")
اتصال = سوکت.سوکت(سوکت.AF_INET, سوکت.SOCK_STREAM)
اتصال.وصل_شو(("127.0.0.1", 5000))
چاپ("وصل شدید. برای پایان بنویسید: خروج")


تابع دریافت_پیام_ها():
    تا_وقتی درست:
        داده = اتصال.دریافت(1024)
        اگر نه داده:
            چاپ("ارتباط قطع شد.")
            بشکن
        چاپ(داده.کدگشایی("utf-8"))


نخ(هدف=دریافت_پیام_ها, پس_زمینه=درست).شروع_کن()
تا_وقتی درست:
    متن_پیام = ورودی("")
    اگر متن_پیام == "خروج":
        بشکن
    اتصال.بفرست((نام + ": " + متن_پیام).کدگذاری_کردن("utf-8"))
اتصال.بستن()
'''

EXAMPLES["سخت_افزار.dpy"] = r'''# ارتباط با آردوینو / ESP / رزبری‌پای از راه پورت سریال
# کتابخانه‌ها نام اصلی خودشان را دارند (serial.Serial و ...)؛ فقط دستورهای زبان دری است.
# نصب: از منوی «کتابخانه» بنویسید  pyserial
وارد_کن سیستم

بیازما:
    وارد_کن serial
بجز خطای_وارد_کردن:
    چاپ("ابتدا کتابخانهٔ pyserial را از بخش «کتابخانه» نصب کنید.")
    سیستم.خروج()

درگاه = "COM3"   # در لینوکس/اندروید مثلاً /dev/ttyUSB0
بیازما:
    ارتباط = serial.Serial(درگاه, 9600, timeout=2)
    ارتباط.write(b"LED_ON\n")
    چاپ("پاسخ:", ارتباط.readline().decode().strip())
    ارتباط.close()
بجز استثنا به_عنوان خطا:
    چاپ("اتصال برقرار نشد:", خطا)
'''

EXAMPLES["فایل_و_جیسون.dpy"] = r'''وارد_کن جیسون
وارد_کن سیستم_عامل

داده = {"نام": "احمد", "شهر": "کابل", "امتیاز": [10, 20, 30]}

با بازکن("داده.json", "w", کدگذاری="utf-8") به_عنوان ف:
    جیسون.ذخیره_جیسون(داده, ف, فقط_اسکی=نادرست, تورفتگی=2)

با بازکن("داده.json", encoding="utf-8") به_عنوان ف:
    خوانده = جیسون.بارگذاری(ف)

چاپ("خوانده شد:", خوانده)
چاپ("فایل وجود دارد؟", سیستم_عامل.مسیر.وجود_دارد("داده.json"))
'''

EXAMPLES["وب_ساده.dpy"] = r'''# یک سرور وب کوچک؛ کتابخانهٔ http.server با همان نام اصلی
از http.server وارد_کن HTTPServer, BaseHTTPRequestHandler


کلاس مدیر(BaseHTTPRequestHandler):
    تابع do_GET(خود):
        خود.send_response(200)
        خود.send_header("Content-Type", "text/html; charset=utf-8")
        خود.end_headers()
        خود.wfile.write("<h1 dir='rtl'>سلام از پایتون دری</h1>".encode("utf-8"))


چاپ("آدرس: http://127.0.0.1:8000  (برای توقف دکمهٔ «توقف» را بزنید)")
HTTPServer(("127.0.0.1", 8000), مدیر).serve_forever()
'''


# ════════════════════════════════════════════════════════════════════
#  ۵. محیط برنامه‌نویسی (سرور محلی + رابط وب راست‌به‌چپ)
# ════════════════════════════════════════════════════════════════════

def _load_token():
    """توکن یک‌بار ساخته و در ‎~/.dari_token‎ ذخیره می‌شود تا نشانی همیشه یکی بماند."""
    p = os.path.join(os.path.expanduser("~"), ".dari_token")
    try:
        with open(p, encoding="utf-8") as f:
            t = f.read().strip()
        if len(t) >= 16:
            return t
    except OSError:
        pass
    t = secrets.token_urlsafe(18)
    try:
        with open(p, "w", encoding="utf-8") as f:
            f.write(t)
        os.chmod(p, 0o600)
    except OSError:
        pass
    return t


TOKEN = _load_token()
STATE = {"root": None}
JOBS = {}
JOBS_LOCK = threading.Lock()
MAX_OUT = 4_000_000


class _ApiError(Exception):
    pass


class _Job(object):
    """اجرای یک برنامه در فرایند جداگانه (خروجی زنده + ورودی)."""

    def __init__(self, cmd, cwd):
        self.id = secrets.token_hex(6)
        self.buf = ""
        self.done = False
        self.code = None
        self.lock = threading.Lock()
        env = dict(os.environ)
        env["PYTHONIOENCODING"] = "utf-8"
        env["PYTHONUNBUFFERED"] = "1"
        self.proc = subprocess.Popen(
            cmd, cwd=cwd, env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, bufsize=0)
        threading.Thread(target=self._read, daemon=True).start()

    def _append(self, text):
        with self.lock:
            if len(self.buf) < MAX_OUT:
                self.buf += text

    def _read(self):
        dec = codecs.getincrementaldecoder("utf-8")("replace")
        try:
            while True:
                chunk = self.proc.stdout.read(4096)
                if not chunk:
                    break
                self._append(dec.decode(chunk))
            self._append(dec.decode(b"", final=True))
        except Exception:
            pass
        self.code = self.proc.wait()
        self.done = True

    def read(self, pos):
        with self.lock:
            return self.buf[pos:], len(self.buf)

    def write(self, text):
        try:
            self.proc.stdin.write((text + "\n").encode("utf-8"))
        except Exception:
            pass

    def stop(self):
        try:
            self.proc.terminate()
            threading.Timer(2.0, self._kill).start()
        except Exception:
            pass

    def _kill(self):
        try:
            if self.proc.poll() is None:
                self.proc.kill()
        except Exception:
            pass


class _ThreadJob(object):
    """جایگزین برای دستگاه‌هایی که ساخت فرایند جدید را اجازه نمی‌دهند (اجرا در همین فرایند)."""

    def __init__(self, path):
        import queue
        self.id = secrets.token_hex(6)
        self.buf = ""
        self.done = False
        self.code = None
        self.lock = threading.Lock()
        self.q = queue.Queue()
        self.tid = None
        threading.Thread(target=self._main, args=(path,), daemon=True).start()

    def _append(self, text):
        with self.lock:
            if len(self.buf) < MAX_OUT:
                self.buf += text

    def _main(self, path):
        self.tid = threading.get_ident()
        job = self

        class W(object):
            encoding = "utf-8"

            def write(self_, t):
                job._append(t)
                return len(t)

            def flush(self_):
                pass

            def isatty(self_):
                return False

        def fake_input(prompt=""):
            job._append(str(prompt))
            line = job.q.get()
            if line is None:
                raise KeyboardInterrupt
            return line

        old = (sys.stdout, sys.stderr, builtins.input)
        sys.stdout = sys.stderr = W()
        builtins.input = fake_input
        try:
            self.code = run_file(path)
        except BaseException:
            self.code = 1
        finally:
            sys.stdout, sys.stderr, builtins.input = old
            self.done = True

    def read(self, pos):
        with self.lock:
            return self.buf[pos:], len(self.buf)

    def write(self, text):
        self.q.put(text)

    def stop(self):
        self.q.put(None)
        try:
            import ctypes
            ctypes.pythonapi.PyThreadState_SetAsyncExc(
                ctypes.c_ulong(self.tid), ctypes.py_object(KeyboardInterrupt))
        except Exception:
            pass


def _register(job):
    with JOBS_LOCK:
        for k in [k for k, j in JOBS.items() if j.done][:-10]:
            JOBS.pop(k, None)
        JOBS[job.id] = job
    return job.id


def _root():
    return os.path.abspath(STATE["root"])


def _safe(rel):
    root = _root()
    p = os.path.abspath(os.path.join(root, rel))
    if p != root and not p.startswith(root + os.sep):
        raise _ApiError("مسیر خارج از پوشهٔ کار مجاز نیست")
    return p


def _rel(p):
    return os.path.relpath(p, _root()).replace(os.sep, "/")


def _unique(p):
    if not os.path.exists(p):
        return p
    base, ext = os.path.splitext(p)
    i = 2
    while os.path.exists("%s_%d%s" % (base, i, ext)):
        i += 1
    return "%s_%d%s" % (base, i, ext)


def _first(q, k, d=""):
    return q.get(k, [d])[0]


# ---- مسیرهای API ----

def api_files(q):
    root = _root()
    items = []

    def walk(d, rel, depth):
        try:
            names = sorted(os.listdir(d), key=lambda s: (not os.path.isdir(os.path.join(d, s)), s))
        except OSError:
            return
        for nm in names:
            if nm.startswith(".") or nm == "__pycache__":
                continue
            full = os.path.join(d, nm)
            r = (rel + "/" + nm) if rel else nm
            isd = os.path.isdir(full)
            items.append({"path": r, "dir": isd, "depth": depth})
            if isd and depth < 4 and len(items) < 1500:
                walk(full, r, depth + 1)

    walk(root, "", 0)
    return {"root": root, "items": items}


def api_file(q):
    p = _safe(_first(q, "path"))
    if not os.path.isfile(p):
        raise _ApiError("فایل پیدا نشد")
    if os.path.getsize(p) > 5_000_000:
        raise _ApiError("فایل بیش از حد بزرگ است")
    with open(p, encoding="utf-8-sig", errors="replace", newline="") as f:
        return {"content": f.read().replace("\r\n", "\n")}


def api_save(d):
    p = _safe(d["path"])
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(d.get("content", ""))
    return {"ok": True}


def api_new(d):
    rel = d["path"].strip().strip("/")
    if not rel:
        raise _ApiError("نام خالی است")
    kind = d.get("kind", "file")
    if kind == "file" and "." not in os.path.basename(rel):
        rel += ".dpy"
    p = _safe(rel)
    if kind == "dir":
        os.makedirs(p, exist_ok=True)
        return {"path": _rel(p)}
    if os.path.exists(p) and not d.get("unique"):
        raise _ApiError("این فایل از قبل وجود دارد")
    p = _unique(p)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(d.get("content", ""))
    return {"path": _rel(p)}


def api_delete(d):
    p = _safe(d["path"])
    if p == _root():
        raise _ApiError("پوشهٔ اصلی حذف نمی‌شود")
    if os.path.isdir(p):
        shutil.rmtree(p)
    elif os.path.exists(p):
        os.remove(p)
    return {"ok": True}


def api_rename(d):
    a, b = _safe(d["path"]), _safe(d["to"])
    if os.path.exists(b):
        raise _ApiError("نام تازه از قبل وجود دارد")
    os.makedirs(os.path.dirname(b), exist_ok=True)
    os.rename(a, b)
    return {"path": _rel(b)}


def _start(cmd, cwd):
    return _register(_Job(cmd, cwd))


def api_run(d):
    p = _safe(d["path"])
    if not os.path.isfile(p):
        raise _ApiError("فایل پیدا نشد")
    cmd = [sys.executable, "-X", "utf8", "-u", os.path.abspath(__file__), "run", p]
    try:
        return {"id": _start(cmd, os.path.dirname(p))}
    except (OSError, ValueError):
        return {"id": _register(_ThreadJob(p))}


_PKG_RX = r"[A-Za-z0-9_.\-\[\]=<>!~,]+"


class _PipJob(object):
    """اجرای pip داخل همین برنامه (برای گوشی‌هایی که `python -m pip` در آن‌ها کار نمی‌کند)."""

    def __init__(self, args):
        self.id = secrets.token_hex(6)
        self.buf = ""
        self.done = False
        self.code = None
        self.lock = threading.Lock()
        self.q = None
        threading.Thread(target=self._main, args=(args,), daemon=True).start()

    def read(self, pos):
        with self.lock:
            return self.buf[pos:], len(self.buf)

    def write(self, t):
        with self.lock:
            if len(self.buf) < MAX_OUT:
                self.buf += t
        return len(t)

    def flush(self):
        pass

    def isatty(self):
        return False

    def stop(self):
        pass

    def send(self, line):
        pass

    def _main(self, args):
        old = sys.stdout, sys.stderr
        sys.stdout = sys.stderr = self
        try:
            try:
                from pip._internal.cli.main import main as pipmain
            except Exception as e:
                print("pip در این پایتون وجود ندارد: %s" % e)
                self.code = 1
                return
            try:
                self.code = int(pipmain(args) or 0)
            except SystemExit as e:
                self.code = e.code if isinstance(e.code, int) else 1
            except BaseException as e:
                print("خطا:", e)
                self.code = 1
        finally:
            sys.stdout, sys.stderr = old
            self.done = True


def _pip_subprocess_ok():
    import subprocess
    try:
        r = subprocess.run([sys.executable, "-m", "pip", "--version"], capture_output=True,
                           text=True, timeout=60)
        return r.returncode == 0
    except Exception:
        return False


def api_pip(d):
    names = d.get("name", "").split()
    if not names or any(n.startswith("-") or not re.fullmatch(_PKG_RX, n) for n in names):
        raise _ApiError("نام کتابخانه معتبر نیست (مثال: requests)")
    act = d.get("action", "install")
    if act == "uninstall":
        args = ["uninstall", "-y", "--disable-pip-version-check"] + names
    elif act == "upgrade":
        args = ["install", "--upgrade", "--disable-pip-version-check"] + names
    else:
        args = ["install", "--disable-pip-version-check"] + names
    if _pip_subprocess_ok():
        try:
            return {"id": _start([sys.executable, "-m", "pip"] + args, _root())}
        except (OSError, ValueError):
            pass
    return {"id": _register(_PipJob(args))}


def api_piplist(q):
    import subprocess
    try:
        r = subprocess.run([sys.executable, "-m", "pip", "list", "--format=json",
                            "--disable-pip-version-check"], capture_output=True, text=True, timeout=60)
        items = json.loads(r.stdout or "[]")
        if items:
            return {"items": items}
    except Exception:
        pass
    try:
        from importlib import metadata
        seen = {}
        for dist in metadata.distributions():
            n = dist.metadata["Name"]
            if n:
                seen[n] = dist.version
        return {"items": [{"name": k, "version": v} for k, v in sorted(seen.items(), key=lambda x: x[0].lower())]}
    except Exception as e:
        raise _ApiError("فهرست کتابخانه‌ها خوانده نشد: %s" % e)


def api_pypi(q):
    """جستجوی یک کتابخانه در PyPI (نیازمند اینترنتِ همین دستگاه)."""
    import urllib.request
    name = _first(q, "name").strip()
    if not re.fullmatch(r"[A-Za-z0-9_.\-]+", name):
        raise _ApiError("نام کتابخانه را با حروف انگلیسی بنویسید (مثال: requests)")
    try:
        with urllib.request.urlopen("https://pypi.org/pypi/%s/json" % name, timeout=10) as r:
            info = json.loads(r.read().decode("utf-8"))["info"]
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {"found": False}
        raise _ApiError("خطا در ارتباط با PyPI: %s" % e)
    except Exception as e:
        raise _ApiError("اینترنت در دسترس نیست یا PyPI پاسخ نداد: %s" % e)
    return {"found": True, "name": info.get("name"), "version": info.get("version"),
            "summary": info.get("summary") or "", "home": info.get("home_page") or ""}


def _job(i):
    j = JOBS.get(i)
    if not j:
        raise _ApiError("اجرای مورد نظر پیدا نشد")
    return j


def api_out(q):
    j = _job(_first(q, "id"))
    pos = int(_first(q, "pos", "0") or 0)
    done = j.done
    text, n = j.read(pos)
    return {"text": text, "pos": n, "done": bool(done and not j.read(n)[0]), "code": j.code}


def api_stdin(d):
    _job(d["id"]).write(d.get("text", ""))
    return {"ok": True}


def api_stop(d):
    _job(d["id"]).stop()
    return {"ok": True}


def api_translate(d):
    try:
        return {"py": transpile(d.get("code", ""))}
    except SyntaxError as e:
        raise _ApiError(format_syntax_error(e, "<دری>", d.get("code", "").split("\n")))


# ════════════════════════════════════════════════════════════════════
#  عیب‌یاب: پیدا کردن اشتباه‌ها پیش از اجرا
# ════════════════════════════════════════════════════════════════════

_BR_OPEN = {"(": ")", "[": "]", "{": "}"}
_BR_NAME = {"(": "پرانتز", ")": "پرانتز", "[": "کروشه", "]": "کروشه", "{": "آکولاد", "}": "آکولاد"}


def _scan_brackets(src):
    """پرانتز، کروشه، آکولاد و نقل‌قول‌های باز یا بسته‌نشده را با شمارهٔ خط پیدا می‌کند."""
    issues, stack = [], []
    i, n, line, ls = 0, len(src), 1, 0
    while i < n:
        c = src[i]
        if c == "\n":
            line += 1
            ls = i + 1
            i += 1
        elif c == "#":
            while i < n and src[i] != "\n":
                i += 1
        elif c in "\"'":
            col = i - ls + 1
            if src[i:i + 3] == c * 3:
                j = src.find(c * 3, i + 3)
                if j < 0:
                    issues.append({"line": line, "col": col, "sev": "error",
                                   "msg": "رشتهٔ سه‌نقل‌قولی (%s) که اینجا باز شده هرگز بسته نشده است" % (c * 3)})
                    return issues
                line += src.count("\n", i, j)
                ls = src.rfind("\n", 0, j) + 1
                i = j + 3
            else:
                j = i + 1
                while j < n and src[j] != c and src[j] != "\n":
                    j += 2 if src[j] == "\\" else 1
                if j >= n or src[j] != c:
                    issues.append({"line": line, "col": col, "sev": "error",
                                   "msg": "نقل‌قول (%s) در این خط باز شده ولی بسته نشده است" % c})
                    i = j
                else:
                    i = j + 1
        elif c == "«":
            j = i + 1
            while j < n and src[j] not in "»\n":
                j += 1
            if j >= n or src[j] != "»":
                issues.append({"line": line, "col": i - ls + 1, "sev": "error",
                               "msg": "«» باز شده ولی علامت بستنِ » جا افتاده است"})
            i = j + 1
        elif c in _BR_OPEN:
            stack.append((c, line, i - ls + 1))
            i += 1
        elif c in ")]}":
            if not stack:
                issues.append({"line": line, "col": i - ls + 1, "sev": "error",
                               "msg": "%s بسته «%s» اضافی است؛ %s بازی برایش نیست" % (_BR_NAME[c], c, _BR_NAME[c])})
            else:
                o, ol, oc = stack.pop()
                if _BR_OPEN[o] != c:
                    issues.append({"line": line, "col": i - ls + 1, "sev": "error",
                                   "msg": "«%s» آمده ولی %s «%s» که در خط %d باز شده بود با «%s» بسته می‌شود"
                                          % (c, _BR_NAME[o], o, ol, _BR_OPEN[o])})
            i += 1
        else:
            i += 1
    for o, ol, oc in stack:
        issues.append({"line": ol, "col": oc, "sev": "error",
                       "msg": "%s باز «%s» در این خط هرگز بسته نشده است؛ «%s» لازم است" % (_BR_NAME[o], o, _BR_OPEN[o])})
    return issues


def _undefined_names(tree):
    import ast
    import difflib
    defined = set(dir(builtins)) | {"__file__", "__name__", "__doc__", "__spec__"}
    loads = []
    star = False
    for nd in ast.walk(tree):
        if isinstance(nd, ast.Name):
            if isinstance(nd.ctx, ast.Load):
                loads.append(nd)
            else:
                defined.add(nd.id)
        elif isinstance(nd, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            defined.add(nd.name)
        elif isinstance(nd, ast.arg):
            defined.add(nd.arg)
        elif isinstance(nd, ast.ExceptHandler) and nd.name:
            defined.add(nd.name)
        elif isinstance(nd, (ast.Import, ast.ImportFrom)):
            for a in nd.names:
                if a.name == "*":
                    star = True
                defined.add((a.asname or a.name).split(".")[0])
        elif isinstance(nd, (ast.Global, ast.Nonlocal)):
            defined.update(nd.names)
        elif isinstance(nd, ast.MatchAs) and nd.name:
            defined.add(nd.name)
    if star:
        return []
    out, seen = [], set()
    cands = list(defined) + list(BUILTINS)
    for nd in loads:
        if nd.id in defined or nd.id in seen:
            continue
        seen.add(nd.id)
        m = difflib.get_close_matches(nd.id, cands, n=1, cutoff=0.72)
        hint = "؛ منظورتان «%s» بود؟" % m[0] if m else "؛ نامش را درست نوشته‌اید یا قبلش تعریف کرده‌اید؟"
        out.append({"line": nd.lineno, "col": nd.col_offset + 1, "sev": "warn",
                    "msg": "نام «%s» تعریف نشده است%s" % (nd.id, hint)})
    return out


def diagnose(src):
    """فهرست اشتباه‌های برنامه: [{line, col, sev: error|warn, msg}]"""
    issues = _scan_brackets(src)
    if issues:
        return issues
    try:
        py = transpile(src)
        tree = compile(py, "<دری>", "exec", flags=__import__("ast").PyCF_ONLY_AST)
    except SyntaxError as e:
        msg = _fa_msg(type(e), e)
        if "does not match opening" in str(e.msg):
            msg = "پرانتز/کروشه/آکولاد با نوع بازِ خودش بسته نشده است"
        return [{"line": getattr(e, "lineno", None) or 1, "col": getattr(e, "offset", None) or 1,
                 "sev": "error", "msg": msg}]
    except Exception as e:
        return [{"line": 1, "col": 1, "sev": "error", "msg": "%s: %s" % (type(e).__name__, e)}]
    try:
        return _undefined_names(tree)
    except Exception:
        return []


def api_check(d):
    return {"issues": diagnose(d.get("code", ""))[:30]}



def api_vocab(q):
    return {"keywords": KEYWORDS, "soft": SOFT, "builtins": BUILTINS, "kwargs": KWARGS,
            "attrs": ATTRS, "modules": MODULES, "dunders": DUNDERS,
            "pykw": sorted(_EN_KW)}


EXAMPLES["برنامه_وب.dpy"] = r'''# یک دفترچهٔ یادداشت وب با چند خط — دکمهٔ ▶ را بزنید
# صفحهٔ برنامه همان‌جا باز می‌شود. برای نصب روی صفحهٔ گوشی، «نصب برنامه» را در منوی مرورگر بزنید.
وارد_کن وب

برنامه = وب.برنامه("دفترچهٔ یادداشت")
یادداشت_ها = []


@برنامه.صفحه("/")
تابع خانه(د):
    اگر د.روش == "POST" و د.پارامتر("متن"):
        یادداشت_ها.افزودن(د.پارامتر("متن"))
    ردیف‌ها = ""
    برای مورد در یادداشت_ها:
        ردیف‌ها += "<div class='کارت'>" + وب.متن_امن(مورد) + "</div>"
    فرم = ("<form method='post'><input name='متن' placeholder='یادداشت تازه…' autofocus>"
           "<button>ذخیره</button></form>")
    برگردان فرم + ردیف‌ها


@برنامه.صفحه("/داده")
تابع داده(د):
    برگردان {"تعداد": طول(یادداشت_ها), "یادداشت_ها": یادداشت_ها}


برنامه.راه_اندازی(8000)
'''

EXAMPLES["چت_بات_هوش_مصنوعی.dpy"] = r'''# چت‌بات هوش مصنوعی — به اینترنت و «کلید دسترسی» (API key) خودتان نیاز دارد
# کلید را جای دیگر منتشر نکنید. برای مدل‌های سازگار با OpenAI: ارائه_دهنده="openai"
وارد_کن هوش_مصنوعی به_عنوان هوش

کلید = ورودی("کلید دسترسی (API key): ").حذف_فاصله()
بیازما:
    دستیار = هوش.دستیار(کلید_دسترسی=کلید, سیستم="تو دستیاری مهربان هستی و به فارسی پاسخ می‌دهی.")
بجز هوش.خطای_هوش_مصنوعی بنام خ:
    چاپ("⚠", خ)
    خروج()

چاپ("گفتگو شروع شد. برای پایان بنویسید: خروج")
تا_وقتی درست:
    پرسش = ورودی("شما: ").حذف_فاصله()
    اگر پرسش == "خروج":
        بشکن
    اگر نه پرسش:
        ادامه
    بیازما:
        چاپ("🤖", دستیار.بپرس(پرسش))
    بجز هوش.خطای_هوش_مصنوعی بنام خ:
        چاپ("⚠", خ)
'''


def api_examples(q):
    return EXAMPLES


def api_workspace(d):
    p = os.path.abspath(os.path.expanduser(d.get("path", "").strip()))
    os.makedirs(p, exist_ok=True)
    STATE["root"] = p
    return {"root": p}


GET_ROUTES = {"/api/files": api_files, "/api/file": api_file, "/api/out": api_out,
              "/api/vocab": api_vocab, "/api/examples": api_examples,
              "/api/pypi": api_pypi, "/api/piplist": api_piplist}
POST_ROUTES = {"/api/file": api_save, "/api/new": api_new, "/api/delete": api_delete,
               "/api/rename": api_rename, "/api/run": api_run, "/api/pip": api_pip,
               "/api/stdin": api_stdin, "/api/check": api_check, "/api/stop": api_stop,
               "/api/translate": api_translate, "/api/workspace": api_workspace}


# ════════════════════════════════════════════════════════════════════
#  نصب به‌عنوان برنامه (PWA): آیکون و پنجرهٔ مستقل برای محیط و برای هر برنامه
# ════════════════════════════════════════════════════════════════════

_ICON_CACHE = {}


def _png_bytes(size, rgb):
    """آیکون ساده: پس‌زمینهٔ تک‌رنگ و مثلث سفید «اجرا» (بدون نیاز به کتابخانهٔ تصویر)."""
    key = (size, rgb)
    if key in _ICON_CACHE:
        return _ICON_CACHE[key]
    import struct
    import zlib
    ax, ay, bx, by, cx, cy = 0.38, 0.28, 0.38, 0.72, 0.74, 0.50

    def inside(px, py):
        d1 = (px - bx) * (ay - by) - (ax - bx) * (py - by)
        d2 = (px - cx) * (by - cy) - (bx - cx) * (py - cy)
        d3 = (px - ax) * (cy - ay) - (cx - ax) * (py - ay)
        neg = d1 < 0 or d2 < 0 or d3 < 0
        pos = d1 > 0 or d2 > 0 or d3 > 0
        return not (neg and pos)

    raw = bytearray()
    bg = bytes(rgb)
    for y in range(size):
        raw.append(0)
        py = (y + 0.5) / size
        for x in range(size):
            raw += b"\xff\xff\xff" if inside((x + 0.5) / size, py) else bg

    def chunk(t, d):
        c = struct.pack(">I", len(d)) + t + d
        return c + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)

    png = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0)) +
           chunk(b"IDAT", zlib.compress(bytes(raw), 6)) + chunk(b"IEND", b""))
    _ICON_CACHE[key] = png
    return png


def _icon_color(k):
    if not k or k == "ide":
        return (22, 78, 155)
    h = hashlib.sha256(k.encode("utf-8")).digest()
    pal = [(8, 123, 89), (156, 39, 176), (211, 84, 0), (192, 57, 43), (41, 128, 185), (22, 160, 133), (127, 140, 141)]
    return pal[h[0] % len(pal)]


def _manifest(q):
    app = _first(q, "app")
    if app:
        name = os.path.basename(app)
        for ext in (".dpy", ".dari", ".دری"):
            if name.endswith(ext):
                name = name[:-len(ext)]
        start = "/?t=%s&page=run&path=%s" % (TOKEN, urllib.parse.quote(app))
        key = app
    else:
        name, start, key = "پایتون دری", "/?t=%s" % TOKEN, "ide"
    ik = urllib.parse.quote(key)
    return {"name": name, "short_name": name[:12], "id": start, "start_url": start, "scope": "/",
            "display": "standalone", "lang": "fa", "dir": "rtl", "background_color": "#ffffff",
            "theme_color": "#164e9b",
            "icons": [{"src": "/icon.png?t=%s&s=%d&k=%s" % (TOKEN, n, ik), "sizes": "%dx%d" % (n, n),
                       "type": "image/png", "purpose": "any maskable"} for n in (192, 512)]}


_SW_JS = ("self.addEventListener('install',function(){self.skipWaiting();});\n"
          "self.addEventListener('activate',function(e){e.waitUntil(self.clients.claim());});\n"
          "self.addEventListener('fetch',function(){});\n")


class _Handler(http.server.BaseHTTPRequestHandler):
    server_version = "DariPython/" + __version__

    def log_message(self, *a):
        pass

    def _host_ok(self):
        return self.headers.get("Host", "").rsplit(":", 1)[0] in ("127.0.0.1", "localhost")

    def _auth(self):
        return hmac.compare_digest(self.headers.get("X-Token", ""), TOKEN)

    def _send(self, code, body, ctype="application/json; charset=utf-8"):
        if isinstance(body, (dict, list)):
            body = json.dumps(body, ensure_ascii=False)
        if isinstance(body, str):
            body = body.encode("utf-8")
        try:
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def _dispatch(self, fn, arg):
        try:
            self._send(200, fn(arg))
        except _ApiError as e:
            self._send(400, {"error": str(e)})
        except KeyError as e:
            self._send(400, {"error": "پارامتر ناقص: %s" % e})
        except Exception as e:
            self._send(500, {"error": "%s: %s" % (type(e).__name__, e)})

    def do_GET(self):
        if not self._host_ok():
            return self._send(403, "forbidden", "text/plain")
        u = urllib.parse.urlparse(self.path)
        q = urllib.parse.parse_qs(u.query)
        if u.path in ("/manifest.webmanifest", "/sw.js", "/icon.png"):
            if not hmac.compare_digest(_first(q, "t"), TOKEN):
                return self._send(403, "forbidden", "text/plain")
            if u.path == "/sw.js":
                return self._send(200, _SW_JS, "text/javascript; charset=utf-8")
            if u.path == "/icon.png":
                try:
                    n = max(48, min(512, int(_first(q, "s") or 192)))
                except ValueError:
                    n = 192
                return self._send(200, _png_bytes(n, _icon_color(_first(q, "k"))), "image/png")
            return self._send(200, _manifest(q), "application/manifest+json; charset=utf-8")
        if u.path == "/":
            if not hmac.compare_digest(_first(q, "t"), TOKEN):
                return self._send(403, "دسترسی غیرمجاز — از نشانی چاپ‌شده در برنامه وارد شوید.",
                                  "text/plain; charset=utf-8")
            appqs = ""
            if _first(q, "page") == "run" and _first(q, "path"):
                appqs = "&app=" + urllib.parse.quote(_first(q, "path"))
            page = HTML.replace("__APPQS__", appqs).replace("__ICONKEY__", urllib.parse.quote(_first(q, "path") or "ide")
                                                           if appqs else "ide")
            return self._send(200, page.replace("__TOKEN__", TOKEN), "text/html; charset=utf-8")
        if not self._auth():
            return self._send(403, {"error": "forbidden"})
        fn = GET_ROUTES.get(u.path)
        if not fn:
            return self._send(404, {"error": "یافت نشد"})
        self._dispatch(fn, q)

    def do_POST(self):
        if not self._host_ok() or not self._auth():
            return self._send(403, {"error": "forbidden"})
        fn = POST_ROUTES.get(urllib.parse.urlparse(self.path).path)
        if not fn:
            return self._send(404, {"error": "یافت نشد"})
        try:
            n = int(self.headers.get("Content-Length", "0"))
            data = json.loads(self.rfile.read(n).decode("utf-8") or "{}")
        except Exception:
            return self._send(400, {"error": "درخواست نامعتبر"})
        self._dispatch(fn, data)


def cmd_ide(args):
    folder, port, open_b = None, 0, True
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--no-browser":
            open_b = False
        elif a == "--port" and i + 1 < len(args):
            port = int(args[i + 1])
            i += 1
        else:
            folder = a
        i += 1
    if folder is None:
        folder = os.path.join(os.path.expanduser("~"), "DariPython")
    try:
        os.makedirs(folder, exist_ok=True)
    except OSError:
        folder = os.getcwd()
    STATE["root"] = os.path.abspath(folder)
    load_user_vocab(STATE["root"])
    if not any(not n.startswith(".") for n in os.listdir(STATE["root"])):
        with open(os.path.join(STATE["root"], "سلام.dpy"), "w", encoding="utf-8") as f:
            f.write(EXAMPLES["سلام.dpy"])
    srv = None
    for p in ([port] if port else [8765, 8766, 8767, 0]):
        try:
            srv = http.server.ThreadingHTTPServer(("127.0.0.1", p), _Handler)
            break
        except OSError:
            continue
    if srv is None:
        print("هیچ درگاهی آزاد نبود.")
        return 1
    url = "http://127.0.0.1:%d/?t=%s" % (srv.server_address[1], TOKEN)
    print("═" * 52)
    print(" پایتون دری %s — محیط برنامه‌نویسی" % __version__)
    print(" پوشهٔ کار:", STATE["root"])
    print(" اگر مرورگر خودکار باز نشد، این نشانی را در مرورگر باز کنید:")
    print(" ", url)
    print(" برای بستن: Ctrl+C")
    print("═" * 52)
    sys.stdout.flush()
    if open_b:
        threading.Timer(0.7, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


HTML = r'''<!doctype html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,viewport-fit=cover">
<title>پایتون دری</title>
<link rel="manifest" href="/manifest.webmanifest?t=__TOKEN____APPQS__">
<link rel="icon" type="image/png" href="/icon.png?t=__TOKEN__&s=192&k=__ICONKEY__">
<link rel="apple-touch-icon" href="/icon.png?t=__TOKEN__&s=192&k=__ICONKEY__">
<meta name="theme-color" content="#164e9b">
<meta name="mobile-web-app-capable" content="yes">
<style>
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
:root{--mono:"Vazirmatn Code","Noto Sans Mono","DejaVu Sans Mono",Consolas,Menlo,"Courier New","Tahoma",monospace;--fs:17px}
body{--bg:#4a4a40;--panel:#12263f;--panel2:#1b3454;--fg:#fffbe8;--mut:#a9b3c4;--acc:#ffd966;--accfg:#2b2400;--bd:#2a4468;
--kw:#7dd3fc;--bi:#fdba74;--st:#f5e27a;--cm:#9aa08c;--nm:#f9a8d4;--gut:#3d3d35}
body.t-dark{--bg:#0f172a;--panel:#111c33;--panel2:#16233f;--fg:#e5e9f0;--mut:#8da0bd;--acc:#38bdf8;--accfg:#04202e;--bd:#24365c;
--kw:#f472b6;--bi:#fbbf24;--st:#86efac;--cm:#6b7fa3;--nm:#fca5a5;--gut:#0c1426}
body.t-light{--bg:#f6f8fc;--panel:#ffffff;--panel2:#eef2f9;--fg:#1e293b;--mut:#64748b;--acc:#0369a1;--accfg:#fff;--bd:#d5deec;
--kw:#be185d;--bi:#b45309;--st:#15803d;--cm:#94a3b8;--nm:#b91c1c;--gut:#e6ebf4}
html,body{height:100%;margin:0}
body{height:100vh;height:100dvh}
body{background:var(--bg);color:var(--fg);font-family:"Vazirmatn","Noto Sans Arabic","Tahoma","Segoe UI",system-ui,sans-serif;
display:flex;flex-direction:column;overflow:hidden}
button{font:inherit;font-size:14px;background:var(--panel2);color:var(--fg);border:1px solid var(--bd);border-radius:10px;padding:8px 14px;cursor:pointer}
button:active{filter:brightness(1.25)}
button.pri{background:var(--acc);color:var(--accfg);border-color:var(--acc);font-weight:700}
button.dng{color:#fca5a5}
button:disabled{opacity:.4}
.top{display:flex;align-items:center;gap:4px;padding:6px 8px;background:var(--panel);direction:ltr;min-height:54px;flex:none}
.top .ic{background:transparent;border:0;font-size:22px;padding:8px 11px;color:var(--fg);line-height:1}
.top .ttl{flex:1;font-size:19px;font-weight:700;padding:0 10px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;unicode-bidi:plaintext;text-align:start}
.mut{color:var(--mut);font-size:13px}
#tabs{display:flex;overflow-x:auto;background:var(--panel);border-top:1px solid var(--bd);direction:ltr;flex:none;scrollbar-width:none}
#tabs::-webkit-scrollbar{display:none}
.tab{flex:none;padding:11px 16px;color:var(--mut);font-size:16px;white-space:nowrap;display:flex;gap:8px;align-items:center;border-bottom:3px solid transparent;cursor:pointer;unicode-bidi:plaintext}
.tab.on{color:var(--fg);border-bottom-color:var(--acc);font-weight:700}
.tab i{font-style:normal;opacity:.6;padding:0 2px}
.ed{position:relative;flex:1;display:flex;min-height:0;background:var(--bg)}
.ed.ltr{direction:ltr}.ed.rtl,.ed.auto{direction:rtl}
.gut{width:3.2em;flex:none;padding:12px 6px;text-align:center;color:var(--mut);background:var(--bg);border-inline-end:1px solid var(--bd);
font:var(--fs)/1.6 var(--mono);overflow:hidden;white-space:pre;direction:ltr;user-select:none}
.code{position:relative;flex:1;min-width:0}
.code pre,.code textarea{position:absolute;top:0;right:0;bottom:0;left:0;margin:0;padding:12px 14px 120px;border:0;
font:var(--fs)/1.6 var(--mono);tab-size:4;white-space:pre;overflow:auto;letter-spacing:0;word-spacing:0}
.code pre{pointer-events:none;overflow:hidden;color:var(--fg)}
.code textarea{background:transparent;color:transparent;-webkit-text-fill-color:transparent;caret-color:var(--acc);resize:none;outline:none}
.ed.rtl pre,.ed.rtl textarea{direction:rtl;text-align:right}
.ed.ltr pre,.ed.ltr textarea{direction:ltr;text-align:left}
.ed.auto pre,.ed.auto textarea{unicode-bidi:plaintext;text-align:start}
.k{color:var(--kw)}.b{color:var(--bi)}.s{color:var(--st)}.c{color:var(--cm);font-style:italic}.n{color:var(--nm)}
#empty{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;text-align:center;color:var(--mut);padding:30px;line-height:2}
#diag{display:none;flex:none;padding:9px 14px;font-size:14px;line-height:1.7;cursor:pointer;border-top:1px solid var(--bd)}
#diag.error{display:block;background:#7f1d1d;color:#fff}
#diag.warn{display:block;background:#854d0e;color:#fff}
.gut span{display:block}.gut .bad{background:#dc2626;color:#fff;border-radius:4px}.gut .wrn{background:#d97706;color:#fff;border-radius:4px}
.tab.plus{font-size:24px;padding:6px 18px;color:var(--acc);font-weight:700;position:sticky;left:0;background:var(--panel);z-index:2}
#bNew{margin-top:14px;font-size:18px;padding:12px 26px}
#keys{display:flex;overflow-x:auto;background:var(--panel);border-top:1px solid var(--bd);direction:ltr;flex:none;scrollbar-width:none;padding-bottom:env(safe-area-inset-bottom)}
#keys::-webkit-scrollbar{display:none}
#keys b{flex:none;min-width:48px;text-align:center;padding:13px 12px;font:600 19px var(--mono);border-inline-end:1px solid var(--bd);cursor:pointer;user-select:none}
#keys b:active{background:var(--panel2)}
.runout{flex:1;margin:0;padding:12px 14px;overflow:auto;white-space:pre-wrap;word-break:break-word;background:var(--bg);color:var(--fg);font:15px/1.8 var(--mono);unicode-bidi:plaintext;text-align:start}
.runout a{color:var(--acc)}
.webbar{display:flex;gap:8px;align-items:center;flex-wrap:wrap;padding:8px 12px;background:var(--panel2);border-bottom:1px solid var(--bd)}
.webframe{flex:1;width:100%;border:0;background:#fff}
#fab{position:fixed;right:18px;bottom:84px;width:62px;height:62px;border-radius:50%;background:var(--acc);color:var(--accfg);border:0;font-size:26px;
padding:0;box-shadow:0 6px 18px #0008;z-index:20}
#sheet{position:fixed;left:0;right:0;bottom:0;height:52%;background:var(--bg);border-top:3px solid var(--acc);z-index:30;display:none;flex-direction:column}
#sheet.on{display:flex}
.sh1{display:flex;align-items:center;gap:8px;padding:6px 10px;background:var(--panel)}
.sh1 .sp{flex:1}
#out{flex:1;margin:0;padding:10px 14px;overflow:auto;white-space:pre-wrap;word-break:break-word;
font:calc(var(--fs) - 2px)/1.7 var(--mono);unicode-bidi:plaintext;text-align:start}
.inrow{display:flex;gap:6px;padding:6px;background:var(--panel)}
.inp{width:100%;font:inherit;font-size:16px;padding:10px;background:var(--bg);color:var(--fg);border:1px solid var(--bd);border-radius:10px;margin:4px 0;min-width:0}
.inrow .inp{margin:0;flex:1}
#drawer{position:fixed;inset:0;z-index:40;display:none}
#drawer.on{display:block}
#drawer .bk{position:absolute;inset:0;background:#000a}
#drawer .pn{position:absolute;top:0;bottom:0;left:0;width:78%;max-width:320px;background:var(--panel);display:flex;flex-direction:column;overflow:auto}
#drawer .hd{padding:22px 18px;font-size:20px;font-weight:700;color:var(--acc);border-bottom:1px solid var(--bd)}
#drawer .it{padding:15px 18px;font-size:16px;cursor:pointer;border-bottom:1px solid var(--bd)}
#drawer .it:active{background:var(--panel2)}
.popup{position:fixed;z-index:50;background:var(--panel);border:1px solid var(--bd);border-radius:12px;padding:4px;min-width:190px;box-shadow:0 8px 28px #000a}
.popup div{padding:12px 14px;cursor:pointer;border-radius:8px}
.popup div:active{background:var(--panel2)}
#app{flex:1;display:flex;flex-direction:column;min-height:0;min-width:0}
#toast{position:fixed;bottom:90px;left:0;right:0;margin:auto;width:max-content;max-width:90vw;background:var(--panel2);color:var(--fg);
border:1px solid var(--bd);padding:9px 18px;border-radius:20px;opacity:0;transition:.25s;pointer-events:none;z-index:99}
#toast.on{opacity:1}
/* صفحه‌های کامل و جدا */
.pg{flex:1;min-height:0;overflow-y:auto;-webkit-overflow-scrolling:touch;touch-action:pan-y;overscroll-behavior:contain;padding:14px;max-width:820px;width:100%;margin:0 auto}
.card{background:var(--panel);border:1px solid var(--bd);border-radius:14px;padding:14px;margin:10px 0}
.card h4{margin:0 0 6px;color:var(--acc)}
label{font-size:14px;color:var(--mut);display:block;margin-top:12px}
.row{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.row .grow{flex:1;min-width:140px}
.li{display:flex;align-items:center;gap:8px;padding:12px 6px;border-bottom:1px solid var(--bd)}
.li .nm{flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;cursor:pointer;unicode-bidi:plaintext;text-align:start}
.li.d .nm{color:var(--mut)}
.li button{padding:5px 10px}
.chip{display:inline-block;margin:3px;padding:6px 12px;border-radius:18px;background:var(--panel2);border:1px solid var(--bd);cursor:pointer;direction:ltr;font-family:var(--mono);font-size:14px}
table{border-collapse:collapse;width:100%;font-size:14px;margin:6px 0 14px}
td,th{border-bottom:1px solid var(--bd);padding:5px 8px;text-align:start}
td.en{direction:ltr;text-align:left;font-family:var(--mono);color:var(--bi)}
.pyv{display:block;white-space:pre;direction:ltr;text-align:left;background:var(--bg);padding:12px;border-radius:10px;overflow:auto;font-family:var(--mono);margin:0}
.outp{background:var(--bg);border:1px solid var(--bd);border-radius:10px;padding:10px;min-height:90px;max-height:40vh;overflow:auto;white-space:pre-wrap;direction:ltr;text-align:left;font:13px/1.6 var(--mono);margin:8px 0}
</style>
</head>
<body>
<div id="app"></div>
<div id="toast"></div>
<script>
const TOKEN="__TOKEN__";
const PAGE=new URLSearchParams(location.search).get('page')||'main';
const $=s=>document.querySelector(s);
const el=(tag,attrs,...kids)=>{const e=document.createElement(tag);attrs=attrs||{};
 for(const k in attrs){if(k==='class')e.className=attrs[k];else if(k==='text')e.textContent=attrs[k];
 else if(k.startsWith('on'))e[k]=attrs[k];else e.setAttribute(k,attrs[k]);}
 for(const c of kids)e.append(c);return e;};
const esc=s=>s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
const lsGet=(k,d)=>{try{const v=localStorage.getItem(k);return v===null?d:JSON.parse(v);}catch(e){return d;}};
const lsSet=(k,v)=>{try{localStorage.setItem(k,JSON.stringify(v));}catch(e){}};
async function api(path,body){
 const o={headers:{'X-Token':TOKEN}};
 if(body!==undefined){o.method='POST';o.headers['Content-Type']='application/json';o.body=JSON.stringify(body);}
 const r=await fetch(path,o);let j={};
 try{j=await r.json();}catch(e){}
 if(!r.ok)throw new Error(j.error||('خطا '+r.status));
 return j;
}
function toast(t){const x=$('#toast');x.textContent=t;x.classList.add('on');clearTimeout(toast.t);toast.t=setTimeout(()=>x.classList.remove('on'),2200);}
const S=Object.assign({size:17,theme:'olive',dir:'rtl'},lsGet('dari_s',{}));
function applySettings(){
 document.body.className='t-'+(PAGE==='main'?S.theme:'light');
 document.documentElement.style.setProperty('--fs',S.size+'px');
 const ed=$('#ed');if(ed)ed.className='ed '+S.dir;
 lsSet('dari_s',S);
}
function closePage(){window.close();setTimeout(()=>{location.href=urlOf('main');},250);}
const urlOf=p=>'/?t='+TOKEN+(p&&p!=='main'?'&page='+p:'');
const app=$('#app');
function shell(title){   // صفحهٔ کامل و جدا با دکمهٔ بازگشت
 app.innerHTML='';
 const top=el('div',{class:'top'},el('button',{class:'ic',text:'→',onclick:closePage}),el('div',{class:'ttl',text:title}));
 const pg=el('div',{class:'pg'});app.append(top,pg);return pg;
}
function popupAt(btn,items){
 const old=$('#popup');if(old)old.remove();
 const p=el('div',{class:'popup',id:'popup'});
 for(const it of items)p.append(el('div',{text:it[0],onclick:()=>{p.remove();it[1]();}}));
 document.body.append(p);
 const r=btn.getBoundingClientRect();p.style.top=(r.bottom+4)+'px';
 p.style.left=Math.max(6,Math.min(r.right-p.offsetWidth,innerWidth-p.offsetWidth-6))+'px';
}
document.addEventListener('click',e=>{const p=$('#popup');if(p&&!e.target.closest('.popup')&&!e.target.closest('[data-pop]'))p.remove();});
async function follow(id,box,onDone){  // نمایش زندهٔ خروجی یک کار

 let pos=0,code=1;
 for(;;){
  let j;try{j=await api('/api/out?id='+id+'&pos='+pos);}catch(e){box.append(e.message+'\n');break;}
  if(j.text){box.append(j.text);box.scrollTop=box.scrollHeight;}
  pos=j.pos;
  if(j.done){code=j.code;box.append('\n— پایان (کد '+j.code+') —\n');box.scrollTop=box.scrollHeight;break;}
  await new Promise(r=>setTimeout(r,150));
 }
 if(onDone)onDone();
 return {code:code};
}

/* ───────────── صفحهٔ اصلی: ویرایشگر ───────────── */
const RX=/(#[^\n]*)|("""[\s\S]*?(?:"""|$)|'{3}[\s\S]*?(?:'{3}|$)|"(?:\\.|[^"\\\n])*"?|'(?:\\.|[^'\\\n])*'?|«[^»\n]*»?)|([\p{L}_][\p{L}\p{N}_]*)|([0-9۰-۹٠-٩][0-9۰-۹٠-٩._]*)/gu;
async function mainPage(){
 app.innerHTML=
 '<div class="top"><button class="ic" id="bMenu">☰</button><div class="ttl" id="title">پایتون دری</div>'+
 '<button class="ic" id="bFiles" title="پوشه‌ها و فایل‌ها">📁</button><button class="ic" id="bLib" title="کتابخانه‌ها">💡</button>'+
 '<button class="ic" id="bMore" data-pop="1">⋮</button></div>'+
 '<div id="tabs"></div>'+
 '<div class="ed rtl" id="ed"><div class="gut" id="gut">1</div><div class="code"><pre id="hl"></pre>'+
 '<textarea id="ta" spellcheck="false" autocapitalize="off" autocomplete="off" autocorrect="off"></textarea></div>'+
 '<div id="empty">فایلی باز نیست.<br>از منوی ☰ «فایل جدید» یا «نمونه برنامه‌ها» را بزنید.<br><button class="pri" id="bNew">＋ فایل جدید</button></div></div>'+
 '<div id="diag"></div><div id="keys"></div><button id="fab">▶</button>'+
 '<div id="drawer"><div class="bk"></div><div class="pn"><div class="hd">🌿 پایتون دری</div></div></div>';
 const ta=$('#ta'),hl=$('#hl'),gut=$('#gut'),ed=$('#ed');
 let V=await api('/api/vocab');
 const KW=new Set(Object.keys(V.keywords).concat(Object.keys(V.soft),V.pykw)),BI=new Set(Object.keys(V.builtins));
 let T=lsGet('dari_tabs',{tabs:[],cur:null}),dirty=false,lastN=0,timer=null;
 const base=p=>p.split('/').pop();
 function highlight(t){
  let o='',last=0,m;RX.lastIndex=0;
  while((m=RX.exec(t))){
   o+=esc(t.slice(last,m.index));const s=m[0];let c='';
   if(m[1])c='c';else if(m[2])c='s';else if(m[3]){if(KW.has(s))c='k';else if(BI.has(s))c='b';}else c='n';
   o+=c?'<span class="'+c+'">'+esc(s)+'</span>':esc(s);last=RX.lastIndex;
  }
  return o+esc(t.slice(last))+'\n';
 }
 function sync(){hl.scrollTop=ta.scrollTop;hl.scrollLeft=ta.scrollLeft;gut.scrollTop=ta.scrollTop;}
 function refresh(){
  const t=ta.value;hl.innerHTML=highlight(t);const n=t.split('\n').length;
  if(n!==lastN||gutKey!==issKey()){drawGut(n);lastN=n;}sync();
 }
 let issues=[],gutKey='',chk=null,ci=0;
 const issKey=()=>issues.map(i=>i.line+i.sev).join(',');
 function drawGut(n){
  const bad={};for(const i of issues){if(bad[i.line]!=='error')bad[i.line]=i.sev;}
  let h='';for(let i=1;i<=n;i++)h+='<span'+(bad[i]?' class="'+(bad[i]==='error'?'bad':'wrn')+'"':'')+'>'+i+'</span>';
  gut.innerHTML=h;gutKey=issKey();
 }
 function renderDiag(){
  const d=$('#diag');d.className='';
  if(!issues.length){d.textContent='';drawGut(lastN);return;}
  const i=issues[Math.min(ci,issues.length-1)];
  d.className=i.sev;
  d.textContent=(i.sev==='error'?'⛔ ':'⚠️ ')+'خط '+i.line+': '+i.msg+(issues.length>1?'   ('+(Math.min(ci,issues.length-1)+1)+' از '+issues.length+' — لمس برای بعدی)':'');
  drawGut(lastN);
 }
 function jumpTo(line){
  const lines=ta.value.split('\n');let st=0;for(let k=0;k<line-1&&k<lines.length;k++)st+=lines[k].length+1;
  const en=st+(lines[line-1]||'').length;ta.focus();ta.setSelectionRange(st,en);
  const lh=parseFloat(getComputedStyle(ta).lineHeight)||28;ta.scrollTop=Math.max(0,(line-3)*lh);sync();
 }
 $('#diag').onclick=()=>{if(!issues.length)return;const i=issues[Math.min(ci,issues.length-1)];jumpTo(i.line);ci=(ci+1)%issues.length;setTimeout(renderDiag,50);};
 async function check(){
  if(!T.cur){issues=[];renderDiag();return;}
  try{const j=await api('/api/check',{code:ta.value});issues=j.issues||[];ci=0;renderDiag();}catch(e){}
 }
 function saveT(){lsSet('dari_tabs',T);}
 function renderTabs(){
  const bar=$('#tabs');bar.innerHTML='';bar.append(el('div',{class:'tab plus',text:'＋',title:'فایل جدید',onclick:quickNew}));
  for(const p of T.tabs){
   const t=el('div',{class:'tab'+(p===T.cur?' on':''),title:p},el('span',{text:base(p).replace(/\.(dpy|dari|دری)$/,'')+(p===T.cur&&dirty?'*':'')}),
    el('i',{text:'✕',onclick:e=>{e.stopPropagation();closeTab(p);}}));
   t.onclick=()=>switchTo(p);bar.append(t);
  }
  $('#title').textContent=T.cur?base(T.cur).replace(/\.(dpy|dari|دری)$/,''):'پایتون دری';
  $('#empty').style.display=T.cur?'none':'flex';ta.style.visibility=T.cur?'visible':'hidden';
  const on=bar.querySelector('.on');if(on)on.scrollIntoView({inline:'center',block:'nearest'});
 }
 async function save(quiet){
  if(!T.cur||!dirty)return;
  try{await api('/api/file',{path:T.cur,content:ta.value});dirty=false;renderTabs();if(!quiet)toast('ذخیره شد ✓');}
  catch(e){toast(e.message);}
 }
 async function load(p){
  try{const j=await api('/api/file?path='+encodeURIComponent(p));ta.value=j.content;dirty=false;lastN=0;refresh();ta.scrollTop=0;sync();check();return true;}
  catch(e){return false;}
 }
 async function switchTo(p){
  await save(true);T.cur=p;saveT();
  if(!(await load(p))){T.tabs=T.tabs.filter(x=>x!==p);T.cur=T.tabs[0]||null;saveT();if(T.cur)await load(T.cur);else{ta.value='';refresh();}}
  renderTabs();
 }
 async function openFile(p){if(!T.tabs.includes(p))T.tabs.push(p);await switchTo(p);}
 async function closeTab(p){
  if(p===T.cur)await save(true);
  const i=T.tabs.indexOf(p);T.tabs=T.tabs.filter(x=>x!==p);
  if(p===T.cur){T.cur=T.tabs[Math.min(i,T.tabs.length-1)]||null;saveT();if(T.cur)await load(T.cur);else{ta.value='';refresh();}}
  saveT();renderTabs();
 }
 function onEdit(){dirty=true;refresh();renderTabs();clearTimeout(timer);timer=setTimeout(()=>save(true),900);clearTimeout(chk);chk=setTimeout(check,700);}
 ta.addEventListener('input',onEdit);ta.addEventListener('scroll',sync);
 function ins(txt){ta.focus();ta.setRangeText(txt,ta.selectionStart,ta.selectionEnd,'end');onEdit();}
 ta.addEventListener('keydown',e=>{if(e.key==='Tab'){e.preventDefault();ins('    ');}});
 ta.addEventListener('beforeinput',e=>{
  if(e.inputType==='insertLineBreak'||e.inputType==='insertParagraph'){
   e.preventDefault();const v=ta.value,s=ta.selectionStart;
   const ls=v.lastIndexOf('\n',s-1)+1,line=v.slice(ls,s);
   let ind=(line.match(/^[ \t]*/)||[''])[0];
   if(/:\s*$/.test(line.replace(/#.*$/,'')))ind+='    ';
   ta.setRangeText('\n'+ind,s,ta.selectionEnd,'end');onEdit();
  }
 });
 document.addEventListener('keydown',e=>{
  if((e.ctrlKey||e.metaKey)&&e.key==='s'){e.preventDefault();save();}
  if((e.ctrlKey||e.metaKey)&&e.key==='Enter'){e.preventDefault();run();}
 });
 for(const k of ['Tab',':',';',"'",'"','#','(',')','[',']','{','}','=','+','-','*','/','%','<','>','_','،','.',',','«','»','\\','&','|','!','@']){
  const b=el('b',{text:k});
  b.addEventListener('pointerdown',e=>{e.preventDefault();ins(k==='Tab'?'    ':k);});
  $('#keys').append(b);
 }
 /* اجرا: یک صفحهٔ سفید، کامل و مستقل */
 async function run(){
  if(!T.cur){toast('ابتدا یک فایل باز یا ایجاد کنید');return;}
  await save(true);
  const u=urlOf('run')+'&path='+encodeURIComponent(T.cur);
  if(!window.open(u,'dari_run'))location.href=u;
 }
 $('#fab').onclick=run;
 /* برگه‌ها و منو */
 const go=async p=>{await save(true);if(!window.open(urlOf(p),'dari_'+p))location.href=urlOf(p);};
 async function quickNew(){
  try{await save(true);const j=await api('/api/new',{path:'برنامه',kind:'file',content:'# برنامهٔ تازه\n',unique:true});await openFile(j.path);ta.focus();}catch(e){toast(e.message);}
 }
 async function newFile(){
  const n=(prompt('نام فایل جدید (پسوند .dpy خودکار اضافه می‌شود):','برنامه')||'').trim();if(!n)return;
  try{const j=await api('/api/new',{path:n,kind:'file',content:'# برنامهٔ تازه\n'});await openFile(j.path);}catch(e){toast(e.message);}
 }
 async function renameCur(){
  if(!T.cur)return toast('فایلی باز نیست');
  const n=(prompt('نام تازه:',T.cur)||'').trim();if(!n||n===T.cur)return;
  try{await save(true);const j=await api('/api/rename',{path:T.cur,to:n});T.tabs=T.tabs.map(x=>x===T.cur?j.path:x);T.cur=j.path;saveT();renderTabs();}
  catch(e){toast(e.message);}
 }
 async function deleteCur(){
  if(!T.cur)return toast('فایلی باز نیست');
  if(!confirm('فایل «'+T.cur+'» برای همیشه حذف شود؟'))return;
  const p=T.cur;try{await api('/api/delete',{path:p});dirty=false;await closeTab(p);}catch(e){toast(e.message);}
 }
 async function examples(){
  let ex;try{ex=await api('/api/examples');}catch(e){return toast(e.message);}
  const names=Object.keys(ex);const c=prompt('شمارهٔ نمونه را بنویسید:\n'+names.map((n,i)=>(i+1)+') '+n).join('\n'),'1');
  const i=parseInt(c,10)-1;if(!(i>=0&&i<names.length))return;
  try{const j=await api('/api/new',{path:names[i],kind:'file',content:ex[names[i]],unique:true});await openFile(j.path);}catch(e){toast(e.message);}
 }
 const menu=[['📄  فایل جدید',newFile],['💾  ذخیره',()=>save()],['📁  پوشه‌ها و فایل‌ها',()=>go('files')],['💡  کتابخانه‌ها (pip)',()=>go('lib')],
  ['🧩  نمونه برنامه‌ها',examples],['🐍  کد پایتونِ معادل',()=>go('py')],['⚙️  تنظیمات',()=>go('settings')],['📖  راهنما و واژگان',()=>go('help')]];
 const pn=$('#drawer .pn');
 for(const m of menu)pn.append(el('div',{class:'it',text:m[0],onclick:()=>{$('#drawer').classList.remove('on');m[1]();}}));
 $('#bNew').onclick=quickNew;
 $('#bMenu').onclick=()=>$('#drawer').classList.add('on');
 $('#drawer .bk').onclick=()=>$('#drawer').classList.remove('on');
 $('#bFiles').onclick=()=>go('files');$('#bLib').onclick=()=>go('lib');
 $('#bMore').onclick=e=>popupAt(e.currentTarget,[['ذخیره',()=>save()],['تغییر نام',renameCur],['حذف فایل',deleteCur],
  ['کد پایتونِ معادل',()=>go('py')],['تنظیمات',()=>go('settings')],['راهنما',()=>go('help')]]);
 window.addEventListener('pagehide',()=>{if(dirty&&T.cur){try{fetch('/api/file',{method:'POST',keepalive:true,headers:{'X-Token':TOKEN,'Content-Type':'application/json'},body:JSON.stringify({path:T.cur,content:ta.value})});}catch(e){}}});
 window.addEventListener('storage',async e=>{
  if(e.key==='dari_s'){try{Object.assign(S,JSON.parse(e.newValue));}catch(x){}applySettings();}
  else if(e.key==='dari_open'&&e.newValue&&e.newValue!=='null'){const w=JSON.parse(e.newValue);lsSet('dari_open',null);await openFile(w);}
  else if(e.key==='dari_err'&&e.newValue){try{const r=JSON.parse(e.newValue);if(r.path===T.cur&&r.line){issues=[{line:r.line,sev:'error',msg:r.msg}];ci=0;renderDiag();}}catch(x){}}
  else if(e.key==='dari_tabs'&&e.newValue){const n=JSON.parse(e.newValue);await save(true);T=n;if(T.cur)await load(T.cur);else{ta.value='';refresh();}renderTabs();}
 });
 applySettings();
 const want=lsGet('dari_open',null);
 if(want){lsSet('dari_open',null);await openFile(want);}
 else if(T.cur){await switchTo(T.cur);}
 else{
  let items=[];try{items=(await api('/api/files')).items;}catch(e){}
  const first=items.find(i=>!i.dir&&/\.(dpy|dari)$/.test(i.path));
  if(first)await openFile(first.path);else{refresh();renderTabs();}
 }
 renderTabs();refresh();
}

/* ───────────── صفحهٔ پوشه‌ها و فایل‌ها ───────────── */
async function filesPage(){
 const pg=shell('پوشه‌ها و فایل‌ها');
 const rootEl=el('div',{class:'mut',style:'direction:ltr;text-align:left;word-break:break-all;margin-bottom:8px'});
 const list=el('div',{class:'card'});
 const open=p=>{lsSet('dari_open',p);closePage();};
 async function reload(){
  const j=await api('/api/files');rootEl.textContent=j.root;list.innerHTML='';
  if(!j.items.length)list.append(el('div',{class:'mut',text:'پوشه خالی است. «فایل جدید» را بزنید.'}));
  for(const it of j.items){
   const row=el('div',{class:'li'+(it.dir?' d':'')});
   const nm=el('div',{class:'nm',text:(it.dir?'📁 ':'📄 ')+it.path.split('/').pop(),onclick:()=>{if(!it.dir)open(it.path);}});
   nm.style.paddingInlineStart=(it.depth*16)+'px';
   row.append(nm);
   if(!it.dir)row.append(el('button',{text:'✎',title:'تغییر نام',onclick:async()=>{
     const n=(prompt('نام تازه:',it.path)||'').trim();if(!n||n===it.path)return;
     try{await api('/api/rename',{path:it.path,to:n});const T=lsGet('dari_tabs',{tabs:[],cur:null});
      T.tabs=T.tabs.map(x=>x===it.path?n:x);if(T.cur===it.path)T.cur=n;lsSet('dari_tabs',T);reload();}catch(e){toast(e.message);}}}));
   row.append(el('button',{class:'dng',text:'🗑',title:'حذف',onclick:async()=>{
     if(!confirm('«'+it.path+'» حذف شود؟'))return;
     try{await api('/api/delete',{path:it.path});const T=lsGet('dari_tabs',{tabs:[],cur:null});
      T.tabs=T.tabs.filter(x=>x!==it.path&&!x.startsWith(it.path+'/'));if(!T.tabs.includes(T.cur))T.cur=T.tabs[0]||null;lsSet('dari_tabs',T);reload();}catch(e){toast(e.message);}}}));
   list.append(row);
  }
 }
 const bar=el('div',{class:'row'},
  el('button',{class:'pri',text:'📄 فایل جدید',onclick:async()=>{
   const n=(prompt('نام فایل (برای ساخت داخل پوشه: پوشه/نام):','برنامه')||'').trim();if(!n)return;
   try{const j=await api('/api/new',{path:n,kind:'file',content:'# برنامهٔ تازه\n'});open(j.path);}catch(e){toast(e.message);}}}),
  el('button',{text:'📁 پوشهٔ جدید',onclick:async()=>{
   const n=(prompt('نام پوشهٔ جدید:','')||'').trim();if(!n)return;
   try{await api('/api/new',{path:n,kind:'dir'});reload();}catch(e){toast(e.message);}}}),
  el('button',{text:'🧩 نمونه‌ها',onclick:async()=>{
   try{const ex=await api('/api/examples');exBox.innerHTML='';
    for(const n of Object.keys(ex))exBox.append(el('div',{class:'li'},el('div',{class:'nm',text:'🧩 '+n,onclick:async()=>{
     const j=await api('/api/new',{path:n,kind:'file',content:ex[n],unique:true});open(j.path);}})));
    exBox.style.display='block';}catch(e){toast(e.message);}}}));
 const exBox=el('div',{class:'card',style:'display:none'});
 pg.append(bar,rootEl,exBox,list);
 const ws=el('input',{class:'inp',dir:'ltr'});
 pg.append(el('div',{class:'card'},el('h4',{text:'پوشهٔ کار'}),el('div',{class:'mut',text:'فایل‌ها در این پوشه روی دستگاه شما ذخیره می‌شوند.'}),ws,
  el('button',{text:'تغییر پوشهٔ کار',onclick:async()=>{
   try{await api('/api/workspace',{path:ws.value});lsSet('dari_tabs',{tabs:[],cur:null});toast('پوشهٔ کار تغییر کرد');reload();}catch(e){toast(e.message);}}})));
 await reload();ws.value=rootEl.textContent;
}

/* ───────────── صفحهٔ کتابخانه‌ها (pip) ───────────── */
const POP=('requests numpy pandas scipy matplotlib flask django fastapi uvicorn aiohttp httpx beautifulsoup4 lxml selenium playwright '+
 'pillow opencv-python pygame pyserial pyqt5 pyside6 torch tensorflow keras scikit-learn transformers openai anthropic langchain '+
 'python-telegram-bot telethon discord.py aiogram websockets websocket-client paho-mqtt sqlalchemy psycopg2-binary pymongo redis '+
 'pyinstaller pytest rich colorama tqdm click pyyaml python-dotenv cryptography pyjwt bcrypt gtts pyttsx3 speechrecognition '+
 'sympy networkx nltk spacy yfinance pyautogui schedule apscheduler celery boto3 firebase-admin kivy').split(' ');
async function libPage(){
 const pg=shell('کتابخانه‌ها (pip)');
 const inp=el('input',{class:'inp',dir:'ltr',placeholder:'requests numpy ...',autocomplete:'off',autocapitalize:'off'});
 const chips=el('div'),res=el('div'),banner=el('div'),box=el('pre',{class:'outp'}),inst=el('div'),count=el('div',{class:'mut'});
 let busy=false,list=[];
 const norm=n=>n.toLowerCase().replace(/\[.*$/,'').replace(/[=<>!~].*$/,'').replace(/[-_.]+/g,'-');
 const verOf=n=>{const k=norm(n);const f=list.find(p=>norm(p.name)===k);return f?f.version:null;};
 const faNum=n=>String(n).replace(/\d/g,d=>'۰۱۲۳۴۵۶۷۸۹'[d]);
 function why(t){
  if(/Could not find a version|No matching distribution|not found in the package index/i.test(t))return 'این اسم در PyPI پیدا نشد؛ املای آن را بررسی کنید.';
  if(/Temporary failure|NewConnectionError|Connection (?:aborted|refused|reset)|Network is unreachable|Name or service not known|timed out|ProxyError|Max retries/i.test(t))return 'اینترنت در دسترس نیست یا قطع شد.';
  if(/externally-managed-environment/i.test(t))return 'پایتون این دستگاه اجازهٔ نصب مستقیم نمی‌دهد (محیط مدیریت‌شده).';
  if(/Permission denied|EACCES|Errno 13/i.test(t))return 'اجازهٔ نوشتن در پوشهٔ پایتون وجود ندارد.';
  if(/subprocess-exited-with-error|Failed building wheel|Failed to build|compiler|gcc|cl\.exe|Microsoft Visual/i.test(t))return 'ساخت این کتابخانه روی این دستگاه ممکن نشد (به کامپایلر نیاز دارد و نسخهٔ آماده برای این گوشی ندارد).';
  return 'دلیل (از خروجی pip): '+(t.trim().split('\n').filter(l=>l.trim()&&!/^— پایان/.test(l)).slice(-3).join(' | ')||'خروجی خالی بود');
 }
 function say(kind,text,sub){   // kind: ok | bad | info
  const c={ok:'#0a7d43',bad:'#c0392b',info:'#164e9b'}[kind];
  const d=el('div',{class:'card',style:'border-inline-start:6px solid '+c});
  d.append(el('div',{style:'font-weight:700;color:'+c,text:text}));
  if(sub)d.append(el('div',{class:'mut',text:sub}));
  banner.append(d);
 }
 function sug(){
  chips.innerHTML='';const q=inp.value.trim().split(/\s+/).pop().toLowerCase();
  const l=(q?POP.filter(x=>x.includes(q)):POP.slice(0,14)).slice(0,18);
  for(const n of l){const ok=verOf(n);chips.append(el('span',{class:'chip',text:(ok?'✓ ':'')+n,onclick:()=>{const w=inp.value.trim().split(/\s+/);w.pop();w.push(n);inp.value=w.filter(Boolean).join(' ')+' ';sug();}}));}
 }
 async function loadInst(){
  try{const j=await api('/api/piplist');list=j.items;}catch(e){inst.innerHTML='';inst.append(el('div',{class:'mut',text:e.message}));return false;}
  count.textContent=faNum(list.length)+' کتابخانه روی این دستگاه نصب شده است.';
  inst.innerHTML='';
  const f=el('input',{class:'inp',dir:'ltr',placeholder:'فیلتر…'});const lst=el('div');
  const draw=()=>{lst.innerHTML='';for(const p of list.filter(p=>p.name.toLowerCase().includes(f.value.toLowerCase()))){
    lst.append(el('div',{class:'li'},el('div',{class:'nm',style:'direction:ltr;text-align:left',text:'✓ '+p.name+'  '+p.version}),
     el('button',{text:'↑',title:'به‌روزرسانی',onclick:()=>runPip('upgrade',p.name)}),
     el('button',{class:'dng',text:'✕',title:'حذف',onclick:()=>{if(confirm('«'+p.name+'» حذف شود؟'))runPip('uninstall',p.name);}})));}};
  f.oninput=draw;draw();inst.append(f,lst);sug();return true;
 }
 async function runPip(action,names){
  if(busy)return toast('یک کار در حال اجراست');
  names=names.trim();if(!names)return;
  busy=true;box.textContent='';banner.innerHTML='';
  const arr=names.split(/\s+/);const before={};for(const n of arr)before[n]=verOf(n);
  say('info',({install:'در حال نصب…',upgrade:'در حال به‌روزرسانی…',uninstall:'در حال حذف…'})[action]+' ('+names+')','چند لحظه صبر کنید.');
  let code=1;
  try{const j=await api('/api/pip',{name:names,action});const r=await follow(j.id,box);code=r.code;}catch(e){box.textContent=e.message;}
  await loadInst();banner.innerHTML='';
  const out=box.textContent;const satisfied=/already satisfied/i.test(out)&&!/Successfully installed/i.test(out);
  for(const n of arr){
   const v=verOf(n);
   if(action==='uninstall'){
    if(!v)say('ok','✅ «'+n+'» حذف شد.');else say('bad','❌ «'+n+'» حذف نشد.',why(out));
   }else if(v){
    if(action==='upgrade')say('ok',(before[n]&&before[n]!==v?'✅ «'+n+'» به نسخهٔ '+v+' به‌روز شد.':'✅ «'+n+'» از قبل آخرین نسخه ('+v+') بود.'));
    else if(satisfied&&before[n])say('info','ℹ️ «'+n+'» از قبل نصب بود (نسخهٔ '+v+'). نیازی به نصب دوباره نیست.');
    else say('ok','✅ «'+n+'» با موفقیت نصب شد (نسخهٔ '+v+').','حالا در برنامه بنویسید: وارد_کن '+n);
   }else{
    say('bad','❌ «'+n+'» نصب نشد.',why(out));
   }
  }
  busy=false;
 }
 async function search(){
  const names=inp.value.trim().split(/\s+/).filter(Boolean);if(!names.length)return;
  res.innerHTML='';
  if(!list.length)await loadInst();
  for(const n of names){
   const v=verOf(n);
   const card=el('div',{class:'card'});res.append(card);
   if(v){
    card.append(el('div',{style:'font-weight:700;color:#0a7d43',text:'✅ «'+n+'» نصب شده است (نسخهٔ '+v+').'}),
     el('div',{class:'row',style:'margin-top:8px'},el('button',{text:'↑ به‌روزرسانی',onclick:()=>runPip('upgrade',n)}),
      el('button',{class:'dng',text:'✕ حذف',onclick:()=>{if(confirm('«'+n+'» حذف شود؟'))runPip('uninstall',n);}})));
    continue;
   }
   card.append(el('div',{class:'mut',text:'در حال جستجوی «'+n+'» در PyPI…'}));
   try{
    const j=await api('/api/pypi?name='+encodeURIComponent(n));card.innerHTML='';
    if(!j.found){card.append(el('div',{style:'font-weight:700;color:#c0392b',text:'❌ کتابخانه‌ای با نام «'+n+'» در PyPI وجود ندارد.'}),el('div',{class:'mut',text:'املای آن را بررسی کنید.'}));continue;}
    card.append(el('div',{style:'font-weight:700;color:#b9770e',text:'⬜ «'+j.name+'» نصب نشده است.'}),
     el('div',{text:'آخرین نسخه: '+j.version+(j.summary?' — '+j.summary:''),style:'direction:ltr;text-align:left;margin:6px 0'}),
     el('button',{class:'pri',text:'⬇ نصب',onclick:()=>runPip('install',j.name)}));
   }catch(e){
    card.innerHTML='';
    card.append(el('div',{style:'font-weight:700;color:#b9770e',text:'⬜ «'+n+'» روی این دستگاه نصب نیست.'}),
     el('div',{class:'mut',text:'برای بررسی وجود آن در PyPI و نصب، اینترنت لازم است ('+e.message+').'}),
     el('button',{class:'pri',style:'margin-top:8px',text:'⬇ تلاش برای نصب',onclick:()=>runPip('install',n)}));
   }
  }
 }
 inp.oninput=sug;inp.onkeydown=e=>{if(e.key==='Enter')search();};
 const bar=el('div',{class:'row'},el('button',{text:'🔍 جستجو (نصب شده؟)',onclick:search}),
  el('button',{class:'pri',text:'⬇ نصب',onclick:()=>runPip('install',inp.value)}));
 const det=el('details',{},el('summary',{text:'جزئیات فنی (خروجی pip)'}),box);
 pg.append(el('div',{class:'card'},el('div',{class:'mut',text:'نام کتابخانه را انگلیسی بنویسید (چند نام با فاصله). «جستجو» می‌گوید نصب هست یا نه؛ «نصب» آن را نصب می‌کند و نتیجه را به فارسی می‌گوید.'}),inp,bar,chips),
  banner,res,el('div',{class:'card'},el('h4',{text:'کتابخانه‌های نصب‌شده'}),count,inst),det);
 sug();loadInst();
}

/* ───────────── صفحهٔ تنظیمات ───────────── */
function settingsPage(){
 const pg=shell('تنظیمات');
 const sel=(opts,val,fn)=>{const s=el('select',{class:'inp'});for(const [v,t] of opts){const o=el('option',{value:v,text:t});if(v===val)o.selected=true;s.append(o);}s.onchange=()=>fn(s.value);return s;};
 const sv=el('span',{class:'mut',text:S.size+'px'});
 const size=el('input',{type:'range',min:12,max:30,value:S.size,class:'inp'});
 size.oninput=()=>{S.size=+size.value;sv.textContent=S.size+'px';applySettings();};
 pg.append(el('div',{class:'card'},
  el('label',{text:'اندازهٔ قلم'}),size,sv,
  el('label',{text:'پوسته'}),sel([['olive','زیتونی (مثل عکس)'],['dark','تیره'],['light','روشن']],S.theme,v=>{S.theme=v;applySettings();}),
  el('label',{text:'جهت ویرایشگر'}),sel([['rtl','راست‌به‌چپ'],['ltr','چپ‌به‌راست'],['auto','خودکار (هر خط جدا)']],S.dir,v=>{S.dir=v;applySettings();})),
  el('div',{class:'card'},el('h4',{text:'پوشهٔ کار'}),el('div',{class:'mut',text:'برای تغییر پوشه به بخش «پوشه‌ها و فایل‌ها» بروید.'}),
   el('button',{text:'📁 باز کردن پوشه‌ها و فایل‌ها',onclick:()=>{location.href=urlOf('files');}})),
  el('div',{class:'card'},el('h4',{text:'درباره'}),el('div',{text:'پایتون دری — پایتون ۳ با دستورهای فارسی/دری. همهٔ کتابخانه‌های پایتون با نام اصلی کار می‌کنند.'})));
 applySettings();
}

/* ───────────── صفحهٔ راهنما و واژگان ───────────── */
async function helpPage(){
 const pg=shell('راهنما و واژگان');const V=await api('/api/vocab');
 pg.append(el('div',{class:'card'},el('h4',{text:'شروع سریع'}),
  el('div',{style:'line-height:2',text:'۱) از ☰ «فایل جدید» یا «نمونه برنامه‌ها». ۲) برنامه را بنویسید و دکمهٔ زردِ ▶ را بزنید. ۳) هر کتابخانه‌ای را از 💡 نصب کنید و با نام اصلی‌اش وارد کنید. ۴) نام فارسی ماژول‌ها اختیاری است: «وارد_کن ریاضی». ۵) دری و انگلیسی را می‌توانید قاطی کنید. ۶) واژه‌های شخصی: فایل «واژگان.json» در پوشهٔ کار.'})));
 const q=el('input',{class:'inp',placeholder:'جستجو در واژگان (دری یا انگلیسی)…'});const box=el('div');
 const groups=[['دستورها','keywords'],['دستورهای ویژه','soft'],['توابع و خطاهای آماده','builtins'],['نام ورودی‌ها (مثل sep=)','kwargs'],
  ['متدها و اعضای ماژول‌ها (بعد از نقطه)','attrs'],['ماژول‌ها','modules'],['متدهای ویژهٔ کلاس','dunders']];
 const render=()=>{box.innerHTML='';const f=q.value.trim().toLowerCase();
  for(const [title,key] of groups){const rows=Object.entries(V[key]).filter(([a,b])=>!f||a.includes(f)||b.toLowerCase().includes(f));
   if(!rows.length)continue;const t=el('table');
   for(const [a,b] of rows)t.append(el('tr',{},el('td',{text:a}),el('td',{class:'en',text:b})));
   box.append(el('div',{class:'card'},el('h4',{text:title+' ('+rows.length+')'}),t));}};
 q.oninput=render;render();pg.prepend(q);pg.append(box);
}


/* ───────────── صفحهٔ اجرا: محیط کامل و مستقل ───────────── */
function linkify(txt){
 return esc(txt).replace(/(https?:\/\/[^\s<>"')]+)/g,'<a href="$1" target="_blank" rel="noopener">$1</a>');
}
async function runPage(){
 const qs=new URLSearchParams(location.search);const path=qs.get('path')||'';
 app.innerHTML='';
 const title=path.split('/').pop().replace(/\.(dpy|dari|دری)$/,'')||'برنامه';
 document.title=title;
 const bStop=el('button',{class:'dng',text:'■ توقف'}),bRun=el('button',{class:'pri',text:'▶ دوباره'});
 const st=el('span',{class:'mut'});
 const top=el('div',{class:'top'},el('button',{class:'ic',text:'→',onclick:closePage}),el('div',{class:'ttl',text:title}),st,bRun,bStop);
 const web=el('div',{class:'webbar',style:'display:none'});
 const frameBox=el('div',{style:'display:none;flex:1;min-height:0'});
 const out=el('pre',{class:'runout'});
 const inp=el('input',{class:'inp',placeholder:'ورودی برنامه، سپس Enter',autocomplete:'off'});
 const inrow=el('div',{class:'inrow'},inp,el('button',{text:'ارسال',onclick:sendIn}));
 app.append(top,web,frameBox,out,inrow);
 let job=null,shown=false;
 function setRun(on){bStop.disabled=!on;bRun.disabled=on;st.textContent=on?'● در حال اجرا':'';inrow.style.display=on?'flex':'none';}
 function detectWeb(t){
  if(shown)return;
  const m=t.match(/https?:\/\/(?:127\.0\.0\.1|localhost|0\.0\.0\.0):\d+[^\s<>"')]*/);
  if(!m)return;shown=true;const u=m[0].replace('0.0.0.0','127.0.0.1');
  web.style.display='flex';web.innerHTML='';
  web.append(el('span',{text:'🌐 برنامهٔ وب اجرا شد'}),
   el('button',{class:'pri',text:'نمایش در همین صفحه',onclick:()=>{frameBox.innerHTML='';frameBox.append(el('iframe',{src:u,class:'webframe'}));frameBox.style.display='flex';out.style.display='none';inrow.style.display='none';}}),
   el('button',{text:'تب جدید',onclick:()=>window.open(u,'_blank')}),
   el('button',{text:'لاگ',onclick:()=>{frameBox.style.display='none';out.style.display='block';}}));
 }
 async function start(){
  out.textContent='';shown=false;web.style.display='none';frameBox.style.display='none';out.style.display='block';
  try{const j=await api('/api/run',{path});job=j.id;setRun(true);
   let pos=0;
   for(;;){
    const r=await api('/api/out?id='+job+'&pos='+pos);
    if(r.text){out.insertAdjacentHTML('beforeend',linkify(r.text));out.scrollTop=out.scrollHeight;detectWeb(out.textContent);}
    pos=r.pos;
    if(r.done){out.insertAdjacentHTML('beforeend','\n— پایان (کد '+r.code+') —\n');break;}
    await new Promise(x=>setTimeout(x,150));
   }
  }catch(e){out.textContent=e.message;}
  job=null;setRun(false);
  const t=out.textContent;const m=[...t.matchAll(/خط (\d+)/g)].pop();
  const e=t.split('\n').filter(l=>/^خطای/.test(l)).pop();
  if(m&&e)lsSet('dari_err',{path,line:+m[1],msg:e,ts:Date.now()});
 }
 async function sendIn(){
  if(!job)return;const v=inp.value;inp.value='';out.append(v+'\n');
  try{await api('/api/stdin',{id:job,text:v});}catch(e){toast(e.message);}
 }
 inp.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();sendIn();}});
 bStop.onclick=async()=>{if(job){try{await api('/api/stop',{id:job});}catch(e){}}};
 bRun.onclick=start;
 start();
}

/* ───────────── صفحهٔ کد پایتونِ معادل ───────────── */
async function pyPage(){
 const pg=shell('کد پایتونِ معادل');const T=lsGet('dari_tabs',{tabs:[],cur:null});
 if(!T.cur){pg.append(el('div',{class:'card',text:'فایلی باز نیست.'}));return;}
 try{const f=await api('/api/file?path='+encodeURIComponent(T.cur));const j=await api('/api/translate',{code:f.content});
  pg.append(el('div',{class:'mut',text:T.cur}),el('pre',{class:'pyv',text:j.py}));}
 catch(e){pg.append(el('pre',{class:'pyv',text:e.message}));}
}

(async()=>{
 applySettings();
 try{if('serviceWorker' in navigator)navigator.serviceWorker.register('/sw.js?t='+TOKEN,{scope:'/'}).catch(()=>{});}catch(e){}
 try{
  if(PAGE==='files')await filesPage();
  else if(PAGE==='lib')await libPage();
  else if(PAGE==='settings')settingsPage();
  else if(PAGE==='help')await helpPage();
  else if(PAGE==='py')await pyPage();
  else if(PAGE==='run')await runPage();
  else await mainPage();
 }catch(e){app.innerHTML='<div class="pg">خطا در راه‌اندازی: '+esc(e.message)+'</div>';}
 applySettings();
})();
</script>
</body>
</html>
'''


# ════════════════════════════════════════════════════════════════════
#  ۶. خط فرمان
# ════════════════════════════════════════════════════════════════════

USAGE = """پایتون دری %s

  python3 dari_python.py                      باز کردن محیط برنامه‌نویسی
  python3 dari_python.py ide [پوشه]           محیط با پوشهٔ دلخواه  (--port N  --no-browser)
  python3 dari_python.py run برنامه.dpy       اجرای برنامه
  python3 dari_python.py shell                پوستهٔ تعاملی
  python3 dari_python.py translate برنامه.dpy دیدن کد پایتونِ معادل
""" % __version__


def _utf8():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def main(argv=None):
    a = list(sys.argv[1:] if argv is None else argv)
    _utf8()
    if not a:
        return cmd_ide([])
    c = a[0]
    if c in ("ide", "محیط", "ویرایشگر"):
        return cmd_ide(a[1:])
    if c in ("run", "اجرا"):
        if len(a) < 2:
            print(USAGE)
            return 2
        return run_file(a[1], a[2:])
    if c in ("shell", "repl", "پوسته"):
        return cmd_shell()
    if c in ("translate", "ترجمه"):
        if len(a) < 2:
            print(USAGE)
            return 2
        with open(a[1], encoding="utf-8-sig") as f:
            src = f.read()
        try:
            sys.stdout.write(transpile(src))
        except SyntaxError as e:
            sys.stderr.write(format_syntax_error(e, a[1], src.split("\n")))
            return 1
        return 0
    if c in ("-h", "--help", "help", "راهنما"):
        print(USAGE)
        return 0
    if os.path.isfile(c):
        return run_file(c, a[1:])
    print(USAGE)
    return 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
