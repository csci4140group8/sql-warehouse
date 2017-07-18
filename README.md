# Dependencies

```pip install -r requirements.txt```

New dependencies must be added to this file as they are imported.

# Environment Variables
The application uses SSH Tunneling to connect to the database hosted at Dalhousie.  The following environment variables are required:

```SSH_USER```

```SSH_PASS```

```MYSQL_USER```

```MYSQL_PASS```

# Run

```python app.py```