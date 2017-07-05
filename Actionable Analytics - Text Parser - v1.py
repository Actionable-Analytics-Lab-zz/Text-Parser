#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 22:13:31 2017

@author: hamjad
"""

################################################################################################
#Packages used in code. Place HANSA.HTM File in working directory
################################################################################################
import re
import os
currdir = os.getcwd()

################################################################################################
#Created functions used in code
################################################################################################
def cleanHtml(html):
    htmltaglist = [r'<p.*?>',r'</p>',r'<div.*?>',r'</div>']
    for tag in htmltaglist:
        html = re.sub(tag, '', html)
        
    html = re.sub(r'<br>', r'\n', html)
    return html

################################################################################################
#Reading the data from raw HANSA file, rewrite file path as needed
################################################################################################
with open(currdir+r'/HANSA.HTM', encoding='utf-8') as input:
    raw = input.read()
    
################################################################################################
#Removing line breaks, tabs and other white space characters, except for single spaces, from string
################################################################################################
onlySpaces = re.sub(r'\s+', ' ', raw)

################################################################################################
#Pull desired values out of cleaned string
################################################################################################
item = re.search(r'<h2.*?>(.*?)</h2>',onlySpaces).group(1)

listingPrice = re.search(r'<div.*?> <strong>(.*?)</strong>',onlySpaces).group(1)
listingPrice = float(re.sub(r'USD\s', '', listingPrice))

vendorname = re.search(r'<td>Vendor</td> <td><a.*?>(.*?)</a>',onlySpaces).group(1)

description = cleanHtml(re.search(r'<h3><u>Listing Details</u></h3>(.*)<footer>',onlySpaces).group(1))

################################################################################################
#Output values
################################################################################################
print("Item Name: ",item)
print("Listing Price: ", listingPrice)
print("Vendor Name: ", vendorname)
print("Description: \n", description)