from flask import Flask, request 
import pandas as pd 
app = Flask(__name__) 

# dokumentasi
@app.route("/docs")
def documentation():
    return '''
        <h1>Documentation</h1>
        <h2>Static Endpoints</h2>

        <ol>
            <li>
                <p> / , method = GET </p>
                <p> Base Endpoint, returning welcoming string value. </p>
                <a href="/data/get/books_c.csv">Example</a>
            </li>
        </ol>
         
        <h2>Dynamic Endpoints</h2>

        <ol start = "2">
            <li>
                <code> 
                    /data/get/<data_name> , method = GET 
                </code>
                <p> Return full data <data_name> in JSON format. Currently available data are: </p>
                <ul style="list-style-type:disc;">
                    <li> books_c.csv </li>
                    <li> pulsar_stars.csv </li>
                </ul>
            </li>

            <li>
                <p> /data/get/equal/<data_name>/<column>/<value> , method = GET </p>
                <p> Return all <data_nam> where the value of column <column> is equal to <value> </p>
            </li>
        </ol>
    '''

@app.route('/data/genres', methods = ['GET'])
def get_genres():
    conn = sqlite3.connect("data_input/chinook.db")
    data = pd.read_sql_query(
        '''
        SELECT *
        FROM genres
        ''', conn)
    return data.to_json()

@app.route('/data/get/<data_name>', methods=['GET']) 
def get_data(data_name): 
    data = pd.read_csv('data/' + str(data_name))
    return data.to_json()
    
@app.route('/data/get/equal/<data_name>/<column>/<value>', methods=['GET']) 
def get_data_equal(data_name, column, value): 
    data = pd.read_csv('data/' + str(data_name))
    mask = data[column] == value
    data = data[mask]
    return data.to_json()

if __name__ == '__main__':
    app.run(debug=True, port=5000) 
