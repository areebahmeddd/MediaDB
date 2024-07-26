'''
Entry point for the Flask application. This script initializes the Flask app using the factory method from
the app package and starts the development server.
'''

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
