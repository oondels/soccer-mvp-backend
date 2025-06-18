from src import create_app

app = create_app()


@app.route("/", methods=['GET'])
def helth_check():
    return "Football api is runnig"


if __name__ == "__main__":
    app.run()
