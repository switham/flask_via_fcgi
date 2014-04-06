<h3>A slightly more secure way to run Flask using FastCGI.</h3>

There's a security bug that people seem to spread by word of mouth.  It shows up in recipes for running web apps using `.htaccess` and `FastCGI`, a.k.a. `fcgi`.  This project gives a recipe for use with Flask, while fixing the bug.

This method could be used to run any Python, Ruby, Perl, or PHP application 
in part of a directory being served by Apache, when you don't have control 
over Apache's config files (e.g., when you're running on a hosting
service).  The recipe deserves explaining in English; for now an example is given by the files in this project.

<h4>The Swiss Cheese</h4>

The bug involves `.htaccess` files like this:

`Options +ExecCGI`<br>
`AddHandler fcgid-script .fcgi`<br>
`RewriteEngine On`<br>
**`RewriteCond %{REQUEST_FILENAME} !-f`**<br>
`RewriteRule ^(.*)$ sponge.fcgi/$1 [L]`

Here, `%{REQUEST_FILENAME}` means, "the absolute path in the filesystem
that the requested URL maps to," 
and `!-f` means, "Not(there's a file there)."
This tells Apache, "If the URL maps to a real file, don't rewrite the URL, 
just **serve the file to anyone who asks for it**, 
otherwise, apply the `RewriteRule` (which activates 
`fcgi`). In other words, make every file in this subdirectory tree 
publicly readable. And, if a URL that you want Flask to serve happens to 
coincide with an actual file, Flask doesn't get called--the direct 
contents of the file take 
precedence. If you want the Flask app to control access, or if there is 
any information in the directory you want to keep secret, then you need a 
much more restrictive rule, Fortunately it's not that hard; rewrite the `RewriteCond` line like this:

`Options +ExecCGI`<br>
`AddHandler fcgid-script .fcgi`<br>
`RewriteEngine On`<br>
**`RewriteCond %{REQUEST_FILENAME} !=/home/me/public_html/sponge/sponge.fcgi`**<br>
`RewriteRule ^(.*)$ sponge.fcgi/$1 [L]`

($HOME doesn't work in this context, you have 
to spell it out.)  What this `RewriteCond` means is, if the URL maps to 
anything but *the specific fcgi script*, then rewrite it--prepend the
script name to it-- and try again.
But once the URL points to the script, let Apache treat it 
in the usual way, which (given the rest of the recipe) is 
to run the script, which runs Flask.  You could set up more 
exceptions (i.e. name paths you want Apache to serve directly) using 
multiple `RewriteCond` lines, but allowing almost nothing at 
first and adding individual exceptions as needed, is the right way to go.
