# -*- coding: utf-8 -*-
"""
Version 6

Updated by: Jeremy Liu

Features:
    - Robust to errors when grabbing data. Will make a new file listing all the files that had an error.
    - Completed Vendor Parser
    
To-Do:
    -Extend functionality of cleanHTML
    -Explicity cast data types in DataFrame
    -Add connection to Database (once Database is set up)
    -Fix sloppy regular expressions statements for reviewerList and feedbackDateList

"""

################################################################################################
#Packages used in code
################################################################################################
import re
import os
import pandas as pd

################################################################################################
#Created functions used in code
################################################################################################
def cleanHTML(html):
    htmltaglist = [r'<p.*?>',r'</p>',r'<div.*?>',r'</div>',r'<u>',r'</u>',r'<b>',r'</b>',r'<i>','r</i>',r'<h1.*?>',r'</h1>',r'<h2.*?>',r'</h2>',r'<h3.*?>',r'</h3>',r'<h4.*?>',r'</h4>',r'<h5.*?>',r'</h5>',r'<h6.*?>',r'</h6>',r'<em>',r'</em>',r'<code>',r'</code>']
    for tag in htmltaglist:
        html = re.sub(tag, '', html)
        
    html = re.sub(r'<br.*?>',r'\n', html)
    
    
    specialEntities = {'r&quot;': r'"',r'&amp;': r'&',r'&lt;': r'<',r'&gt;': r'>',r'&OElig;': r'Œ',r'&oelig;': r'œ',r'&Scaron;': r'Š',r'&scaron;': r'š',r'&Yuml;': r'Ÿ',r'&circ;': r'ˆ',r'&tilde;': r'˜',r'&ensp;': r' ',r'&emsp;': r' ',r'&thinsp;': r' ',r'&zwnj;': r'‌',r'&zwj;': r'‍',r'&lrm;': r'‎',r'&rlm;': r'‏',r'&ndash;': r'–',r'&mdash;': r'—',r'&lsquo;': r'‘',r'&rsquo;': r'’',r'&sbquo;': r'‚',r'&ldquo;': r'“',r'&rdquo;': r'”',r'&bdquo;': r'„',r'&dagger;': r'†',r'&Dagger;': r'‡',r'&permil;': r'‰',r'&lsaquo;': r'‹',r'&rsaquo;': r'›',r'&euro;': r'€'}
    for key, value in specialEntities.items():
        html = re.sub(key,value, html)
        return html

################################################################################################
#Create empty DataFrames which will be used to store the data pulled from files
################################################################################################
columnsListing = ['Listing ID', 'Listing Name', 'Category Name', 'Category ID', 'Listing Price USD', 'Listing Price BTC', 'Vendor Name', 'Description', 'Delivery Method', 'Ships From', 'Ships To', 'Date', 'Url']
structuredDataListing = pd.DataFrame(columns=columnsListing)

columnsPackageAttributes = ['Listing ID', 'Address Label', 'Type of Envelope', 'Vacuum Packed or Heat Sealed', 'Avg. Layers of Mylar', 'Barrier', 'Decoy Item', 'Return Address', 'Date']
structuredDataPackageAttributes = pd.DataFrame(columns=columnsPackageAttributes)

columnsTerms = ['Listing ID', 'Terms and Conditions', 'Date']
structuredDataTerms = pd.DataFrame(columns=columnsTerms)

columnsViews = ['Listing ID', 'Number of Views', 'Date']
structuredDataViews = pd.DataFrame(columns=columnsViews)

columnsFeedback = ['Listing ID', 'Thumbs Up/Down', 'Feedback Text', 'Actual Delivery Time', 'Reviewer', 'Date']
structuredDataFeedback = pd.DataFrame(columns=columnsFeedback)

