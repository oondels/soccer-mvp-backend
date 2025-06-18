from src import create_app
import os

app = create_app()


@app.route("/", methods=['GET'])
def helth_check():
    return "Football api is runnig"


if __name__ == "__main__":
    dev_mode = os.getenv('DEV_ENV') == 'development'
    app.run(debug=dev_mode)
