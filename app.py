import os

from flask import Flask, request, send_from_directory, jsonify
import sqlite3

app = Flask(__name__)

# Custom route to serve image from the 'images' folder
@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory(os.path.join(os.getcwd(), 'images'), filename)

def get_url_path():
    return request.path

## HEADER
header = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>pythonFlaskProject</title>
        <style>
            body {
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
            }
            
            .main-container {
                flex: 1;
                overflow: auto;
            }
        
            #header,
            #footer {
                background-color: #2a2a2a;
                color: #fff;
                padding-top: 20px;
                padding-bottom: 20px;
            }
            
            .header-wrapper {
                display: flex;
                justify-content: space-between;
            }
            
            .logo {
                height: 40px;
                width: auto;
            }
            
            .links-wrapper {
                display: flex;
                align-items: center;
                gap: 15px;
            }
            
            .links-wrapper a {
                color: #fff;
                text-decoration: none;
            }
            
            .links-wrapper a:hover {
                color: #50C878;
            }
            
            p {
                text-align: center;
            }
        
            .container {
                width: 100%;
                padding-right: var(--bs-gutter-x, 1.5rem);
                padding-left: var(--bs-gutter-x, 1.5rem);
                margin-right: auto;
                margin-left: auto;
            }
            
            /* Media query breakpoints for fixed-width containers */
            @media (min-width: 576px) {
                .container {
                    max-width: 540px;
                }
            }
            
            @media (min-width: 768px) {
                .container {
                    max-width: 720px;
                }
            }
            
            @media (min-width: 992px) {
                .container {
                    max-width: 960px;
                }
            }
            
            @media (min-width: 1200px) {
                .container {
                    max-width: 1140px;
                }
            }
            
            @media (min-width: 1400px) {
                .container {
                    max-width: 1320px;
                }
            }
        
            h1 {
                text-align: center;
            }
        
            table {
                font-family: arial, sans-serif;
                border-collapse: collapse;
                width: 100%;
            }
            
            table th {
                background-color: #2a2a2a;
                color: #fff;
            }

            td, th {
                border: 1px solid #2a2a2a;
                text-align: center;
                padding: 8px;
            }

            tr:nth-child(odd) {
                background-color: rgba(80, 200, 120, 0.3);
            }
            
            .buttons {
                display: flex;
                gap: 15px;
            }
            
            .total-table th,
            .total-table td {
                background-color: #2a2a2a;
                color: #fff;
                text-align: center;
            }
            
            td a {
                width: 100%;
                text-align: center;
                background-color: #2a2a2a;
                color: #fff;
                text-decoration: none;
                padding: 10px;
                border-radius: 5px;
            }
            
            td a:hover {
                background-color: #50C878;
            }
            
            form {
                display: flex;
                flex-direction: column;
                gap: 10px;
            }
            
            form label {
                display: flex;
                flex-direction: column;
            }
            
            input {
                height: 30px;
                border: 1px solid #2a2a2a;
                border-radius: 5px;
            }
            
            input:focus {
                border: 1px solid #50C878;
                outline: none;
            }
            
            button {
                height: 35px;
                border: 1px solid #2a2a2a;
                border-radius: 5px;
                border: 1px solid #2a2a2a;
                background-color: #2a2a2a;
                color: #fff;
            }
            button:hover {
                cursor: pointer;
                border: 1px solid #50C878;
                background-color: #50C878;
            }
            
            .font-size20 {
                font-size: 20px;
            }
            
            .success {
                color: #50C878;
            }
            
            .error {
                color: #bf2d0d;
            }
        </style>
    </head>
    <body>
        <div id="header">
            <div class="container">
                <div class="header-wrapper">
                    <div class="logo-wrapper">
                        <a href="/">
                            <img class="logo" src="/images/logo.png" alt="logo">
                        </a>
                    </div>
                    <div class="links-wrapper">
                        <a href="/" class="home-link">Home</a>
                        <a href="/total_spent" class="totalspent-link">Total spent</a>
                        <a href="/average_spending_by_age" class="average-link">Average spending</a>
                        <a href="/write_high_spending_user" class="add-link">Add high spending user</a>
                    </div>
                </div>
            </div>    
        </div>
        <br>
        <div class="container main-container">
"""

## FOOTER
footer = """
    </div>
    <br>
    <div id="footer">
        <div class="container">
            <p>Петар Белевски - pythonFlaskProject © 2024</p>
        </div>
    </div>
    </body>
    </html>