columnsVendorProfile = ['Vendor Name', 'Vendor Profile', 'Trusted Vendor?', 'Vendor Level', 'Positive Feedback', 'Neutral Feedback', 'Negative Feedback', 'Vendor Registration Date', 'Number of Subscribers', 'Number of Orders', 'Average Volume USD (per order)', 'Average Volume BTC (per order)', 'Date', 'URL']
structuredDataVendorProfile = pd.DataFrame(columns=columnsVendorProfile)

columnsVendorPGP = ['Vendor Name', 'PGP Key']
structuredDataVendorPGP = pd.DataFrame(columns=columnsVendorPGP)

columnsVendorTerms = ['Vendor Name', 'Terms and Conditions']
structuredDataVendorTerms = pd.DataFrame(columns=columnsVendorTerms)

columnsError = ['Type', 'Possible Reasoning', 'File']
structuredDataError = pd.DataFrame(columns=columnsError)
################################################################################################
#Start For Loop. Fan through every file in certain directory. 
################################################################################################
for path, subdirs, files in os.walk(os.getcwd()+r'\HansaMarketFullFiles'):
    for filename in files:
        fileName = os.path.join(path, filename)
        
################################################################################################
#Reading the data from raw HANSA file
################################################################################################
        with open(fileName, encoding='utf-8') as input:
            raw = input.read()
    
################################################################################################
#Removing line breaks, tabs and other white space characters, except for single spaces, from string
################################################################################################
        onlySpaces = re.sub(r'\s+', ' ', raw)

