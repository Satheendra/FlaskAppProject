from flask import Flask, jsonify, request, render_template
import mysql.connector

app = Flask(__name__)

# Function to establish MySQL connection
def connect_to_mysql():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='github_satheendra'
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_language_data', methods=['GET'])
def get_language_data():
    lang_name = request.args.get('lang_name')

    # Connect to MySQL
    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        # Execute SQL query
        query = """
            SELECT
                l.lang_id,
                y.year,
                y.qtr,
                l.repo_count,
                gm.prs_count,
                gm.issues_count
            FROM
                languages l
            JOIN
                github_master gm ON l.lang_id = gm.lang_id
            JOIN
                year y ON gm.year_id = y.year_id
            WHERE
                l.lang_name = %s
        """
        cursor.execute(query, (lang_name,))
        language_data = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        # # Return the data in JSON format
        # return jsonify(language_data)

        # Render the language_data.html template with language_data
        return render_template('language_data.html', lang_name=lang_name, language_data=language_data)

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    # Run the Flask app on port 5000
    app.run(debug=True)

# end of code - commit test comment for github actions