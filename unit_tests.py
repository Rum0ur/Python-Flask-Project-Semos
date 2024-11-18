import pytest
import sqlite3
from app import app

@pytest.fixture
def client():
    ## test fixture that provides the Flask test client
    ## This is run before each test function

    app.config['TESTING'] = True  # Enable testing mode
    app.config['DATABASE'] = 'users_vouchers.db'  # Use in-memory database for testing
    with app.test_client() as client:
        yield client


@pytest.fixture
def init_db():
    ## This fixture initializes the database schema for testing
    ## I use an in-memory database to avoid affecting the real database

    conn = sqlite3.connect('users_vouchers.db')
    cursor = conn.cursor()

    conn.commit()
    conn.close()

def test_total_spent(client, init_db):
    ## Test the total_spent route for a specific user
    response = client.get('/total_spent/90')

    ## Check that the response status code is 200
    assert response.status_code == 200
    ## Check if the user's name is in the response data
    assert b'Daniel Washington' in response.data
    ## Check if the user's email is in the response data
    assert b'daniel_washington@example.com' in response.data
    ## Check if the user's age is in the response data
    assert b'30' in response.data
    ## Check if the total spent value is correct
    assert b'$19983.91' in response.data


def test_average_spending_by_age(client, init_db):
    ## Test the average_spending_by_age route
    response = client.get('/average_spending_by_age')

    ## Check that the response status code is 200
    assert response.status_code == 200

    ## Check if age range 18 - 24 is present on the page
    assert b'18 - 24' in response.data
    ## Check if average spending for age 18-24 is calculated
    assert b'$2509.7405273833674' in response.data

    ## Check if age range 25 - 30 is present on the page
    assert b'25 - 30' in response.data
    ## Check if average spending for age 25 - 30 is calculated
    assert b'$2471.584902193242' in response.data

    ## Check if age range 31 - 36 is present on the page
    assert b'31 - 36' in response.data
    ## Check if average spending for age 31 - 36 is calculated
    assert b'$2529.1548323576367' in response.data

    ## Check if age range 37 - 47 is present on the page
    assert b'37 - 47' in response.data
    ## Check if average spending for age 37 - 47 is calculated
    assert b'$2495.8429822335024' in response.data

    ## Check if age range >47 is present on the page
    assert b'> 47' in response.data
    ## Check if average spending for age >47 is calculated
    assert b'$2485.7710634441087' in response.data

def test_add_high_spending_user(client, init_db):
    ## Test adding a high-spending user

    data = {
        'user_id': 7,
        'total_spending': 7777
    }

    response = client.post('/write_high_spending_user', data=data)

    ## Check that the response status code is 200
    assert response.status_code == 200
    assert b'Successfully added user_id: 7, and total_spending: $7777 to high_spenders table.' in response.data


def test_user_api(client, init_db):
    ## Test the /user API endpoint
    data = {'user_id': 90}
    response = client.post('/user', json=data)

    ## Check that the response status code is 200
    assert response.status_code == 200

    ## Check if the user data is correct
    response_json = response.get_json()
    assert response_json['user_id'] == 90
    assert response_json['name'] == 'Daniel Washington'
    assert response_json['email'] == 'daniel_washington@example.com'
    assert response_json['age'] == 30
    assert response_json['total_spent'] == 19983.91