## CloudFoundry PHP Example Application:  PHPPgAdmin

This is an example application which can be run on CloudFoundry using the [PHP Build Pack].

This is an out-of-the-box implementation of PHPPgAdmin.  It's an example how common PHP applications can easily be run on CloudFoundry.

### Usage

1. Clone the app (i.e. this repo).

  ```bash
  git clone https://github.com/dmikusa-pivotal/cf-ex-phppgadmin
  cd cf-ex-phppgadmin
  ```

1. If you don't have one already, create a Postgres service.  With Pivotal Web Services, the following command will create a free Postgres database through [ElephantSQL].

  ```bash
  cf create-service elephantsql turtle my-test-pgsql-db
  ```

1. Edit the manifest.yml file.  Change the 'host' attribute to something unique.  Then under "services:" change "pgsql-db" to the name of your Postgres service.  This is the name of the service that will be bound to your application and thus available to PHPPgAdmin.  Adding multiple services is OK, they will all show up in the UI.

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

1. The local bits are pushed to your target.  This is small, less than 10 files around 30k. It includes the changes we made and a build pack extension for PHPPgAdmin.
1. The server downloads the [PHP Build Pack] and runs it.  This installs HTTPD and PHP.
1. The build pack sees the extension that we pushed and runs it.  The extension downloads the stock PHPPgAdmin file from their server, unzips it and installs it into the `htdocs` directory.  It then copies the rest of the files that we pushed and replaces the default PHPPgAdmin files with them.  In this case, it's just the `config.inc.php` file.
1. At this point, the build pack is done and CF runs our droplet.

### Changes

These changes were made to prepare it to run on CloudFoundry:

1. Configure the database in `config.inc.php`.  This was done by reading the environment variable VCAP_SERVICES, which is populated by CloudFoundry and contains the connection information for our services, and configuring the host, port from it.  See this [link](https://github.com/dmikusa-pivotal/cf-ex-phppgadmin/blob/master/htdocs/conf/config.inc.php#L13) for the details.

[PHP Build Pack]:https://github.com/cloudfoundry/php-buildpack
[ElephantSQL]:http://www.elephantsql.com/