"""

## HOMEPAGE
@app.route("/")
def index():
    ## connection to database
    conn = sqlite3.connect('users_vouchers.db')
    cursor = conn.cursor()
    ## get all users info from user_info table
    users = cursor.execute("select * from user_info")
    users_data = users.fetchall()
    ## close connection to database
    conn.close()

    data = header

    data += '''
        <style>
        .home-link {
            color: #50C878!important;
        }
        </style>
    '''

    data += f"<h1>Homepage</h1>"

    ## data to be shown on webpage
    data += '''
        <table>
            <tr>
                <th>#</th>
                <th>Name</th>
                <th>E-mail</th>
                <th>Age</th>
                <th></th>
            </tr>
    '''

    ## Loop through users and add them to the table
    for user in users_data:
        data += f'''
            <tr>
                <td>{user[0]}</td>
                <td>{user[1]}</td>
                <td>{user[2]}</td>
                <td>{user[3]}</td>
                <td class="buttons">
                    <a href="/total_spent/{user[0]}">See user total spendings</a>
                </td>
            </tr>
        '''

    data += '''
        </table>
    '''

    data += footer

    return data

## USER SINGLE PAGE
@app.route("/total_spent", defaults={"user_id": 791})
@app.route("/total_spent/<int:user_id>")
def total_spent(user_id):
    ## connection to database
    conn = sqlite3.connect('users_vouchers.db')
    cursor = conn.cursor()
    ## get user info from user_info table with particular user_id
    user_info = cursor.execute(f"SELECT * FROM user_info WHERE user_id={user_id}")
    user_data = user_info.fetchall()
    ## get all user spendings info from user_spending table with particular user_id
    user_spending = cursor.execute(f"SELECT * FROM user_spending WHERE user_id={user_id}")
    user_all_spendings = user_spending.fetchall()
    ## get SUM of all user spendings from user_spending table with particular user_id
    user_total_spending = cursor.execute(f"SELECT SUM(money_spent) FROM user_spending WHERE user_id={user_id}")
    user_total_spendings = user_total_spending.fetchall()
    ## close connection to database
    conn.close()

    data = header

    data += '''
        <style>
            .totalspent-link {
                color: #50C878!important;
            }
        </style>
    '''

    data += "<h1>Total spent by user</h1>"

    data += f'''
        <table>
            <tr>
                <th>#</th>
                <th>Name</th>
                <th>E-mail</th>
                <th>Age</th>
            </tr>
            <tr>
                <td>{user_id}</td>
                <td>{user_data[0][1]}</td>
                <td>{user_data[0][2]}</td>
                <td>{user_data[0][3]}</td>
            </tr>
        </table>
        <br>
    '''

    if user_all_spendings != []:

        ## data to be shown on webpage
        data += '''
            <table>
                <tr>
                    <th>#</th>
                    <th>Money spent</th>
                    <th>Year</th>
                </tr>
        '''

        ## loop through user spendings and add them to the table
        i = 1
        for user in user_all_spendings:
            data += f'''
                <tr>
                    <td>{i}</td>
                    <td>${user[1]}</td>
                    <td>{user[2]}</td>
                </tr>
            '''
            i += 1

        data += '''
            </table>
            <br>
        '''

    ## add total spendings of user in new table
    user_total_spent = user_total_spendings[0][0]
    if user_total_spent == None:
        user_total_spent = 0
    data += f'''
        <table class="total-table">
            <tr>
                <th>Total money spent</th>
            </tr>
            <tr>
                <td>${user_total_spent}</td>
            </tr>
        </table>
        <br>
    '''



    data += footer

    return data

## AVERAGE SPENDING BY AGE
@app.route("/average_spending_by_age")
def average_spending_by_age():
    ## connection to database
    conn = sqlite3.connect('users_vouchers.db')
    cursor = conn.cursor()
    ## get average spendings from users grouped by age groups
    average_spending_by_age = cursor.execute(f"""
        SELECT
            AVG(us1.money_spent) AS '18-24',
            AVG(us2.money_spent) AS '25-30',
            AVG(us3.money_spent) AS '31-36',
            AVG(us4.money_spent) AS '37-47',
            AVG(us5.money_spent) AS '>47'
        FROM 
            user_info AS ui
        LEFT JOIN 
            user_spending AS us1 ON ui.user_id = us1.user_id AND (ui.age >= 18 AND ui.age <= 24)
        LEFT JOIN 
            user_spending AS us2 ON ui.user_id = us2.user_id AND (ui.age >= 25 AND ui.age <= 30)
        LEFT JOIN 
            user_spending AS us3 ON ui.user_id = us3.user_id AND (ui.age >= 31 AND ui.age <= 36)
        LEFT JOIN 
            user_spending AS us4 ON ui.user_id = us4.user_id AND (ui.age >= 37 AND ui.age <= 47)
        LEFT JOIN 
            user_spending AS us5 ON ui.user_id = us5.user_id AND ui.age > 47;
    """)
    average_spending_by_age_data = average_spending_by_age.fetchall()
    ## close connection to database
    conn.close()

    data = header

    data += '''
        <style>
            .average-link {
                color: #50C878!important;
            }
        </style>
    '''

    data += "<h1>Average spending by age</h1>"

    data += '''
        <table>
            <tr>
                <th>Age Range</th>
                <th>Average money spent</th>
            </tr>
    '''

    data += f'''
            <tr>
                <td>18 - 24</td>
                <td>${average_spending_by_age_data[0][0]}</td>
            </tr>
            <tr>
                <td>25 - 30</td>
                <td>${average_spending_by_age_data[0][1]}</td>
            </tr>
            <tr>
                <td>31 - 36</td>
                <td>${average_spending_by_age_data[0][2]}</td>
            </tr>
            <tr>
                <td>37 - 47</td>
                <td>${average_spending_by_age_data[0][3]}</td>
            </tr>
            <tr>
                <td>> 47</td>
                <td>${average_spending_by_age_data[0][4]}</td>
            </tr>
        </table>
    '''

    data += footer

    return data

## ADD HIGH SPENDING USER
@app.route("/write_high_spending_user", methods=["POST", "GET"])
def write_high_spending_user():
    if request.method == "GET":

        data = header

        data += '''
            <style>
                .add-link {
                    color: #50C878!important;
                }
            </style>
        '''

        data += "<h1>Add high spending user</h1>"

        data += '''
            <form method="POST" action="/write_high_spending_user">
                <label>
                    User ID
                    <input type="text" name="user_id"/>
                </label>
                <label>
                    Total Spending
                    <input type="text" name="total_spending"/>
                </label>
                <button type="submit">Add</button>
            </form>
        '''

        data += footer

        return data
    else:
        try:
            ## save form inputs into variables
            user_id = request.form.get("user_id")
            total_spending = request.form.get("total_spending")
            ## connection to database
            conn = sqlite3.connect('users_vouchers.db')
            cursor = conn.cursor()
            ## insert variables into high_spenders table
            insert_query = f"""
                INSERT INTO high_spenders (user_id, total_spending)
                VALUES ('{user_id}', '{total_spending}')
            """
            insert = cursor.execute(insert_query)
            conn.commit()
            cursor.close()
        except sqlite3.Error as error:
            data = header

            data += f'''
                <p class="font-size20 error">Failed to insert data. Please try again later. Error: {error}</p>
            '''

            data += footer

            return data
        finally:
            if conn:
                ## close connection to database
                conn.close()

                data = header

                data += f'''
                    <p class="font-size20 success">Successfully added user_id: {user_id}, and total_spending: ${total_spending} to high_spenders table.</p>
                '''

                data += footer

                return data

## BONUS

## BONUS 1 - TELEGRAM BOT INTEGRATION

@app.route('/user', methods=['POST'])
def user():
    ## get posted parameter: user_id
    user_id = int(request.json.get('user_id'))

    ## connection to database
    conn = sqlite3.connect('users_vouchers.db')
    cursor = conn.cursor()
    ## get user info from user_info table with particular user_id
    user_info = cursor.execute(f"SELECT * FROM user_info WHERE user_id={user_id}")
    user_data = user_info.fetchall()
    ## get all user spendings info from user_spending table with particular user_id
    user_spending = cursor.execute(f"SELECT * FROM user_spending WHERE user_id={user_id}")
    user_all_spendings = user_spending.fetchall()
    ## get SUM of all user spendings from user_spending table with particular user_id
    user_total_spending = cursor.execute(f"SELECT SUM(money_spent) FROM user_spending WHERE user_id={user_id}")
    user_total_spendings = user_total_spending.fetchall()
    ## close connection to database
    conn.close()

    user_data = {
        "user_id": user_id,
        "name": user_data[0][1],
        "email": user_data[0][2],
        "age": user_data[0][3],
        "total_spent": user_total_spendings[0][0]
    }
    return jsonify(user_data)

## BONUS 2 - UNIT TESTS





if __name__ == "__main__":
    ##app.run(debug=True)
    app.run(host="127.0.0.1", port=5000, debug=True)