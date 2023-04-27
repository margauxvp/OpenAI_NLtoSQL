# Import the required packages
import openai
import json
import pyodbc

# Data information
server = 'YOUR-SERVER-NAME'
database = 'YOUR-DATABASE-NAME'
username = 'YOUR-USERNAME'
pwd = 'YOUR-PASSWORD'

# Get information about your data, and use it translate natural language to SQL code with OpenAI to then execute it on your data
def NLtoSQL(question):
    # Connect to your database using ODBC
    connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server +';DATABASE=' + database + ';UID=' + username +';PWD=' + pwd + ';')

    try:
        # Execute the query to retrieve the column information
        with connection.cursor() as cursor:
            sql = "SELECT TABLE_NAME,COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS"
            cursor.execute(sql)
            result_set = cursor.fetchall()

            # Extract the column names from the cursor description
            column_names = [column[0] for column in cursor.description]

            # Extract the column names from each row and convert to dictionary
            result_list = [dict(zip(column_names, row)) for row in result_set]

        # Format the result set as a JSON string
        result_set_json = json.dumps(result_list)

        # Define the OpenAI prompt
        prompt = f"Here are the columns in your database:\n{result_set_json}\nGenerate me SQL code for the following question using the information about my database. {question}"

        # Setting API Key and API endpoint for OpenAI
        openai.api_key = "YOUR-AZURE-OPENAI-KEY"
        openai.api_type = "azure"
        openai.api_base = "https://<YOUR-OPENAI-ENDPOINT>.openai.azure.com/"
        openai.api_version = "2022-12-01"
        deployment_engine = "YOUR-DEPLOYMENT-NAME"

        # Generate text using the OpenAI API
        response = openai.Completion.create(
            engine=deployment_engine,
            prompt=prompt,
            max_tokens=200,
            n=1,
            stop=None,
            temperature=0,
        )

        # Retrieve the generated SQL Query
        SQLQuery = response.choices[0].text
    
        # Execute the SQL query 
        cursor.execute(SQLQuery)
        final_result = str(cursor.fetchall())
    
        # Print the question + SQL Query + Generated Response
        return 'Question: ' + question + '\nSQL Query: ' + SQLQuery + '\n\nGenerated Response: ' + final_result
    
    finally:
        # Close the database connection
        connection.close()

# Test the function
print(NLtoSQL('What is the total payments value for 2021?'))
