import smtplib
import requests
import datetime
import pytz
import re
import pandas as pd

class sMS:
    def __init__(self):
        pass
    def number_check(self,_number):
        _number=str(_number)
        if _number.isdigit() and len(_number)==10:
            return True
        raise Exception("The Number is Not Digit or Not Equal to 10")

    def check_time_sms(self,time):
        if time.hour>=10 and time.hour<22:
            return True
        raise Exception("The Time is Over")
        
    def sms_time(self,region):
        if region.lower()=='india':
            d=datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
            #print(d.today())
            return self.check_time_sms(d)
        elif region.lower()=='usa':
            d=datetime.datetime.now(pytz.timezone('US/Central'))
            return self.check_time_sms(d)
        else:
            raise Exception("The Region is different")

    def smsSent(self,number,message,region):
        try:
            if self.number_check(number):
                if self.sms_time(region):
                    if len(message)>1 and len(message)<=10:
                        print(message)
                        url = " https://api.txtbox.in/v1/sms/send"
                        payload = "mobile_number={}&sms_text={}&sender_id=market".format(number,message)
                        headers = {
                            'apiKey': "9f81fddf27be1aa3e73a0619392cbc0c",
                            'content-type': "application/x-www-form-urlencoded"
                        }
                        response = requests.request("POST", url, headers=headers, params=payload)
                        return response.reason
                    else:
                        raise Exception("Text Message Is Long")
        except Exception as e:
            return e


class eMail:
    def check(self,email):
        rg= r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if(re.fullmatch(rg, email)):
          return True
        raise Exception("Email id is not Valid")
    def email_sent(self,dest, message,setup_email,setup_password):
        try:
            if self.check(dest):
                s = smtplib.SMTP('smtp.gmail.com', 587)
                s.starttls()
                s.login(setup_email,setup_password)
                message = message
                s.sendmail(setup_email, dest, message)
                return "SuccessFull!"
                s.quit()
        except Exception as e:
            return e
    
    def sms_snnt(self,idd,message,number,region,setup_email,setup_password):
        t=sMS().smsSent(number,message,region)
        p=self.email_sent(idd,message,setup_email,setup_password)
        return t,p



######ITS for the Mail Setup because Smtp is used to get the setup of the account and due to security reason I am not Sharing the my account Details
setup_email=input()
setup_password=input()


if  __name__ == '__main__':
    try:
        df=pd.read_csv('Sample.csv')
        ee=eMail()
        ss=[]
        pp=[]
        duplicate_email=[]
        duplicate_number=[]
        for i in df.index:
            p=df['Schedule On'][i]
            add_date=''
            if len(p[6:])==2:
                add_date='20'
            d=datetime.datetime(int(add_date+p[6:]),int(p[3:5]),int(p[0:2]))
            a=datetime.datetime.today()
            if len(df['Schedule On'][i])==0 or abs(d-a).days==0:
                if df['Email'][i] not in duplicate_email and df['Phone'][i] not in duplicate_number:
                    duplicate_number.append(df['Phone'][i])
                    duplicate_email.append(df['Email'][i])
                    s,t=ee.sms_snnt(df['Email'][i],df['Message'][i],df['Phone'][i],df['Country'][i],setup_email,setup_password)
                else:
                    s="Duplicate"
                    t=s
            else:
                s="Date is not Correct/Message is schedule"
                t=s
            ss.append(s)
            pp.append(t)
        df['Email_is_output']=pp
        df['SMS_OUTPUT']=ss
        df.to_csv("output.csv")
            
    except Exception as e:
        print(e)

print("Output File is Created in the Same Folder")
        





  

    
    



