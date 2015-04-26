from pizza import pizza

@pizza.route('/')
def index():
    return pizza.send_static_file('index.html')