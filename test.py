from django.shortcuts import render
import matplotlib.pyplot as plt
import io
import urllib, base64
from products.models import Stock
import mplfinance as mpf
import pandas as pd