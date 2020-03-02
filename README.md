# CloudFoundry PHP Example Application:  PHPPgAdmin

This is an example application which can be run on CloudFoundry using the [PHP Buildpack].

This is an out-of-the-box implementation of PHPPgAdmin.  It's an example how common PHP applications can easily be run on CloudFoundry.

## Usage

1. Download the latest phpPgAdmin from [the project site](http://phppgadmin.sourceforge.net/doku.php?id=download).

1. Extract all of the files from phpPgAdmin to the `htdocs` directory. For example: `tar -zx --strip-components=1 -C htdocs/ -f ~/Downloads/phpPgAdmin-5.6.0.tar.bz2`. When done, you should have an `htdocs` directory that looks like this...

    ```bash
    $ ls -l htdocs/
    total 1616
    -rw-r--r--@  1 dmikusa  staff   3141 Nov 12  2018 CREDITS
    -rw-r--r--@  1 dmikusa  staff   6324 Nov 12  2018 DEVELOPERS
    -rw-r--r--@  1 dmikusa  staff   8603 Nov 12  2018 FAQ
    -rw-r--r--@  1 dmikusa  staff  27737 Nov 12  2018 HISTORY
    -rw-r--r--@  1 dmikusa  staff   2890 Nov 12  2018 INSTALL
    -rw-r--r--@  1 dmikusa  staff    581 Nov 12  2018 LICENSE
    -rw-r--r--@  1 dmikusa  staff   5719 Nov 12  2018 TODO
    -rw-r--r--@  1 dmikusa  staff   2414 Nov 12  2018 TRANSLATORS
    -rw-r--r--@  1 dmikusa  staff  28907 Nov 12  2018 admin.php
    -rw-r--r--@  1 dmikusa  staff  16000 Nov 12  2018 aggregates.php
    -rw-r--r--@  1 dmikusa  staff   2492 Nov 12  2018 ajax-ac-insert.php
    ...
    ```

1. If you don't have one already, create a Postgres service.  With Pivotal Web Services, the following command will create a free Postgres database through [ElephantSQL].

    ```bash
    cf create-service elephantsql turtle pgsql
    ```

    If you do not name your service `pgsql` then you need to edit `manifest.yml` and change the service name to match the name of your service.

1. Edit `htdocs/conf/config.inc.php`. Add this block of code at the top of the file. Then delete the block that starts with the comment `An example server.` and runs just up to the block that starts with `Groups definition`. This is deleting the sample configuration.

    ```php
        /*
        * Read PGSQL service properties from 'VCAP_SERVICES'
        */
        $service_blob = json_decode(getenv('VCAP_SERVICES'), true);
        $pgsql_services = array();
        foreach($service_blob as $service_provider => $service_list) {
            // looks for 'elephantsql' service
            if ($service_provider === 'elephantsql') {
                foreach($service_list as $pgsql_service) {
                    $pgsql_services[] = $pgsql_service;
                }
                continue;
            }
            foreach ($service_list as $some_service) {
                // looks for tags of 'postgresql'
                if (in_array('postgresql', $some_service['tags'], true)) {
                    $pgsql_services[] = $some_service;
                    continue;
                }
                // look for a service where the name includes 'pgsql'
                if (strpos($some_service['name'], 'pgsql') !== false) {
                    $pgsql_services[] = $some_service;
                }
            }
        }

        /*
        * Servers configuration
        */
        for ($i = 0; $i < count($pgsql_services); $i++) {
            // parse individual config from uri
            preg_match('/^(?:postgres|postgresql)\:\/\/(.*):(.*)@(.*):(.*)\/(.*)$/',
                    $pgsql_services[$i]['credentials']['uri'], $db);
            if (count($db) == 6) {
                // configure server
                $conf['servers'][$i]['desc'] = $pgsql_services[$i]['name'];
                $conf['servers'][$i]['host'] = $db[3];
                $conf['servers'][$i]['port'] = $db[4];
                $conf['servers'][$i]['sslmode'] = 'allow';
                $conf['servers'][$i]['defaultdb'] = $db[5];
                // Specify the path to the database dump utilities for this server.
                // You can set these to '' if no dumper is available.
                $conf['servers'][$i]['pg_dump_path'] = '/usr/bin/pg_dump';
                $conf['servers'][$i]['pg_dumpall_path'] = '/usr/bin/pg_dumpall';
            }
        }
    ```

1. Edit `htdocs/composer.json` and change `"type": "Application"` to `"type": "application"`. This is a problem with the upstream project and it will cause Composer errors. It should be lower case.

1. Push it to CloudFoundry.

    ```bash
    cf push
    ```

    Access your application URL in the browser.  Login with the credentials for your service.  If you need to find these, just run this command and look for the VCAP_SERVICES environment variable under the `System Provided` section.

    ```bash
    cf env <app-name>
    ```

### How It Works

When you push the application here's what happens.

1. The server downloads the [PHP Build Pack] and runs it.  This installs HTTPD and PHP.
1. At this point, the build pack is done and CF runs our droplet.
1. The code we added to `config.inc.php` will read service information from the `VCAP_SERVICES` environment variable and automatically configure phpPgAdmin to use the bound services.

[PHP Buildpack]:https://github.com/cloudfoundry/php-buildpack
[ElephantSQL]:http://www.elephantsql.com/
