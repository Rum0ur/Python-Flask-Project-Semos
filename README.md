- images folder is used for storred images that I use in the UI of the app.

- app.py
  - function serve_image(): used for serving(showing) images on the webpage.
  - function get_url_path(): used for returning current page path and mark link to that page as active in the header.
  - header - html and css for the header of the app.
  - footer - html and css for the footer of the app.
  - route index(): listing all users (user_id, name, email, age) and link to total_spent/user_id route.
    ![image](https://github.com/user-attachments/assets/17ca1995-28de-4370-ba14-fe5c3574b526)
    
  - route total_spent(): get user_id from url and get all his info from database, then list his personal info in the first table, his spendings in the second table and total spent in the third table. (if the user has not spent anything the second table is not shown)
    ![image](https://github.com/user-attachments/assets/c65c9983-8801-4fd4-a1c4-4fd1f25b06b7)
    
  - route average_spending_by_age(): query that calculates average spending of people grouped by age ranges: 18-24, 25-30, 31-36, 37-47, >47 and shows them in a table
    ![image](https://github.com/user-attachments/assets/5dd3a7a7-8787-405a-a3a2-d488c0c0dbb4)
    
  - route write_high_spending_user() (POST and GET):
    - GET: shows a form to insert a new high spending user
      ![image](https://github.com/user-attachments/assets/ff346896-0a4d-4b75-aec3-b7e007f1a8eb)

    - POST: inserts the posted parameters for the user in high_spenders table, if this is successfull returns success message and if it is not then returns error message.
      ![image](https://github.com/user-attachments/assets/5b1576a3-b30c-4391-acc9-b90577ca9556)

  - route user (POST): intercepts posted "user_id" from telegram bot and returns: name, email, age and total_spent to the bot

- telegram_bot.py
  - function user(): awaits the response from "app.py -> route user" and returns the message that the telegram bot needs to send, or error message if something went wrong
  - function start(): makes the welcome message the bot sends when activated in telegram
  - function main(): handles/activates telegram bot token, start and user functions
    ![image](https://github.com/user-attachments/assets/4332fb79-38fe-4e72-81b3-4eddb1df77c1)

- unit_tests.py
  - function client(): enables testing mode and configures the database that the app uses
  - function init_db(): initializes the database
  - function test_total_spent(): tests if url path "/total_spent/90" returns the correct info about the user with user_id = 90 from route total_spent
  - function test_average_spending_by_age(): tests if url path "/average_spending_by_age" returns the correct values for average spending grouped by age ranges from route average_spending_by_age
  - function test_add_high_spending_user(): tests if the post and insert in database of the url path "/write_high_spending_user" works correctly
  - function test_user_api(): tests if the url path /user/user_id returns correct info about user with user_id = 90
