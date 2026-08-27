from flask import Flask, request, jsonify
from datetime import datetime
from apps.time.time_queries import (
    add_consultant, add_customer,
    find_consultant, add_time_entry, find_customer
)

app = Flask(__name__)

# add consultant 
@app.route("/consultants", methods=["POST"])
def create_consultant():

    # get the request and extract the data
    data = request.get_json()

    name = data["name"]
    email = data["email"]

    # check if consultant already exist
    consultant_id_exist = find_consultant(email)

    # if not - create customer, else return error
    if consultant_id_exist is None:
        consultant_id = add_consultant(name, email)
    else:
        return jsonify({
            'error': 'consultant already exists'
        }), 409

    # return consultant info
    return jsonify({
        "id": consultant_id,
        "name": name,
        "email": email
    }), 201


# add customer
@app.route("/customers", methods=["POST"])
def create_customer():

    # get the request and extract the data
    data = request.get_json()
    name = data["name"]

    # check if customer already exist
    customer_id_exist = find_customer(name)

    # if not - create customer, else return error
    if customer_id_exist is None:
        customer_id = add_customer(name)
    else:
        return jsonify({
            'error': 'customer already exists'
        }), 409

    # return customer info
    return jsonify({
        "id": customer_id,
        "name": name
    }), 201


# add time entrie
@app.route("/time-entries", methods=["POST"])
def create_time_entry():

    # get the request and extract the data
    data = request.get_json()

    
    email = data["email"]
    customer_name = data["customer_name"]
    start_time = datetime.fromisoformat(data["start_time"])
    end_time = datetime.fromisoformat(data["end_time"])
    lunch_break = data["lunch_break"]

    # Find consultant_id using the email
    consultant_id = find_consultant(email)

    # check if consultant exists
    if consultant_id is None:
        return jsonify({
            "error": "Consultant not found"
        }), 404
    

    #find customer id using name
    customer_id = find_customer(customer_name)

    # check if customer exists
    if customer_id is None:
        return jsonify({
                "error": "Customer not found"
            }), 404
        

    # Create time entry
    time_entry = add_time_entry(
        consultant_id,
        customer_id,
        start_time,
        end_time,
        lunch_break
    )

    # if creation fails
    if time_entry is None:
        return jsonify({
            "error": "Could not create time entry"
        }), 500

    # return info from created time entry
    return jsonify({
        "id": time_entry[0],
        "consultant_id": time_entry[1],
        "customer_id": time_entry[2]
    }), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