################################################################################################
#Pull desired values out of cleaned string
################################################################################################
        if "vendor" in filename and "terms" in filename:
            
            vendorName = re.search(r'vendor/(.*?)/', onlySpaces).group(1)
            
            terms = cleanHTML(re.search(r'<h4>Terms & Conditions</h4>(.*?)</div>', onlySpaces).group(1))
            if (terms == "  "):
                terms = 'N/A'
            
            structuredDataVendorTerms = structuredDataVendorTerms.append({columnsVendorTerms[0]: vendorName, columnsVendorTerms[1]: terms}, ignore_index = True)
            
        elif "vendor" in filename and "pgp" in filename:
            
            vendorName = re.search(r'vendor/(.*?)/', onlySpaces).group(1)
            
            pgp = cleanHTML(re.search(r'<h4>Vendor Public PGP Key</h4>(.*?)</div>', onlySpaces).group(1))
            
            structuredDataVendorPGP = structuredDataVendorPGP.append({columnsVendorPGP[0]: vendorName, columnsVendorPGP[1]: pgp}, ignore_index = True)
            
        elif "vendor" in filename:
            
            vendorName = re.search(r'vendor/(.*?)/', onlySpaces).group(1)
            
            profile = cleanHTML(re.search(r'<h4>Vendor Profile</h4>(.*?)</div>', onlySpaces).group(1))
            if (profile == "  "):
                profile = 'N/A'
            
            trusted = re.search(r'Trusted Vendor', onlySpaces)
            if trusted:
                trusted = 'Yes'
            else:
                trusted = 'No'

            level = re.search(r'Level (.*?)<', onlySpaces).group(1)
            
            feedbackPos = re.search(r'fa fa-thumbs-o-up.*?px;">(.*?)<', onlySpaces).group(1)
            feedbackPos = int(re.sub(r',','',feedbackPos))
            
            feedbackNeu = re.search(r'fa fa-circle-o.*?px;">(.*?)<', onlySpaces).group(1)
            feedbackNeu = int(re.sub(r',','',feedbackNeu))
            
            feedbackNeg = re.search(r'fa fa-thumbs-o-down.*?px;">(.*?)<', onlySpaces).group(1)
            feedbackNeg = int(re.sub(r',','',feedbackNeg))
            
            regDate = re.search(r'Vendor since - (.*?)&', onlySpaces)
            if regDate:
                regDate = regDate.group(1)
            else:
                regDate = 'N/A'

            numSubscribers = re.search(r'fa-feed.*?nbsp; (.*?)(?= Sub)', onlySpaces)
            if numSubscribers.group(1):
                numSubscribers = numSubscribers.group(1)
            else:
                numSubscribers = 'N/A'
            
            numOrders = re.search(r'<h3>Orders</h3> <p><.*?>(.*?)<', onlySpaces)
            if numOrders:
                numOrders = numOrders.group(1)
            else:
                numOrders = 'N/A'
            
            avgVolUSD = re.search(r'fa-btc.*?\(USD (.*?)\)', onlySpaces)
            if avgVolUSD:
                avgVolUSD = avgVolUSD.group(1)
                avgVolUSD = float(re.sub(r',','',avgVolUSD))
            else:
                avgVolUSD = 'N/A'
            
            avgVolBTC = re.search(r'fa-btc.*?i> (.*?)<', onlySpaces)
            if avgVolBTC:
                avgVolBTC = avgVolBTC.group(1)
                avgVolBTC = float(re.sub(r',','',avgVolBTC))
            else:
                avgVolBTC = 'N/A'
            
            date = re.search(r'<tr><td>Date: (.*?)</td>', onlySpaces).group(1)
            
            url = "http://hansamkt2rr6nfg3.onion/vendor/" + vendorName
            
            structuredDataVendorProfile = structuredDataVendorProfile.append({columnsVendorProfile[0]: vendorName, columnsVendorProfile[1]: profile, columnsVendorProfile[2]: trusted, columnsVendorProfile[3]: level, columnsVendorProfile[4]: feedbackPos, columnsVendorProfile[5]: feedbackNeu, columnsVendorProfile[6]: feedbackNeg, columnsVendorProfile[7]: regDate, columnsVendorProfile[8]: numSubscribers, columnsVendorProfile[9]: numOrders, columnsVendorProfile[10]: avgVolUSD, columnsVendorProfile[11]: avgVolBTC, columnsVendorProfile[12]: date, columnsVendorProfile[13]: url}, ignore_index = True)
            
        elif "category" in filename:
            
            listingIDList = re.findall(r'(?<=ng/)(.*?)(?=/\" class=\"btn btn-red-0)', raw)
            
            viewsList = re.findall(r'Views: (.*?)</small>', onlySpaces)
            
            date = re.search(r'Date: (.*?)</td>', onlySpaces).group(1)
            
            # SUPER makeshift. May be very inefficient way to do this. 
            if (len(listingIDList) == len(viewsList)):
                for i in range (0, len(listingIDList)):
                    structuredDataViews = structuredDataViews.append({columnsViews[0]: listingIDList[i], columnsViews[1]: viewsList[i], columnsViews[2]: date}, ignore_index = True)
            else:
                structuredDataError = structuredDataError.append({columnsError[0]: 'Views', columnsError[1]: 'N/A', columnsError[2]: fileName}, ignore_index = True)
            
        elif "feedback" in filename:
            
            listingID = re.search(r'<form action=\"/listing/(.*?)/\" method=\"post\">', onlySpaces).group(1)
            
            addressLabel = re.search(r'Address label</p> <p>(.*?)</p>',onlySpaces)
            if addressLabel:
                addressLabel = addressLabel.group(1)
            else:
                addressLabel = 'N/A'
            
            envelopeType = re.search(r'Type of envelope</p> <p>(.*?)</p>',onlySpaces)
            if envelopeType:
                envelopeType = envelopeType.group(1)
            else:
                envelopeType = 'N/A'

            vacHeat = re.search(r'Vacuum packed or heat sealed</p> <p>(.*?)</p>',onlySpaces)
            if vacHeat:
                vacHeat = vacHeat.group(1)
            else:
                vacHeat = 'N/A'
            
            layersMylar = re.search(r'Avg. layers of mylar</p> <p>(.*?)</p>',onlySpaces)
            if layersMylar:
                layersMylar = layersMylar.group(1)
            else:
                layersMylar = 'N/A'
            
            barrier = re.search(r'Barrier</p> <p>(.*?)</p>',onlySpaces)
            if barrier:
                barrier = barrier.group(1)
            else:
                barrier = 'N/A'
            
            decoyItem = re.search(r'Decoy item</p> <p>(.*?)</p>',onlySpaces)
            if decoyItem:
                decoyItem = decoyItem.group(1)
            else:
                decoyItem = 'N/A'
            
            returnAddress = re.search(r'Return address</p> <p>(.*?)</p>',onlySpaces)
            if returnAddress:
                returnAddress = returnAddress.group(1)
            else:
                returnAddress = 'N/A'
        
            date = re.search(r'Date: (.*?)</td>', onlySpaces).group(1)
            
            thumbsUpDownList = re.findall(r'fa-thumbs-o-(.*?)  ">', raw)
            
            feedbackTextList = re.findall(r'<td><p>(.*?)</p></td>', onlySpaces)
            for i in range (0, len(feedbackTextList)):
                feedbackTextList[i] = cleanHTML(feedbackTextList[i])
                if (feedbackTextList[i] == "---"):
                    feedbackTextList[i] = 'N/A'
            
            deliveryTimeList = re.findall(r'</p></td> <td>(.*?)</td>', onlySpaces)
            for i in range (0, len(deliveryTimeList)):
                deliveryTimeList[i] = cleanHTML(deliveryTimeList[i])
            
            # SUPER STRUGGLE. MAY BE A BETTER WAT TO GRAB REVIEWER NAME
            reviewerListBeg = re.findall(r'<td>(.*?)(?=\*\*\*)', raw)
            reviewerListEnd = re.findall(r'(?<=\*\*\*)(.*?)<', raw)
            reviewerList = []
            if (len(reviewerListBeg) == len(reviewerListEnd)):
                for i in range(0, len(reviewerListBeg)):
                    reviewerList.append(reviewerListBeg[i] + "***" + reviewerListEnd[i])
            
            # ONLY WORKS FOR 83 MORE YEARS. NEED A BETTER WAY.
            feedbackDateList = re.findall(r'(?<=d>20)(.*?)(?=UTC</td> )', onlySpaces)
            for i in range(0, len(feedbackDateList)):
                feedbackDateList[i] = "20" + feedbackDateList[i] + "UTC"
        
        ################################################################################################
        #Append values to dataframe
        ################################################################################################
        
            structuredDataPackageAttributes = structuredDataPackageAttributes.append({columnsPackageAttributes[0]: listingID, columnsPackageAttributes[1]: addressLabel, columnsPackageAttributes[2]: envelopeType, columnsPackageAttributes[3]: vacHeat, columnsPackageAttributes[4]: layersMylar, columnsPackageAttributes[5]: barrier, columnsPackageAttributes[6]: decoyItem, columnsPackageAttributes[7]: returnAddress, columnsPackageAttributes[8]: date}, ignore_index=True)
            
            if (len(thumbsUpDownList) == len(feedbackTextList) and len(thumbsUpDownList) == len(deliveryTimeList) and len(thumbsUpDownList) == len(reviewerList) and len(thumbsUpDownList) == len(feedbackDateList)):
                for i in range (0, len(thumbsUpDownList)):
                    structuredDataFeedback = structuredDataFeedback.append({columnsFeedback[0]: listingID, columnsFeedback[1]: thumbsUpDownList[i], columnsFeedback[2]: feedbackTextList[i], columnsFeedback[3]: deliveryTimeList[i], columnsFeedback[4]: reviewerList[i], columnsFeedback[5]: feedbackDateList[i]}, ignore_index = True)
            else:
                structuredDataError = structuredDataError.append({columnsError[0]: "Feedback", columnsError[1]: "N/A", columnsError[2]: fileName}, ignore_index = True)
            
        elif "terms" in filename:
            
            listingID = re.search(r'<form action=\"/listing/(.*?)/\" method=\"post\">', onlySpaces).group(1)
            
            terms = cleanHTML(re.search(r'</u></h3> (.*?)</div>', onlySpaces).group(1))
            if (terms == ""):
                terms = 'N/A'
            
            date = re.search(r'Date: (.*?)</td>', onlySpaces).group(1)
            
        ################################################################################################
        #Append values to dataframe
        ################################################################################################
        
            structuredDataTerms = structuredDataTerms.append({columnsTerms[0]: listingID, columnsTerms[1]: terms, columnsTerms[2]: date}, ignore_index = True)
        
        # Listing Files
        else:
            
            listingName = re.search(r'<h2.*?>(.*?)</h2>',onlySpaces).group(1)

            listingPriceUSD = re.search(r'<div.*?> <strong>(.*?)</strong>',onlySpaces).group(1)
            listingPriceUSD = re.sub(r',','',listingPriceUSD)
            listingPriceUSD = float(re.sub(r'USD\s', '', listingPriceUSD))
            
            listingPriceBTC = re.search(r'btc.?"></i>(.*?)</span>',onlySpaces).group(1)
            listingPriceBTC = float(re.sub(r',','',listingPriceBTC))

            vendorName = re.search(r'<td>Vendor</td> <td><a.*?>(.*?)</a>',onlySpaces).group(1)

            description = cleanHTML(re.search(r'<h3><u>Listing Details</u></h3>(.*)<footer>',onlySpaces).group(1))

            date = re.search(r'Date: (.*?)</td>', onlySpaces).group(1)

            categoryListName = re.findall(r'<.*?category.*?>(.*?)</a>', onlySpaces)
            categoryName = categoryListName[-1]
            
            categoryListID = re.findall(r'/category/(.*?)/', onlySpaces)
            categoryID = categoryListID[-1]
        
            delivery = re.search(r'<td>Class</td> <td>(.*?)</td>', onlySpaces).group(1)
            if delivery == 'Physical':
                shipsFrom = re.search(r'Ships From</td> <td>(.*?)</td>', onlySpaces).group(1)
                shipsTo = re.search(r'Ships To</td> <td>(.*?)</td>', onlySpaces).group(1)
            else:
                shipsFrom = 'N/A'
                shipsTo = 'N/A'

            listingID = re.search(r'<form action=\"/listing/(.*?)/\" method=\"post\">', onlySpaces).group(1)
            
            url = 'http://hansamkt2rr6nfg3.onion/listing/' + listingID
        
        ################################################################################################
        #Append values to dataframe
        ################################################################################################
            structuredDataListing = structuredDataListing.append({columnsListing[0]: listingID, columnsListing[1]: listingName, columnsListing[2]: categoryName, columnsListing[3]: categoryID, columnsListing[4]: listingPriceUSD, columnsListing[5]: listingPriceBTC, columnsListing[6]: vendorName, columnsListing[7]: description, columnsListing[8]: delivery, columnsListing[9]: shipsFrom, columnsListing[10]: shipsTo, columnsListing[11]: date, columnsListing[12]: url}, ignore_index=True) 

################################################################################################
#Convert dataframe to csv
################################################################################################

structuredDataListing.to_csv(os.getcwd()+r'\Structured Full Listing Data.csv', index=False)
structuredDataPackageAttributes.to_csv(os.getcwd()+r'\Structured Full Package Attributes Data.csv', index=False)
structuredDataTerms.to_csv(os.getcwd()+r'\Structured Full Terms Data.csv', index=False)
structuredDataViews.to_csv(os.getcwd()+r'\Structured Full Views Data.csv', index=False)
structuredDataFeedback.to_csv(os.getcwd()+r'\Structured Full Feedback Data.csv', index=False)
structuredDataVendorTerms.to_csv(os.getcwd()+r'\Structured Full Vendor Terms Data.csv', index=False)
structuredDataVendorPGP.to_csv(os.getcwd()+r'\Structured Full Vendor PGP Data.csv', index=False)
structuredDataVendorProfile.to_csv(os.getcwd()+r'\Structured Full Vendor Profile Data.csv', index=False)
structuredDataError.to_csv(os.getcwd()+r'\Structured Full Error Data.csv', index=False)