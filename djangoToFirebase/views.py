from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from djangoToFirebase.models import SmartBin
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from .process import html_to_pdf
import pyrebase, json, pytz
from xhtml2pdf import pisa
from datetime import datetime

config={
  "apiKey": "AIzaSyB_1yoKFusZpfCpXIaDRNfWQ1rAhEoqzE4",
  "authDomain": "e-tapon-9cefd.firebaseapp.com",
  "databaseURL": "https://e-tapon-9cefd-default-rtdb.asia-southeast1.firebasedatabase.app",
  "storageBucket": "e-tapon-9cefd.appspot.com"

}
firebase=pyrebase.initialize_app(config)
authe = firebase.auth()
database=firebase.database()



BIN1 = "Cloudbin_ITECH1"
BIN2 = "Cloudbin_ITECH2"
BIN3 = "Cloudbin_ITECH3"

currentTimeZone = pytz.timezone('Asia/Hong_Kong')
timeInPH = datetime.now(currentTimeZone)
currentDatePH = timeInPH.strftime('%d-%m-%y')
currentTimePH = timeInPH.strftime("%H:%M:%S")

print("time from pytz:", currentTimeZone)
print("time in the ph", currentTimePH)

class ViewPdf(View):
    def get(self, request, *args, **kwargs):
        data = SmartBin.objects.all()
        pdf = html_to_pdf('report.html', {'data:': data})
        return HttpResponse(pdf, content_type='application/pdf')



def test(request):
    battery1 = database.child('ITECH').child('battery1').get().val()
    bin1 = database.child('ITECH').child('bin1').get().val()

    template = loader.get_template('test.html')
    context = {
        'battery1': battery1,
        'bin1': bin1
    }
    return HttpResponse(template.render(context, request))

def listview(request):
    data = SmartBin.objects.all();
    return HttpResponse(render(request, 'generate.html', {'data': data}))

def pdfCreate(request):
    data = SmartBin.objects.all();

    template_path = 'generate.html'

    context = {'data': data}

    response = HttpResponse(content_type='application/pdf')
    response['Content'] = 'filename="Etapon_Logs.pdf"'

    template = loader.get_template(template_path)

    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error')
    return response



@csrf_exempt
def updateToFirebase(request):
    if request.method == 'POST':

        current_date = timeInPH.strftime("%H-%M-%S")
        print("Current Date:", current_date)

        current_time = timeInPH.strftime("%H:%M")
        print("Current Time:", current_time)
        # json file will be converted into dictionary
        data = json.loads(request.body)
        print(data) # debug

        binName = data.get("binName")

        if BIN1 == binName:
            battery1 = data.get("battery1")
            bin1Level = data.get("bin1")
            bin2Level = data.get("bin2")

            print("From:", binName)
            print("Battery1:", battery1)
            print("bin1Level:", bin1Level)
            print("Bin2Level:", bin2Level)

            database.child('ITECH').update({'battery1': battery1})

            smartBinobj = SmartBin(binName=BIN1, binDate=current_date, binTime=current_time, battery=battery1, binLevel1=bin1Level, binLevel2=bin2Level)

            database.child('ITECH').update({'bin1': bin1Level})
            database.child('ITECH').update({'bin1Date': current_date})
            database.child('ITECH').update({'bin1Time': current_time})
            database.child('ITECH').update({'bin2': bin2Level})
            database.child('ITECH').update({'bin2Date': current_date})
            database.child('ITECH').update({'bin2Time': current_time})

            smartBinobj.save()
            print("Database Updated")

        elif BIN2 == binName:
            battery2 = data.get("battery2")
            bin3Level = data.get("bin3")
            bin4Level = data.get("bin4")

            smartBinobj = SmartBin(binName=BIN2, binDate=current_date, binTime=current_time, battery=battery2, binLevel1=bin3Level, binLevel2=bin4Level)

            print("From:", binName)
            print("Battery2:", battery2)
            print("bin3Level:", bin3Level)
            print("Bin4Level:", bin4Level)


            database.child('ITECH').update({'battery2': battery2})

            database.child('ITECH').update({'bin3': bin3Level})
            database.child('ITECH').update({'bin3Date': current_date})
            database.child('ITECH').update({'bin3Time': current_time})
            database.child('ITECH').update({'bin4': bin4Level})
            database.child('ITECH').update({'bin4Date': current_date})
            database.child('ITECH').update({'bin4Time': current_time})

            smartBinobj.save()
            print("Database Updated")

        elif BIN3 == binName: 
            battery3 = data.get("battery3")
            bin5Level = data.get("bin5")
            bin6Level = data.get("bin6")

            
            print("From:", binName)
            print("Battery3:", battery3)
            print("bin5Level:", bin5Level)
            print("Bin6Level:", bin6Level)


            database.child('ITECH').update({'battery3': battery3})

            smartBinobj = SmartBin(binName=BIN3, binDate=current_date, binTime=current_time, battery=battery3, binLevel1=bin5Level, binLevel2=bin6Level)

            database.child('ITECH').update({'bin5': bin5Level})
            database.child('ITECH').update({'bin5Date': current_date})
            database.child('ITECH').update({'bin5Time': current_time})
            database.child('ITECH').update({'bin6': bin6Level})
            database.child('ITECH').update({'bin6Date': current_date})
            database.child('ITECH').update({'bin6Time': current_time})
    
            smartBinobj.save()
            print("Database Updated")

    msg = "Database Updated at:" + str(binName)
    return HttpResponse(request, msg)
