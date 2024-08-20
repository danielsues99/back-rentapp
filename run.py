from app import create_app, db
from app.models import Landlord, Tenant, Payment

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Landlord': Landlord, 'Tenant': Tenant, 'Payment': Payment}

if __name__ == '__main__':
    app.run(debug=True)
