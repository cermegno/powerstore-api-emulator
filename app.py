#/usr/bin/python3
import os, json, re
from flask import Flask, jsonify, request, abort, render_template, redirect, url_for, make_response
from random import randrange
import copy
from operator import itemgetter
from data import *

debug = 0

app = Flask(__name__)

def get_random_id():
    ### Generate random Id. We don't double check for colisions

    id = randrange(1000000)
    if debug: print(id)
    return "19894d22-87e1-4fef-9a04-5f120" + str(id).zfill(7)

def get_one(in_list, search_key, search_value):
    ### Searches a list of dict for an item that matches a key and a value
    ### Ex: get_one(hosts, "name", "demo01") 
    
    requested_item = {}
    for each_item in in_list:
        if each_item[search_key] == search_value:
            requested_item = dict(each_item)
            break
    return requested_item

def filter_select(in_list, select):
    ### Returns a list that contains only the keys requested

    if not in_list:
        return in_list #If the list is empty go back
    if not select: # If select is not specified the API returns only 'id'
        select_keys = ["id"]
        if debug: print("Select is     :", select)
    else:
        if debug: print(select)
        if "," in select:
            select_keys = select.split(",")
        elif "%2C" in select:
            select_keys = select.split("%2C")
        else: #There must be a single item in select
            select_keys = [select]
            
    if debug: print("Keys in template  :", in_list[0].keys())
    out_keys = list(set(in_list[0].keys()) - set(select_keys))
    if debug: print("Keys to remove    :", out_keys)
    for each_item in in_list:
        for each_key in out_keys:
            each_item.pop(each_key,None)
    return in_list

def sort_output(in_list, order_param):
    ### Returns a sorted list

    sort_key, sort_order = order_param.split(".")
    reverse = False
    if sort_order == "desc": reverse = True
    in_list = sorted(in_list, key=itemgetter(sort_key), reverse=reverse)

    return in_list

def get_matches(in_list, all_params):
    ### Returns list with items that match criteria
    ### It will only match one parameter if multiple are provided
    ### Only "eq." operator is matched

    valid_params = all_params.to_dict()
    valid_params.pop('select', None)
    valid_params.pop('order', None)
    if not valid_params: # If select and order were the only parameters return everything
        return in_list
    if debug: print("Params to match: ",valid_params)

    first_param = list(valid_params.keys())[0] # We are going to match only the first param we find
    if first_param not in in_list[0].keys():
        return "Parameter '" + first_param + "' not found"
    if debug: print(valid_params)
    operator, criteria = valid_params[first_param].split(".")
    if operator != "eq":
        return "Operator '" + operator + "' not supported"
    
    if debug: print("Let's find records with " + first_param + " = " + criteria)
    matched_records = []
    for record in in_list:
        if record[first_param] == criteria:
            matched_records.append(record)
    if debug: print(matched_records)
    if not matched_records:
        return matched_records

    return matched_records

@app.route('/api/rest/cluster', methods=['GET'])
def get_cluster():
    ### GET all cluster details. Returns Token

    select = request.args.get('select')
    out_cluster = copy.deepcopy(cluster)
    out_cluster = filter_select(out_cluster, select)
    response = make_response(jsonify(out_cluster))
    response.headers["DELL-EMC-TOKEN"] = "yXc92rvwX2DT8khX3Im786KfFCPCVjLecegBMidGZ6A="
    return response, 200

@app.route('/api/rest/event', methods=['GET'])
def get_event():
    ### GET all cluster details. Returns Token

    out_event = copy.deepcopy(events)

    matched_records = get_matches(out_event, request.args)
    if isinstance(matched_records, str):
        return jsonify({"ERROR" : matched_records}), 422 
    out_event = filter_select(matched_records, request.args.get('select'))
    if 'order' in request.args:
        out_event = sort_output(out_event, request.args.get('order'))

    response = make_response(jsonify(out_event))
    response.headers["DELL-EMC-TOKEN"] = "yXc92rvwX2DT8khX3Im786KfFCPCVjLecegBMidGZ6A="
    return response, 200

