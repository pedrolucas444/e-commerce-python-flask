# Importation
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'  # SQLite database URI

db = SQLAlchemy(app)  # Initializing SQLAlchemy with the Flask app

# Modeling
# Product (id, name, price, description)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True) #Text is used for long text fields, when the length doesn't have a limit

@app.route('/api/products/add', methods=["POST"]) # Defining the route for adding a product and specifying the HTTP method (POST)
def add_product():
    # Assuming the data is sent as JSON in the request body
    # Checking if the required fields are present in the request data
    # If they are, create a new product and add it to the database
    # If not, return an error message
    data = request.json 
    if 'name' in data and 'price' in data: 
        product = Product(name=data["name"], price=data["price"], description=data.get("description", "")) 
        db.session.add(product)
        db.session.commit()
        return jsonify ({"message": "Product registered successfully"}), 200 
    return jsonify({"message": "Invalid product data"}), 400 

@app.route('/api/products/delete/<int:product_id>', methods=["DELETE"]) # Defining the route for getting all products and specifying the HTTP method (GET)
def delete_product(product_id):
    # Retrieve product from the database
    # Check if the product exists
    # If it exists, delete it from the database
    # If it does not exist, return error 404 not found
    product = Product.query.get(product_id)
    if product != None:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"}), 200
    return jsonify({"message": "Product not found"}), 404  
  
# Defining the root route (Home page) and the function that will be executed when it's requested
@app.route('/')
def hello_world():
    return "Hello World"

# Running the Flask application
# The debug=True option allows for automatic reloading and better error messages
if __name__ == '__main__':
    app.run(debug=True)