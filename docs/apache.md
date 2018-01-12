# Apache

The final Apache config file will look something like this. It has the server
configured for:
- HTTPS with letsencrypt
- Mapzen server (no longer needed)
- Django WSGI in a virtualenv

Put the config in `/etc/apache2/sites-available/tours-le-ssl.conf` and run
```
a2ensite /etc/apache2/sites-available/tours-le-ssl.conf
service apache2 reload
```

> This example config assumes the Django project is installed at
> `/var/www/html/tours-backend`, and that Valhalla is running on port `8080`.

```apache
<IfModule mod_ssl.c>
<VirtualHost *:443>

	ServerName tours.bruinmobile.com
	ServerAdmin webmaster@localhost
	DocumentRoot /var/www/html

	Protocols h2 http/1.1
	<Directory "/var/www/html/tours-backend/.git">
		Order allow,deny
		Deny from all
	</Directory>

	# Port forwarding for Valhalla; port should match valhalla.json
	#<Location /route>
	#	ProxyPreserveHost On
	#	ProxyPass http://localhost:8080/route
	#	ProxyPassReverse http://localhost:8080/route
	#</Location>
	#<Location /optimized_route>
	#	ProxyPreserveHost On
	#	ProxyPass http://localhost:8080/optimized_route
	#	ProxyPassReverse http://localhost:8080/optimized_route
	#</Location>


	# Django

	Alias /static /var/www/html/tours-backend/static
	<Directory /var/www/html/tours-backend/static>
		Options -Indexes
		Require all granted
	</Directory>

	Alias /media /var/www/html/tours-backend/media
	<Directory /var/www/html/tours-backend/media>
		Options -Indexes
		Require all granted
	</Directory>

	<Directory /var/www/html/tours-backend/tours>
		<Files wsgi.py>
			Require all granted
		</Files>
	</Directory>


	# Use this if not using virtualenv
	#WSGIDaemonProcess tours python-path=/var/www/html/tours-backend

	# Use this if using virtualenv
	WSGIDaemonProcess tours python-path=/var/www/html/tours-backend:/usr/local/venvs/tours-backend/lib/python2.7/site-packages

	WSGIProcessGroup tours
	WSGIScriptAlias / /var/www/html/tours-backend/tours/wsgi.py


	Options -Indexes

	ErrorLog ${APACHE_LOG_DIR}/tours.log
	CustomLog ${APACHE_LOG_DIR}/tours.log combined

	# LetsEncrypt SSL
	SSLCertificateFile /etc/letsencrypt/live/tours.bruinmobile.com/cert.pem
	SSLCertificateKeyFile /etc/letsencrypt/live/tours.bruinmobile.com/privkey.pem
	Include /etc/letsencrypt/options-ssl-apache.conf
	SSLCertificateChainFile /etc/letsencrypt/live/tours.bruinmobile.com/chain.pem
</VirtualHost>

</IfModule>
```
