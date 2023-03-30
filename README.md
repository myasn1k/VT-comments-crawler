# VT-comments-crawler

Get VT comments and samples connected by author name and store them in an ElasticSearch index.
ElastAlert could be used to alert about relevant samples using comment tags.

## Configuration

In `config_vol/`, please copy `config.sample.yaml` to `config.yaml`, and edit the following:

* Elastic protocol
* Elastic host
* Elastic port
* Elatic user and password
* Indexes names
* VT api key
* List of usernames to track

## Usage

1. Build the container: `docker-compose build app`
2. Add crontab
	- Example crontab entry: `*/30 * * * * cd /PATH/TO/VT-comments-crawler && ./run.sh`
