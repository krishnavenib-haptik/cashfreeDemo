from django.shortcuts import render
import hashlib
import hmac
import base64


def request(request):
    print("@@@@@@@@@@@@@@@@@",request.POST)
    postData = {
      "appId" : '7299599073f7263c184054fb859927',
      "orderId" : request.POST['orderId'],
      "orderAmount" : request.POST['orderAmount'],
      "orderCurrency" : request.POST['orderCurrency'],
      "orderNote" : request.POST['orderNote'],
      "customerName" : request.POST['customerName'],
      "customerPhone" : request.POST['customerPhone'],
      "customerEmail" : request.POST['customerEmail'],
      "returnUrl": 'http://85a8640a42b7.ngrok.io/payment/processed',
      "notifyUrl": 'http://85a8640a42b7.ngrok.io/payment/processed'
    }

    sig = generate_signature(postData)
    print(sig)
    return render(request, 'payment/request.html', context={'sig': sig, 'postData': postData})

def index(request):
    return render(request, 'payment/index.html')

def processed(request):
    print("##############processed",request.POST)
    postData = {
        "orderId": request.POST['orderId'],
        "orderAmount": request.POST['orderAmount'],
        "referenceId": request.POST['referenceId'],
        "txStatus": request.POST['txStatus'],
        "paymentMode": request.POST['paymentMode'],
        "txMsg": request.POST['txMsg'],
        "signature": request.POST['signature'],
        "txTime": request.POST['txTime']
    }

    signatureData = ""
    secretKey = "784d80d584cb823382c18b88699a2947bdcca445"
    signatureData = postData['orderId'] + postData['orderAmount'] + postData['referenceId'] + postData['txStatus'] + \
                    postData['paymentMode'] + postData['txMsg'] + postData['txTime']

    message = signatureData.encode('utf-8')
    # get secret key from your config
    secret = secretKey.encode('utf-8')
    computedsignature = base64.b64encode(hmac.new(secret, message, digestmod=hashlib.sha256).digest()).decode('utf-8')
    print("computedsignature", computedsignature)
    print(request.POST['signature'])
    return render(request, 'payment/process.html', context={'computedsignature': computedsignature, 'postData': postData})


def generate_signature(postData):

    secretKey = "784d80d584cb823382c18b88699a2947bdcca445"
    sortedKeys = sorted(postData)
    signatureData = ""
    for key in sortedKeys:
        signatureData += key+postData[key]
    message = signatureData.encode('utf-8')
    #get secret key from your config
    secret = secretKey.encode('utf-8')
    signature = base64.b64encode(hmac.new(secret,message,digestmod=hashlib.sha256).digest()).decode("utf-8")
    return signature
