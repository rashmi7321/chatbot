import datetime
import re
from difflib import SequenceMatcher

import datefinder
from click import DateTime
from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
import requests
from flask import request
import json
import requests
app = Flask(__name__)
CORS(app)

from_date = None
from_year = None
to_year = None
from_dateString=None
to_dateString =None
def checkvaliddate(matches,matchdate,matchmonth):
    if matchdate or matchmonth:
        correctformat = False
        regex = r"(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})"
        datelist =[]
        if len(matches)==1:
            getdate1 = datefinder.find_dates(str(matches[0]))
            for date in getdate1:
                datelist.append(date)
        else:
            getdate1 = datefinder.find_dates(str(matches[0]))
            getdate2 = datefinder.find_dates(str(matches[1]))
            for date1 in getdate1:
                print(date1)
                datelist.append(date1)
            for date2 in getdate2:
                print(date2)
                datelist.append(date2)
            print(datelist)
        if len(matches)==1:
            if len(datelist) == 0:
                correctformat=False
            else:
                validdatenew=None
                validdate1 = re.finditer(regex, datelist[0].strftime("%d/%m/%Y"), re.MULTILINE)
                for matchNum, match in enumerate(validdate1, start=1):
                    validdatenew=match.group()
                    print(match.group())
                if validdatenew:
                    correctformat = True
        elif len(matches)>1:
            validdatenew1 =None
            validdatenew2=None
            if len(datelist)==0 or len(datelist)==1:
                correctformat=False
            else:
                validdate2 = re.finditer(regex, datelist[0].strftime("%d/%m/%Y"),re.MULTILINE)
                for matchNum, match in enumerate(validdate2, start=1):
                    validdatenew1 = match.group()
                    print(match.group())
                validdate3 = re.finditer(regex, datelist[1].strftime("%d/%m/%Y"), re.MULTILINE)
                for matchNum, match in enumerate(validdate3, start=1):
                    validdatenew2 = match.group()
                    print(match.group())
                if validdatenew1 and validdatenew2:
                    correctformat = True
    else:
        correctformat=True

    return correctformat

