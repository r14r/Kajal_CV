# SQLite notes

SQLite is an embedded SQL database stored in a local file. It is useful for prototypes and single-user applications because it does not require a separate database server. SQL parameters keep user input separate from SQL syntax, reducing SQL injection risk.

This demonstration stores documents, chunks, conversations and messages in SQLite. It binds its web server to the local loopback interface and has no user authentication, so it should not be published publicly without additional controls.
