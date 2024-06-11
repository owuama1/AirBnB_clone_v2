# Update package list and install Nginx if it's not already installed
package { 'nginx':
  ensure => installed,
}

# Create required directories
file { '/data/web_static/releases/test/':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
  recurse => true,
}

file { '/data/web_static/shared/':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
  recurse => true,
}

# Create a fake HTML file
file { '/data/web_static/releases/test/index.html':
  ensure  => file,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0644',
  content => "<html>
  <head>
  </head>
  <body>
    Welcome to your web_static test page.
  </body>
</html>",
}

# Create a symbolic link, forcefully delete if it already exists
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test/',
  force  => true,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

# Update ownership recursively
exec { 'chown_data_folder':
  command => 'chown -R ubuntu:ubuntu /data/',
  path    => ['/bin', '/usr/bin'],
}

# Update Nginx configuration to serve the content
file_line { 'nginx_hbnb_static':
  line    => '    location /hbnb_static {',
  path    => '/etc/nginx/sites-available/default',
  match   => 'server_name _;',
  before  => '}',
  require => Package['nginx'],
  notify  => Service['nginx'],
}

file_line { 'nginx_alias':
  line    => '        alias /data/web_static/current/;',
  path    => '/etc/nginx/sites-available/default',
  match   => 'server_name _;',
  before  => '}',
  require => Package['nginx'],
  notify  => Service['nginx'],
}

# Restart Nginx to apply the changes
service { 'nginx':
  ensure  => running,
  enable  => true,
  require => [
    Package['nginx'],
    File['/etc/nginx/sites-available/default'],
  ],
}

notify { 'Setup completed successfully!':
  require => [
    File_line['nginx_hbnb_static'],
    File_line['nginx_alias'],
    Exec['chown_data_folder'],
  ],
}
