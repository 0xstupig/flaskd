from elasticsearch import RequestsHttpConnection
from elasticsearch_dsl.connections import connections

import services.search as search
from services.email import email_service


def init_app(app, db):
    email_service.sender.init_app(app)

    connections.create_connection(
        hosts=[{'host': app.config['ES_HOST'], 'port': app.config['ES_PORT']}],
        use_ssl=app.config['ES_USE_SSL'],
        connection_class=RequestsHttpConnection,
        timeout=120
    )

    app.elasticsearch = connections.get_connection()

    db.event.listen(db.session, 'before_commit', search.before_commit)
    db.event.listen(db.session, 'after_commit', search.after_commit)

