# Quick reference

Maintained by: [Michael Oberdorf IT-Consulting](https://www.oberdorf-itc.de/)

Source code: [GitHub](https://github.com/cybcon/docker.hpmon-pushover)

Container image: [DockerHub](https://hub.docker.com/r/oitc/hpmon-pushover)

<!-- SHIELD GROUP -->
[![][github-action-test-shield]][github-action-test-link]
[![][github-action-release-shield]][github-action-release-link]
[![][github-release-shield]][github-release-link]
[![][github-releasedate-shield]][github-releasedate-link]
[![][github-stars-shield]][github-stars-link]
[![][github-forks-shield]][github-forks-link]
[![][github-issues-shield]][github-issues-link]
[![][github-license-shield]][github-license-link]

[![][docker-release-shield]][docker-release-link]
[![][docker-pulls-shield]][docker-pulls-link]
[![][docker-stars-shield]][docker-stars-link]
[![][docker-size-shield]][docker-size-link]


# Supported tags and respective `Dockerfile` links

* [`latest`, `1.1.1`](https://github.com/cybcon/docker.hpmon-pushover/blob/v1.1.1/Dockerfile)
* [`1.1.0`](https://github.com/cybcon/docker.hpmon-pushover/blob/v1.1.0/Dockerfile)
* [`1.0.2`](https://github.com/cybcon/docker.hpmon-pushover/blob/v1.0.2/Dockerfile)
* [`1.0.1`](https://github.com/cybcon/docker.hpmon-pushover/blob/v1.0.1/Dockerfile)
* [`1.0.0`](https://github.com/cybcon/docker.hpmon-pushover/blob/v1.0.0/Dockerfile)

# What is the hpmon_pushover container?

It's a simple tool, developed in python, to validate if a given URL is up and running and sends a message over
[Pushover](https://pushover.net/) service if not.

# Prerequisites to run the docker container
1. You need a Pushover account and you need to create a new application for that (UserKey, ApiKey)
2. You need to create a configuration file in json format with the webpages to check

# Configuration
## Container configuration

The container grab the configuration via environment variables.

| Environment variable name | Description | Required | Default value |
|--|--|--|--|
| `MONITORING_CONFIGURATION_URL` | The URL (can also be a file://) to the configuration in JSON format. | **MANDATORY** | |
| `PUSHOVER_USER_KEY` | The user key of your pushover account | **MANDATORY** | |
| `PUSHOVER_API_KEY` | The application key of your pushover application | **MANDATORY** | |
| `REPEAT_ON_ERROR`  | `Boolean` (`true` or `false`). If the monitor runs on an error. Repeat the call. | **OPTIONAL** | `false` |
| `REPEAT_ON_ERROR_COUNTER` | `Integer` Repeat n times. | **OPTIONAL** | 1 |
| `REPEAT_ON_ERROR_WAIT_TIME_SEC` | `Integer` Wait time in seconds between next try. | **OPTIONAL** | 2 |
| `LOGLEVEL` | The loglevel of the application inside the container, can be one of: `debug`, `info`, `warning`, `error` | **OPTIONAL** | ` info` |

## Monitoring configuration

The configuration file (referenced in environment variable `MONITORING_CONFIGURATION_URL`) is in json format. The inner main json frame is:

```json
{
  "webpages": []
}
```

Inside the `webpages` array, you can define objects with the following attributes:

| Attribute name       | Description | Required | Default value |
|----------------------|-------------|----------|---------------|
| `monitoring_url`     | The http or https URL to monitor. | **MANDATORY** | |
| `response_ok_data`   | A pattern inside the http response body that defines everything is ok. | optional | |
| `response_warn_data` | A pattern inside the http response body that defines that there is a warning. | optional | |


### Example
```json
{
  "webpages": [
    {
      "monitoring_url": "http://www.example.com/",
    },
    {
      "monitoring_url": "http://www.example.com/",
      "response_ok_data": "This domain is for use in illustrative examples in documents.",
    },
    {
      "monitoring_url": "http://www.example.com/",
      "response_ok_data": "Status: OK",
      "response_warn_data": "Status: WARNING"
    }
  ]
}
```



# Docker run

```
docker run --rm \
  -e MONITORING_CONFIGURATION_URL='https://github.com/cybcon/docker.hpmon-pushover/blob/main/example_config.json?raw=true' \
  -e PUSHOVER_USER_KEY='myPushoverUserKey' \
  -e PUSHOVER_API_KEY='myPushoverApiKey' \
  oitc/hpmon-pushover:latest
```

# Docker compose configuration

```yaml
  monitoring:
    restart: "no"
    image: oitc/hpmon-pushover:latest
    environment:
      MONITORING_CONFIGURATION_URL: https://github.com/cybcon/docker.hpmon-pushover/blob/main/example_config.json?raw=true
      PUSHOVER_USER_KEY: myPushoverUserKey
      PUSHOVER_API_KEY: myPushoverApiKey
```

# Example crontab entry
This is an example crontab entry to trigger the docker container every 5pm to send the updates for tomorrow using docker compose.
```
* 0,15,30,45 * * * /usr/bin/docker-compose -f docker-compose.yml run --rm monitoring >/dev/null 2>&1
```

# Donate
I would appreciate a small donation to support the further development of my open source projects.

<a href="https://www.paypal.com/donate/?hosted_button_id=BHGJGGUS6RH44" target="_blank"><img src="https://raw.githubusercontent.com/stefan-niedermann/paypal-donate-button/master/paypal-donate-button.png" alt="Donate with PayPal" width="200px"></a>


# License

Copyright (c) 2021-2024 Michael Oberdorf IT-Consulting

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

<!-- LINK GROUP -->
[docker-pulls-link]: https://hub.docker.com/r/oitc/hpmon-pushover
[docker-pulls-shield]: https://img.shields.io/docker/pulls/oitc/hpmon-pushover?color=45cc11&labelColor=black&style=flat-square
[docker-release-link]: https://hub.docker.com/r/oitc/hpmon-pushover
[docker-release-shield]: https://img.shields.io/docker/v/oitc/hpmon-pushover?color=369eff&label=docker&labelColor=black&logo=docker&logoColor=white&style=flat-square
[docker-size-link]: https://hub.docker.com/r/oitc/hpmon-pushover
[docker-size-shield]: https://img.shields.io/docker/image-size/oitc/hpmon-pushover?color=369eff&labelColor=black&style=flat-square
[docker-stars-link]: https://hub.docker.com/r/oitc/hpmon-pushover
[docker-stars-shield]: https://img.shields.io/docker/stars/oitc/hpmon-pushover?color=45cc11&labelColor=black&style=flat-square
[github-action-release-link]: https://github.com/cybcon/docker.hpmon-pushover/actions/workflows/release-from-label.yaml
[github-action-release-shield]: https://img.shields.io/github/actions/workflow/status/cybcon/docker.hpmon-pushover/release-from-label.yaml?label=release&labelColor=black&logo=githubactions&logoColor=white&style=flat-square
[github-action-test-link]: https://github.com/cybcon/docker.hpmon-pushover/actions/workflows/test.yaml
[github-action-test-shield-original]: https://github.com/cybcon/docker.hpmon-pushover/actions/workflows/test.yaml/badge.svg
[github-action-test-shield]: https://img.shields.io/github/actions/workflow/status/cybcon/docker.hpmon-pushover/test.yaml?label=tests&labelColor=black&logo=githubactions&logoColor=white&style=flat-square
[github-forks-link]: https://github.com/cybcon/docker.hpmon-pushover/network/members
[github-forks-shield]: https://img.shields.io/github/forks/cybcon/docker.hpmon-pushover?color=8ae8ff&labelColor=black&style=flat-square
[github-issues-link]: https://github.com/cybcon/docker.hpmon-pushover/issues
[github-issues-shield]: https://img.shields.io/github/issues/cybcon/docker.hpmon-pushover?color=ff80eb&labelColor=black&style=flat-square
[github-license-link]: https://github.com/cybcon/docker.hpmon-pushover/blob/main/LICENSE
[github-license-shield]: https://img.shields.io/badge/license-MIT-blue?labelColor=black&style=flat-square
[github-release-link]: https://github.com/cybcon/docker.hpmon-pushover/releases
[github-release-shield]: https://img.shields.io/github/v/release/cybcon/docker.hpmon-pushover?color=369eff&labelColor=black&logo=github&style=flat-square
[github-releasedate-link]: https://github.com/cybcon/docker.hpmon-pushover/releases
[github-releasedate-shield]: https://img.shields.io/github/release-date/cybcon/docker.hpmon-pushover?labelColor=black&style=flat-square
[github-stars-link]: https://github.com/cybcon/docker.hpmon-pushover
[github-stars-shield]: https://img.shields.io/github/stars/cybcon/docker.hpmon-pushover?color=ffcb47&labelColor=black&style=flat-square
