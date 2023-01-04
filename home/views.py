from django.http import HttpResponse
from django.shortcuts import render,redirect
import requests

import urllib.parse
# Create your views here.
def home(request):
    if 'username' in request.session:
        return render(request,'home.html')
    else:
        return redirect(login)
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        url = "https://10.0.201.30:8006/api2/json/access/ticket"
        headers = {"content-Type": "application/x-www-form-urlencoded"}
        response1 = requests.post(url, headers=headers, data=f"username={username}&password={password}", verify=False)
        if response1.status_code == 200:
            response_json = response1.json()
            username= response_json['data']['username']
            ticket = response_json['data']['ticket']
            csrf = response_json['data']['CSRFPreventionToken']

            url2 = "https://10.0.201.30:8006/api2/json/nodes"
            headers2 = {"CSRFPreventionToken": csrf, "Cookie": "PVEAuthCookie="+ticket}
            response2 = requests.get(url2,headers=headers2,verify=False)
            response_json = response2.json()
            nodes = response_json['data']
            for i in nodes:
                node=i
                break
            node = node['node']

            request.session['username'] = username
            request.session['ticket'] = ticket
            request.session['csrf'] = csrf
            request.session['nodes'] = nodes
            request.session['node'] = node

            response = redirect('cloudservers')
            return response
        else:
            return redirect('login')
    else:
        if 'username' in request.session:
            return redirect('cloudservers')
        else:
            return render(request,'login.html')


def logout(request):
    sessions = request.session
    sessions.delete()
    response = redirect(login)
    response.delete_cookie('PVEAuthCookie')
    return response

def fun(request):
    ticket = request.session['ticket']
    context={
            'ticket':ticket
        }
    return render(request,'fun.html',context)

def cloudservers(request):
    if 'username' in request.session:
        csrf = request.session['csrf']
        ticket = request.session['ticket']
        node = request.session['node']
    
        url = f"https://10.0.201.30:8006/api2/json/nodes/{node}/qemu/"
        headers = {"CSRFPreventionToken": csrf, "Cookie": "PVEAuthCookie="+ticket}
        response = requests.get(url,headers=headers, verify=False)
        response_json = response.json()

        vms = response_json['data']
        request.session['vms'] = vms
        context={
            'ticket':ticket
        }
        
        response = render(request,'dashboard.html',context)
        return response
    else:
        return redirect('login')

def console(request,name):
    ticket = request.session['ticket']
    vms = request.session['vms']
    print(vms)
    print(name)
    for vm in vms:
        print(vm['name'])
        if vm['name'] == name:
            vm = vm
    vmid = vm['vmid']
    name = vm['name']
    node = request.session['node']
    url = 'https://server.prom.cd:8006/?console=kvm&novnc=1&vmid=' + str(vmid)+ '&vmname='+ str(name)+'&node='+ node + '&resize=off&cmd='
    ticket = request.session['ticket']
    context={
            'ticket':ticket
        }
    response = render(request,'console.html',context)
    
    ticket = urllib.parse.quote(ticket, safe='')
    response.set_cookie('PVEAuthCookie',ticket,domain='.prom.cd',samesite=None,secure=True)
    return response

def summary(request,name):
    ticket = request.session['ticket']
    vms = request.session['vms']
    for vm in vms:
        if vm['name'] == name:
            vm = vm
    context={
            'ticket':ticket,
            'vm':vm
        }
    response = render(request,'summary.html',context)
    return response

def snapshots(request,name):
    pass

def backup(request,name):
    pass