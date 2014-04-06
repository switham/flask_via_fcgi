<h2>A slightly more secure way to run Flask using FastCGI.</h2>

There's a security bug that people seem to spread by word of mouth.  It shows up in recipes for running web apps using `.htaccess` and `FastCGI`, a.k.a. `fcgi`.  This project gives the same recipe while fixing the bug.

This method could be used to run any Python, Ruby, Perl, or PHP application 
in part of a directory being served by Apache, when you don't have control 
over Apache's config files (e.g., when you're running on on a hosting
service).  The recipe deserves explaining in English; for now an example of 
the correct solution is given by the files in this project.

<b>But the bug</b> involves `.htaccess` files with this line:

    RewriteCond %{REQUEST_FILENAME} !-f

This tells Apache, "If the URL maps to a real file, **serve it to anyone who asks for it**, otherwise, apply the RewriteRule (which activates the Flask app). In other words, make every file in this subdirectory tree publicly readable. And, if a URL that Flask is trying to serve happens to coincide with an actual file, the direct contents of the file take precedence. If you want the Flask app to control access, or if there is any information in the directory you want to keep secret, then you need a much more restrictive rule, Fortunately it's not that hard; replace the RewriteCond line with something like:

    RewriteCond %(REQUEST_FILENAME) !=/home/me/public_html/sponge/sponge.fcgi

That should be all one line. $HOME doesn't work in this context, you have to spell it out. What this RewriteCond means is, treat this *one file* in the usual way, which has been set up to be a CGI script. Every other URL in this subdirectory goes through Flask. You could set up more exceptions using multiple RewriteCond lines, but allowing nothing at first and adding individual exceptions as needed, is the right way to go.