@app.route('/api/rest/host', methods=['GET'])
def get_host():
    ### GET all existing hosts or a host matching the name parameter

    all_hosts = copy.deepcopy(hosts)

    matched_records = get_matches(all_hosts, request.args)
    if isinstance(matched_records, str):
        return jsonify({"ERROR" : matched_records}), 422 
    out_hosts = filter_select(matched_records, request.args.get('select'))
    if 'order' in request.args:
        out_hosts = sort_output(out_hosts, request.args.get('order'))

    response = make_response(jsonify(out_hosts))
    response.headers["DELL-EMC-TOKEN"] = "yXc92rvwX2DT8khX3Im786KfFCPCVjLecegBMidGZ6A="
    return response, 200

@app.route('/api/rest/host/<string:host_id>', methods=['GET'])
def get_single_host(host_id):
    ### GET details of one host

    requested_host = get_one(hosts, "id", host_id)
    if requested_host:
        select = request.args.get('select')
        requested_host = filter_select([requested_host], select)
        return jsonify(requested_host[0]), 200 # This function returns a dict instead of a list but id's are unique
    else:
        return jsonify({"ERROR": "Error: host " + str(host_id) + " not found"}), 404

@app.route('/api/rest/host', methods=['POST'])
def post_host():
    ### Create new host
    ### TO DO: Validate that all mandatory parameters are present
    
    if debug: print(str(request.json))
    global hosts
    if get_one(hosts, "name", request.json["name"]):
            return jsonify({"ERROR": "Operation failed - host already exist"}), 422

    new_host = request.json
    new_id = get_random_id()
    new_host["id"] = new_id
    ### GET  /host provides host_initiators but
    ### POST /host requires initiators
    new_host["host_initiators"] = new_host["initiators"]
    new_host.pop('initiators', None)
    new_host["os_type_l10n"] = new_host["os_type"]
    new_host["host_group_id"] = None
    if 'description' not in request.json:
        new_host["description"] = ""
    hosts.append(new_host)

    return jsonify({"id": new_id}), 201

@app.route('/api/rest/host/<string:host_id>', methods=['DELETE'])
def delete_host(host_id):
    ### Delete host

    if debug: print("Deleting host :",host_id)
    global hosts
    for i in range(len(hosts)):
        if hosts[i]['id'] == host_id:
            del hosts[i]
            break    
    if debug: print("Resulting volume list :",volumes)

    return ("", 204)

@app.route('/api/rest/volume', methods=['GET'])
def get_volume():
    ### GET all existing hosts or a host matching the name parameter

    select = request.args.get('select')
    select = re.sub('\(.*?\)', '', select) #Removing any specific parameters between brackets

    all_volumes = copy.deepcopy(volumes)

    matched_records = get_matches(all_volumes, request.args)
    if isinstance(matched_records, str):
        return jsonify({"ERROR" : matched_records}), 422 
    out_volumes = filter_select(matched_records, select)
    if 'order' in request.args:
        out_volumes = sort_output(out_volumes, request.args.get('order'))

    response = make_response(jsonify(out_volumes))
    response.headers["DELL-EMC-TOKEN"] = "yXc92rvwX2DT8khX3Im786KfFCPCVjLecegBMidGZ369"
    return response, 200

@app.route('/api/rest/volume/<string:vol_id>', methods=['GET'])
def get_single_volume(vol_id):
    ### GET details of one volume

    requested_volume = get_one(volumes, "id", vol_id) 
    if requested_volume:
        select = request.args.get('select')
        requested_volume = filter_select([requested_volume], select)
        return jsonify(requested_volume[0]), 200 # This function returns a dict instead of a list
    else:
        return jsonify({"ERROR": "Error: host " + str(vol_id) + " not found"}), 404

