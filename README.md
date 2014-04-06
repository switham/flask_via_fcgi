<h3>A slightly more secure way to run Flask using FastCGI.</h3>

There's a security bug that people seem to spread by word of mouth.  It shows up in recipes for running web apps using `.htaccess` and `FastCGI`, a.k.a. `fcgi`.  This project gives a recipe for use with Flask, while fixing the bug.

This method could be used to run any Python, Ruby, Perl, or PHP application 
in part of a directory being served by Apache, when you don't have control 
over Apache's config files (e.g., when you're running on a hosting
service).  The recipe deserves explaining in English; for now an example is given by the files in this project.

<h4>The Gaping Hole</h4>

The bug involves `.htaccess` files like this:

`just code`<br>
**`bold code?`**

> Options +ExecCGI<br>
> AddHandler fcgid-script .fcgi<br>
> RewriteEngine On<br>
> <b>RewriteCond %{REQUEST_FILENAME} !-f</b><br>
> RewriteRule ^(.*)$ sponge.fcgi/$1 [L]

Here, `%{REQUEST_FILENAME}` means, "the requested URL mapped to an absolute path in the filesystem," and `!-f` means, "Not(there's a file there)."
This tells Apache, "If the URL maps to a real file, don't rewrite the URL, just **serve it to anyone who asks for it**, 
otherwise, apply the `RewriteRule` (which activates 
`fcgi`). In other words, make every file in this subdirectory tree 
publicly readable. And, if a URL that you want Flask to serve happens to 
coincide with an actual file, Flask doesn't get called--the direct 
contents of the file take 
precedence. If you want the Flask app to control access, or if there is 
any information in the directory you want to keep secret, then you need a 
much more restrictive rule, Fortunately it's not that hard; replace the 
`RewriteCond` line with something like:

> RewriteCond %(REQUEST_FILENAME) !=/home/me/public_html/sponge/sponge.fcgi

That should be all one line. $HOME doesn't work in this context, you have 
to spell it out. What this `RewriteCond` means is, treat this *one file* 
in the usual way, which the rest of the recipe sets up to be an `fcgi` 
script. Every other 
URL in this subdirectory goes through `fcgi` and Flask. You could set up more 
exceptions (i.e. name paths you want Apache to serve directly) using 
multiple `RewriteCond` lines, but allowing almost nothing at 
first and adding individual exceptions as needed, is the right way to go.
