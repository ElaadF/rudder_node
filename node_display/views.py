from django.shortcuts import render
from django.http import HttpResponse
import json
import requests

# Create your views here.
def index(request):
    context = {'navbar': 'All'}
    return render(request, 'node_display/index.html', context)

def get_accepted_node(request):
    try:
        nodes = get_nodes(request.session['url'], request.session['token'])
    except:
        return render(request, 'node_display/index.html', {"error" : error_message(request)})
    return render(request, 'node_display/index.html', {"nodes" : nodes, "navbar" : "accepted"})

def get_pending_node(request):
    try:
        nodes = get_nodes(request.session['url'], request.session['token'])
    except:
        return render(request, 'node_display/index.html', {"error" : error_message(request)})
    return render(request, 'node_display/index.html', {"nodes" : nodes, "navbar" : "pending"})

def get_nodes(url, token):
    params = {"include" : "minimal" }
    headers = { "X-API-TOKEN" : token }

    json_data_accepted = requests.get(url, params = params, headers = headers, verify = False)
    json_nodes_accepted = json.loads(json_data_accepted.text)

    json_data_pending = requests.get(url+"/pending", params = params, headers = headers, verify = False)
    json_nodes_pending= json.loads(json_data_pending.text)

    accepted_nodes = {}
    pending_nodes = {}

    for node in json_nodes_accepted["data"]["nodes"]:
        accepted_nodes[node["hostname"]] = node["id"]
    for node in json_nodes_pending["data"]["nodes"]:
        pending_nodes[node["hostname"]] = node["id"]

    return {"accepted_nodes" : accepted_nodes, "pending_nodes": pending_nodes}

def error_message(request):
    message = "Request have failed"
    if request.session['url'] == "" and request.session['token'] == "":
        message = "Empty URL and Token"
    elif request.session['url'] == "":
        message = "Empty URL"
    elif request.session['token'] == "":
        message = "Empty Token"
    return message

def get_all_node(request):
    try:
        nodes = get_nodes(request.session['url'], request.session['token'])
    except:
        return render(request, 'node_display/index.html', {"error" : error_message(request)})
    return render(request, 'node_display/index.html', {"nodes" : nodes, "navbar" : "all"})

def server_info_submit(request):
    url = request.POST.get('url', '')
    token = request.POST.get('token', '')
    context = {}
    request.session['url'] = url
    request.session['token'] = token
    request.session['accepted'] = "get_nodes(url, token)[]"
    request.session['pending'] = "titi"
    return render(request, 'node_display/index.html', {"infoserv" : context})

def properties(request, hostname, id):
    headers = { "X-API-TOKEN" : request.session['token'] }

    json_data = requests.get(request.session['url']+"/"+id, headers = headers, verify = False)
    json_node = json.loads(json_data.text)

    properties = {}

    for property_lst in json_node["data"]["nodes"]:
        for property in property_lst["properties"]:
            print(property)
            properties[property["name"]] = property["value"]

    return render(request, 'node_display/properties.html', {"properties" : properties, "hostname" : hostname, "id" : id})
