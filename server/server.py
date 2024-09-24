from flask import Flask, jsonify, request, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

groups = []
students = []

@app.route('/api/groups', methods=['GET'])
def get_groups():
    """
    Route to get all groups
    return: Array of group objects
    """
    # TODO: (sample response below)
    return jsonify(groups)

@app.route('/api/students', methods=['GET'])
def get_students():
    """
    Route to get all students
    return: Array of student objects
    """
    # TODO: (sample response below)

    return jsonify(students)

@app.route('/api/groups', methods=['POST'])
def create_group():
    """
    Route to add a new group
    param groupName: The name of the group (from request body)
    param members: Array of member names (from request body)
    return: The created group object
    """
    
    # Getting the request body (DO NOT MODIFY)
    group_data = request.json
    group_name = group_data.get("groupName")
    group_members = group_data.get("members")
    
    # TODO: implement storage of a new group and return their info (sample response below)


    # Get next id
    if not groups:
        new_group_id = 0
    else:
        new_group_id = max(group['id'] for group in groups) + 1

    for member_name in group_members:
        if not students:
            new_student_id = 0
        elif not student_name_exists(member_name):
            new_student_id = max(student['id'] for student in students) + 1
        else:
            continue
        students.append({
            "id": new_student_id,
            "name": member_name,
        })

    new_group = {
        "id": new_group_id,
        "groupName": group_name,
        "members": group_members,
    }

    print(new_group)
    groups.append(new_group)
    return jsonify(new_group), 201

def student_name_exists(student_name):
    for student in students:
        if student["name"] == student_name:
            return True
    return False

@app.route('/api/groups/<int:group_id>', methods=['DELETE'])
def delete_group(group_id):
    """
    Route to delete a group by ID
    param group_id: The ID of the group to delete
    return: Empty response with status code 204
    """
    # TODO: (delete the group with the specified id)

    # Get index of group to delete
    index = 0
    for group in groups:
        if group["id"] == group_id:
            break
        index = index + 1
    
    del groups[index]

    return '', 204  # Return 204 (do not modify this line)


def get_student_id(student_name):
    for student in students:
        if student["name"] == student_name:
            return student["id"]
    return "Unknown Student"

@app.route('/api/groups/<int:group_id>', methods=['GET'])
def get_group(group_id):
    """
    Route to get a group by ID (for fetching group members)
    param group_id: The ID of the group to retrieve
    return: The group object with member details
    """
    # TODO: (sample response below)

    print(students)
    for group in groups:
        if group["id"] == group_id:
            group_members = []
            for member_name in group["members"]:
                group_members.append({
                    "id": get_student_id(member_name),
                    "name": member_name
                })
            print(group_members)
            return jsonify({
                "id": group_id,
                "groupName": group["groupName"],
                "members": group_members,
            })
    abort(404, "Group not found")
    # TODO:
    # if group id isn't valid:
    #     abort(404, "Group not found")

if __name__ == '__main__':
    app.run(port=3902, debug=True)

    # Edge case is when you are creating a group with an already existing member then add
