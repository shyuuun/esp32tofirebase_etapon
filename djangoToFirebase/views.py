from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from djangoToFirebase.models import SmartBin
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from .process import html_to_pdf
import pyrebase, json, pytz
from xhtml2pdf import pisa
from django.utils import timezone

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

        # json file will be converted into dictionary
        data = json.loads(request.body)
        print(data) # debug

        binName = data.get("binName")
        time = timezone.localtime().now().strftime('%I:%M%p')
        date = timezone.localtime().now().strftime('%B %d, %Y')

        print(time)
        print(date)


        if BIN1 == binName:
            battery1 = data.get("battery1")
            bin1Level = data.get("bin1")
            bin2Level = data.get("bin2")
            print("From:", binName)
            print("Battery1:", battery1)
            print("bin1Level:", bin1Level)
            print("Bin2Level:", bin2Level)

            database.child('ITECH').update({'battery1': battery1})

            smartBinobj = SmartBin(binName=BIN1,  battery=battery1, binLevel1=bin1Level, binLevel2=bin2Level)

            database.child('ITECH').update({'bin1': bin1Level})
            database.child('ITECH').update({'bin1Date': date})
            database.child('ITECH').update({'bin1Time': time})
            database.child('ITECH').update({'bin2': bin2Level})
            database.child('ITECH').update({'bin2Date': date})
            database.child('ITECH').update({'bin2Time': time})

            smartBinobj.save()
            print("Database Updated")

        elif BIN2 == binName:
            battery2 = data.get("battery2")
            bin3Level = data.get("bin3")
            bin4Level = data.get("bin4")

            smartBinobj = SmartBin(binName=BIN2, battery=battery2, binLevel1=bin3Level, binLevel2=bin4Level)

            print("From:", binName)
            print("Battery2:", battery2)
            print("bin3Level:", bin3Level)
            print("Bin4Level:", bin4Level)


            database.child('ITECH').update({'battery2': battery2})

            database.child('ITECH').update({'bin3': bin3Level})
            database.child('ITECH').update({'bin3Date': date})
            database.child('ITECH').update({'bin3Time': time})
            database.child('ITECH').update({'bin4': bin4Level})
            database.child('ITECH').update({'bin4Date': date})
            database.child('ITECH').update({'bin4Time': time})

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

            smartBinobj = SmartBin(binName=BIN3, battery=battery3, binLevel1=bin5Level, binLevel2=bin6Level)

            database.child('ITECH').update({'bin5': bin5Level})
            database.child('ITECH').update({'bin5Date': date})
            database.child('ITECH').update({'bin5Time': time})
            database.child('ITECH').update({'bin6': bin6Level})
            database.child('ITECH').update({'bin6Date': date})
            database.child('ITECH').update({'bin6Time': time})
    
            smartBinobj.save()
            print("Database Updated")

    msg = "Database Updated at:" + str(binName)
    return HttpResponse(request, msg)