@app.route('/vaildatedate',methods=['POST'])
def processdata():
    dateresult = None
    datemonthresult=None
    datedata = []
    isvaliddate = False
    nodate = False
    incorrectdate = False
    usermessage = request.data
    json1_data = json.loads(usermessage)
    finalString = json1_data['key']
    finalString=re.sub('[^A-Za-z0-9-]+', ' ', finalString)
    months = ["jan", "january", "feb", "february", "march", "april", "apr", "may", "june", "july", "aug",
              "august", "september", "sep", "oct",
              "october", "nov", "november", "dec", "december"]
    monthsdict = {
        "jan": '01', "january": '01', "feb": '02', "february": '02', "march": '03', "mar": '03', "april": '04',
        "apr": '04',
        "may": '05', "june": '06',
        "july": '07', "aug": '08', "august": '08', "sep": '09', "september": '09', "oct": '10', "october": '10',
        "nov": '11', "november": '11',
        "dec": '12', "december": '12'
    }

    extract_Months = []
    extract_dates=[]
    extract_years = []
    now = datetime.datetime.now()
    current_year = now.year
    verifieddates =[]
    def similar(a, b):
        return SequenceMatcher(None, a, b).ratio()

    def search(values, searchFor):
        for k in values:
            if searchFor in k:
                return values[k]
        return None
    def monthManipulation(datedata):
        for i in range(len(datedata)):
            splitMsg = re.split(r'[` \-=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>?]', datedata[i])
            i = 0
            j = 0
            while i < len(splitMsg):
                j = 0
                while j < len(months):
                    if splitMsg[i][:1] == months[j][0][:1]:
                        result = similar(splitMsg[i], months[j])
                        if result >= 0.80:
                            monthkey = months[j]
                            monthvalue = search(monthsdict, monthkey)
                            extract_Months.append(monthvalue)
                            print("extract months" +str(extract_Months))
                    j = j + 1
                i = i + 1

    def dateyearManipulation(datedata):
        dates=[]
        for i in range(len(datedata)):
            for s in re.split(r'[` \-=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>?]', datedata[i]):
                if s.isdigit():
                    dates.append(str(int(s)))
        for i in range(len(dates)):
            if len(dates[i]) == 2 or len(dates[i])==1:
                extract_dates.append(dates[i])
                print(extract_dates)
            else:
                extract_years.append(dates[i])

    def dynamicdateFormatConstruction():
        from_month = ''
        to_month = ''
        to_date = ''
        if len(extract_Months) > 1:
            from_month = extract_Months[0]
            to_month = extract_Months[1]
        else:
            from_month = extract_Months[0]

        if len(extract_dates) > 1:
            from_date = extract_dates[0]
            to_date = extract_dates[1]
        else:
            from_date = extract_dates[0]
        if  len(extract_years)==0 and from_month and to_month == '' and from_date and to_date == '':
            from_dateString = str(from_date) + "-" + from_month + "-" + str(current_year)
            verifieddates.append(from_dateString)
        elif len(extract_years) == 0 and from_month and to_month and from_date and to_date:
            from_dateString = str(from_date) + "-" + from_month + "-" + str(current_year)
            to_dateString = str(to_date) + "-" + to_month + "-" + str(current_year)
            verifieddates.append(from_dateString)
            verifieddates.append(to_dateString)
        elif len(extract_years)==1 and from_month and to_month and from_date and to_date:
            from_dateString = str(from_date) + "-" + from_month + "-" + str(extract_years[0])
            to_dateString = str(to_date) + "-" + to_month + "-" + str(extract_years[0])
            verifieddates.append(from_dateString)
            verifieddates.append(to_dateString)
        elif len(extract_years) >1 and from_month and to_month and from_date and to_date:
            from_dateString = str(from_date) + "-" + from_month + "-" + str(extract_years[0])
            to_dateString = str(to_date) + "-" + to_month + "-" + str(extract_years[1])
            verifieddates.append(from_dateString)
            verifieddates.append(to_dateString)
        elif len(extract_years) ==1 and from_month and from_date and to_month=='' and to_date =='' :
            from_dateString = str(from_date) + "-" + from_month + "-" + str(extract_years[0])
            verifieddates.append(from_dateString)
        else:
            from_dateString = str(from_date) + "-" + from_month + "-" + str(current_year)
            verifieddates.append(from_dateString)
    matches = re.findall(
            '(\d{1,2}[-\ / ](\d{}|january|jan|february|feb|march|mar|april|apr|may|june|jun|july|jul|august|aug|september|sep|october|oct|november|Nov|december|dec)[-\ / ]\d{4})',
            finalString) or re.findall(
            '(\d{1,2}[-\ / ](\d{}|january|jan|february|feb|march|mar|april|apr|may|june|jun|july|jul|august|aug|september|sep|october|oct|november|nov|december|dec))',
            finalString) \
                  or re.findall(
            '((\d{}|january|jan|february|feb|march|mar|april|apr|may|june|jun|july|jul|august|aug|september|sep|october|oct|november|Nov|december|dec)[-\ / ]\d{1,2}[-\ / ]\d{4})',
            finalString) \
                  or re.findall(
            '((\d{}|january|jan|february|feb|march|mar|april|apr|may|june|jun|july|jul|august|aug|september|sep|october|oct|november|Nov|december|dec)[-\ / ]\d{1,2})',
            finalString) \
                  or re.findall('(\d{4}([ ./-])\d{2}([ ./-])\d{2})', finalString) or re.findall(
            '(\d{2}([ ./-])\d{2}([ ./-])\d{4})', finalString);
    matchdate = re.findall('(\d{1,2})', finalString)
    matchmonth = re.findall('(\d{}|january|jan|february|feb|march|mar|april|apr|may|june|jun|july|jul|august|aug|september|sep|october|oct|november|Nov|december|dec)',finalString)
    if matches:
        for match in matches:
            matches2 = re.search(
                '(\d{1,2}[-\ / ](\d{}|january|jan|february|feb|march|mar|april|apr|may|june|jun|july|jul|august|aug|september|sep|october|oct|november|Nov|december|dec)[-\ / ]\d{2,4})',
                str(match)) or re.search(
                '(\d{1,2}[-\ / ](\d{}|january|jan|february|feb|march|mar|april|apr|may|june|jun|july|jul|august|aug|september|sep|october|oct|november|nov|december|dec))',
                str(match)) \
                       or re.search(
                '((\d{}|january|jan|february|feb|march|mar|april|apr|may|june|jun|july|jul|august|aug|september|sep|october|oct|november|Nov|december|dec)[-\ / ]\d{1,2}[-\ / ]\d{1,4})',
                str(match)) \
                       or re.search(
                '((\d{}|january|jan|february|feb|march|mar|april|apr|may|june|jun|july|jul|august|aug|september|sep|october|oct|november|Nov|december|dec)[-\ / ]\d{1,2})',
                str(match))
            if(matches2):
                datedata.append(matches2.group())

    if datedata:
        monthManipulation(datedata)
        dateyearManipulation(datedata)
        dynamicdateFormatConstruction();
        result = checkvaliddate(verifieddates,matchdate,matchmonth)
        datemonthresult=result

    if matches and len(matchdate)==1 and len(matchmonth)==1:
        if datedata:
            if datemonthresult==True:
                isvaliddate = True
                nodate= False
            else:
                incorrectdate = True
        else:
                result = checkvaliddate(matches)
                dateresult=result
                if dateresult == True:
                    isvaliddate = True
                    nodate = False
                else:
                    incorrectdate = True
    elif matches and len(matchdate) == 2 and len(matchmonth) == 2:
        if datedata:
            if datemonthresult==True:
                isvaliddate = True
                nodate= False
            else:
                incorrectdate = True
        else:
                result = checkvaliddate(matches,matchdate,matchmonth)
                dateresult=result
                if dateresult == True:
                    isvaliddate = True
                    nodate = False
                else:
                    incorrectdate = True
    elif len(matches)==0 and len(matchdate)==0 and len(matchmonth)==0:
        if datedata:
            if datemonthresult==True:
                isvaliddate = True
                nodate= False
            else:
                incorrectdate = True
        else:
                result = checkvaliddate(matches,matchdate,matchmonth)
                dateresult=result
                if dateresult == True:
                    isvaliddate = True
                    nodate = False
                else:
                    incorrectdate = True
    elif matches and len(matchmonth) ==2 and len(matchdate)==2:
        if datedata:
            if datemonthresult==True:
                isvaliddate = True
                nodate= False
            else:
                incorrectdate = True
        else:
                result = checkvaliddate(matches,matchdate,matchmonth)
                dateresult=result
                if dateresult == True:
                    isvaliddate = True
                    nodate = False
                else:
                    incorrectdate = True
    elif matches and len(matchdate) == 1 and len(matchmonth) ==1:
        if datedata:
            if datemonthresult==True:
                isvaliddate = True
                nodate= False
            else:
                incorrectdate = True
        else:
                result = checkvaliddate(matches,matchdate,matchmonth)
                dateresult=result
                if dateresult == True:
                    isvaliddate = True
                    nodate = False
                else:
                    incorrectdate = True
    elif matches and len(matchdate)==6 and len(matchmonth)==2:
        if datedata:
            if datemonthresult==True:
                isvaliddate = True
                nodate= False
            else:
                incorrectdate = True
        else:
                result = checkvaliddate(matches,matchdate,matchmonth)
                dateresult=result
                if dateresult == True:
                    isvaliddate = True
                    nodate = False
                else:
                    incorrectdate = True
    elif matches and len(matchdate)==4 and len(matchmonth)==1:
        incorrectdate=True
    elif matches and len(matchdate)==4 or len(matchdate)==8:
        if datedata:
            if datemonthresult==True:
                isvaliddate = True
                nodate= False
            else:
                incorrectdate = True
        else:
                result = checkvaliddate(matches,matchdate,matchmonth)
                dateresult=result
                if dateresult == True:
                    isvaliddate = True
                    nodate = False
                else:
                    incorrectdate = True
    elif matches and len(matchdate)==3 and len(matchmonth)==1:
        if datedata:
            if datemonthresult==True:
                isvaliddate = True
                nodate= False
            else:
                incorrectdate = True
        else:
                result = checkvaliddate(matches,matchdate,matchmonth)
                dateresult=result
                if dateresult == True:
                    isvaliddate = True
                    nodate = False
                else:
                    incorrectdate = True
    elif len(matchdate)==1 and len(matchmonth)==2:
        incorrectdate = True
    elif len(matchdate)==2 and len(matchmonth)==1:
        incorrectdate = True
    elif len(matchdate)==0 and len(matchmonth)==2:
        incorrectdate = True
    elif len(matchdate)==2 and len(matchmonth)==0:
        incorrectdate = True
    elif len(matchdate)==1 and len(matchmonth)==0:
        incorrectdate = True
    elif len(matchdate)==0 and len(matchmonth)==1:
        incorrectdate = True
    else:
        incorrectdate = True

    print(isvaliddate)
    print(nodate)
    print(incorrectdate)
    data = {"isvaliddate":isvaliddate,"nodate":nodate,"incorrectdate":incorrectdate,"finalString":finalString}
    print(finalString)
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8081,debug = True)
    app.config['JSON_SORT_KEYS'] = False