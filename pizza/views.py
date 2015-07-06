from pizza import app

@lumberapp.route('/docs')
@documentor.doc()
def docs():
    """
    Get API documentation
    """
    return documentor.html(
        title="slice scanner",
        author="ian.luddy@gmail.com"
    )

@app.route('/')
@documentor.doc()
def index():
    return app.send_static_file('index.html')

@app.route('/pizza')
@documentor.doc()
def pizza():
    return {}