@app.route('/api/rest/volume', methods=['POST'])
def post_volume():
    ### Create new host
    ### TO DO: Validate that all mandatory parameters are present
    
    if debug: print(str(request.json))
    global volumes    
    if get_one(volumes, "name", request.json["name"]):
            return jsonify({"ERROR": "Operation failed - volume already exist"}), 422

    new_volume = request.json
    new_id = get_random_id()
    new_volume["id"] = new_id
    if 'description' not in request.json:
        new_volume["description"] = ""
    new_volume["host"] = []
    new_volume["host_group"] = []
    new_volume["volume_groups"] = []
    new_volume["type"] = "Primary"
    wwn = "naa.68ccf098005a587ca54d2fc0baba" + str(randrange(1000)).zfill(4)
    new_volume["wwn"] = wwn
    new_volume["appliance_id"] = "A1"
    new_volume["state"] = "Ready"
    new_volume["protection_policy_id"] = None
    new_volume["performance_policy_id"] = None
    #new_volume["is_replication_destination"] = False
    #new_volume["creation_timestamp"] = "2021-05-05T09:32:10.60977+00:00"
    #new_volume["migration_session_id"] = None
    #new_volume["protection_data"] = {}
    volumes.append(new_volume)

    return jsonify({"id": new_id}), 201

@app.route('/api/rest/volume/<string:vol_id>', methods=['PATCH'])
def patch_volume(vol_id):
    ### Modify volume

    if debug: print(str(request.json))
    if debug: print("Modifying volume :",vol_id)
    global volumes
    for i in range(len(volumes)):
        if volumes[i]['id'] == vol_id:
            for each_key in request.json:
                volumes[i][each_key] = request.json[each_key]

    if debug: print("Resulting volume list :",volumes)

    return ("", 204)

@app.route('/api/rest/volume/<string:vol_id>', methods=['DELETE'])
def delete_volume(vol_id):
    ### Delete volume

    if debug: print("Deleting volume :",vol_id)
    global volumes
    for i in range(len(volumes)):
        if volumes[i]['id'] == vol_id:
            del volumes[i]
            break    
    if debug: print("Resulting volume list :",volumes)

    return ("", 204)

@app.route('/api/rest/volume/<string:vol_id>/attach', methods=['POST'])
def attach_volume(vol_id):
    ### GET details of one volume

    if debug: print(str(request.json))
    global mappings
    global volumes

    ### I need to check if there is already a mapping for this vol_id to the host_id
    mapping_id = ""
    for each_mapping in mappings:
        if each_mapping["volume_id"] == vol_id and each_mapping["host_id"] == request.json["host_id"]:
            mapping_id = each_mapping["id"]
            break
    if debug: print(mapping_id)
    if mapping_id == "":
        new_id = get_random_id()
        new_mapping = {}
        new_mapping["id"] = new_id
        new_mapping["volume_id"] = vol_id
        new_mapping["host_id"] = request.json["host_id"]
        new_mapping["logical_unit_number"] = 1
        new_mapping["host_group_id"] = None
        mappings.append(new_mapping)
        
        new_host = {"id": request.json["host_id"]}
        name = get_one(hosts, "id", request.json["host_id"])["name"]
        new_host["name"] = name
        for each_vol in volumes:
            if each_vol["id"] == vol_id:
                each_vol["host"].append(new_host)
                break
        
    return ("", 204)

@app.route('/api/rest/host_volume_mapping', methods=['GET'])
def get_host_volume_mapping():
    ### Retrieve volume mappings

    select = request.args.get('select')
    all_mappings = copy.deepcopy(mappings)

    matched_records = get_matches(all_mappings, request.args)
    if isinstance(matched_records, str):
        return jsonify({"ERROR" : matched_records}), 422 
    out_mappings = filter_select(matched_records, select)
    if 'order' in request.args:
        out_mappings = sort_output(out_mappings, request.args.get('order'))

    response = make_response(jsonify(out_mappings))
    response.headers["DELL-EMC-TOKEN"] = "yXc92rvwX2DT8khX3Im786KfFCPCVjLecegBMidGZ369"
    return response, 200

if __name__ == "__main__":
	app.run(debug=False, host='0.0.0.0', port=int(os.getenv('PORT', '443')), threaded=True, ssl_context='adhoc')
