from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Employee Onboarding/Offboarding API"

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(debug=True)
