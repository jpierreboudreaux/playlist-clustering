import cgi

spotifyForm = cgi.FieldStorage()

client_id = spotifyForm.getvalue('clientId')
client_secret = spotifyForm.getvalue('clientSecret')
redirect_uri = spotifyForm.getvalue('redirectURI')
