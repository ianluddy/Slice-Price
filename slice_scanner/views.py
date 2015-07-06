from slice_scanner import app, documentor

@app.route('/docs')
@documentor.doc()
def docs():
    """
    Get API documentation
    """
    return documentor.html(
        title="Slice Scanner",
        author="ianluddy@gmail.com"
    )

@app.route('/')
@documentor.doc()
def index():
    return app.send_static_file('index.html')

@app.route('/pizza')
@documentor.doc()
def pizza():
    return {}
