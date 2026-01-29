from flask import Flask , jsonify, render_template, request
import requests
import pandas as pd

api_key='03d45c2035e64d9b906a8baa316b7a3a'
url ='https://newsapi.org/v2/everything?q=tesla&from=2025-12-29&sortBy=publishedAt&apiKey=03d45c2035e64d9b906a8baa316b7a3a'

app= Flask(__name__)


@app.route('/')
def home():
    name="Niranjan"
    return render_template('index.html', name=name)

@app.route('/greet', methods=['POST'])
def greet():
    return "Greetings from Flask!"

@app.route('/hello', methods=['GET'])
def hello():
    return render_template("form.html")

@app.route('/submit', methods=['POST'])
def submit():
    return "Form submitted successfully!"



@app.route('/about')
def about():
    return """<h1>About Page</h1><br>
                <p>This  about page of our Flask application.</p><h3>hii this h3</h3>"""


# user application programming interface


@app.route('/create_user', methods=['POST'])
def create_user():
    return jsonify({'msg':"new user is ccrreated successfully"})

@app.route('/get_user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return jsonify({'msg':f'user with id {user_id} is featched sucessfully'})

@app.route('/update_user/<int:user_id>',methods=['PUT'])
def update_user(user_id):
    return jsonify({'msg':'user with id is updated successfully'})

@app.route('/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    return jsonify({'msg':'user with id is deleted successfully'})


# hamdling the jason data and the external api
@app.route('/app/news')
def get_news():
    response=requests.get(url)
    if response.status_code==200:
        data=response.json()
        artical_lenght=len(data['articles'])
        artical_1=data['articles'][0]
        title1=artical_1['title']
        author1=artical_1['author']
        publised_date=artical_1['publishedAt']
        output_data={
            'artical_lenght':artical_lenght,
            'title1':title1,
            'author1':author1,
            'publised_date':publised_date,
            'artical_1_details':artical_1['description']
        }
        return jsonify(output_data)

# handling the csv files 
@app.route('/upload_csv', methods=['GET'])
def upload_csv():
    return render_template('form1.html')

@app.route('/upload', methods=['POST'])
def upload_msg():
    file = request.files['file']
    print("file:", file)
    if file.filename.endswith('.csv'):
        path='userfile/'+file.filename
        file.save(path)
        file_path='userfile/employee salary dataset.csv'
        df=pd.read_csv(file_path)
        print(df.head())
        # basic stats : nim mod median count avrage 
        minimun_salary=int(df['salary'].min())
        maximum_salary=int(df['salary'].max())
        average_salary=int(df['salary'].mean())
        median_salary=int(df['salary'].median())
        total_emp= int(df['salary'].count())
        responce ={'min salary':minimun_salary,
                   'max salary':maximum_salary,
                   'average salary':average_salary,
                   'median salary':median_salary,
                   'no emp':total_emp
                   }
        return jsonify(responce)
    return "csv file uploaded successfully"






# jsonify the data 
@app.route('/data')
def data():
    data={"name": "John", "age" : 30}
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)