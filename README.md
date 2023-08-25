|![gplv3-or-later](https://www.gnu.org/graphics/gplv3-or-later.png)|
|-|

# Masquerade experiements

Masquerade experiements is a docker based test bed for proxies. It is foccused mainly on testing the proxy [Masquerade](https://github.com/jromwu/masquerade) but is designed to be modulable.


## Requirements

To run the experiement, you will need `docker` and `docker-compose`.
The experiement is also designed to run in background and need for that `screen`


## Usage

To run the experiement, we use a [Makefile](Makefile), be careful, it may not react well to parallelised make, so be sure to run in serialized.
> :warning: The makefile makes use of a kill rule that remove all containers containing `masquerade_experiements` in their name, you may want to modify this rule to prevent killing unwanted containers.

### Image Building

By default, the images ares going to be build locally, this build can take up to an hour, you can chose to use publicly available version of the images on [Docker Hub](https://hub.docker.com/) to do so, replace the occurance of the `build` rule in the [Makefile](Makefile) by the `pull` rule.


### Run caracteristique

The [brosertime.env](browsertime.env) and [basic_test.env](basic_test.env) files provide way of modifying the number of iterations of each test, they already have default value, also setting `MESURE` to false will deactivate the browsertime test and respectivly the speedtest and bulkdownload test.

Moreover in the browsertime file, you can configure the country you are running on by setting `COUNTRY`, possible values are `DE`, `FR`, `IT` and `US`, the default being `IT`.


### Full run

To run the experiement, just use the command `make full`, or to run in detached mode `make silent`.
This way of running the experiement will run the experiement following the script [run.sh](run.sh), you can modify it to choose which set of parameter to use.


### Partial run

To run the experiement in one particular condition, you can create a file `network.env` and set the network conditions.
You can choose between setting
 - the Upload, Download, RTT and Loss, setting the variable `UPLOAD` (in Mbps), `DOWNLOAD` (in Mbps), `RTT` (in ms) and `LOSS` (in %), in this configuration `UPLOAD`, `RTT` and `LOSS` are mandatory, if not set, `DOWLOAD` will default to `UPLOAD`;
 - the Technology, Quality, Operator and Country, setting the variable `TECHNOLOGY`, `QUALITY`, `OPERATOR`, `COUNTRY`, and `PERIODIC` (in sec), in this configuration only `TECHNOLOGY` is mandatory, the others will default to `universal` and `PERIODIC` will default to 10sec; this configuration uses [ERRANT](https://github.com/marty90/errant) to enforce the trafic shapping, please refer to their README.md for more information about valid parameters.

Once the `network.env` file is set, you just need to use the command `make run`


### Clean

The [Makefile](Makefile) provides a `make clean` commands that will make sure that any running containers corresponding to the experiement are stopped and prune all container, images, volumes and network.
> :warning: This can cause the loss of unwanted datas


## Datas

All the results of the experiement are stored in the `results` folder.

You can use the command `make full_compile` to create plots about the experiements you just run, the plot will be found in the `results/results/` subfolders.

You can also choose to use the YAML files found in `results/results` to run them with [Masquerade Data Analysis](https://github.com/Ultraxime/masquerade-data-analysis) to an analyse of the results.


## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

<!-- Please make sure to update tests as appropriate. -->

### Adding Test

To add a test, you need to:
 - create the corresponding python class in `results-compilation` to represent the test's result, it can inherite the class `Result` for simplicity purpose;
 - create an Docker image to run the test;
 - add the build recipe to the `docker-compose-build.yml` file;
 - add the run recipe to the `docker-compose-measure.yml` file, make sure it runs before the `bulk_download` container and after one of the previous test finished.


### Adding Metric

To add a new metric, you will need to:
 - create the corresponding test if need be;
 - add the support in the test-corresponding python class in `results-compilation`.


### Adding Setup

To add a setup, you will need to:
 - modify the classes in `results-compilation` by adding a new field for this scenario and modify all subsequent class et method;
 - modify the `entrypoint.sh` of all the test for them to test also your new setup;
 - create the Docker images nedeed;
 - add their build recipes to the `docker-compose-build.yml` file;
 - add their run recipes to the `docker-compose-measure.yml` file, make sure they are started before the run of the first test.


### Pre-Commit

The project already contains a pre-commit-config, to install the necessary dependencies, run `pip install -Ur pre-commit-requirements.txt`

But is not working properly because some images need python >=3.7 <3.10 while other need python >=3.10


## Authors

 - [@Ultraxime](https://github.com/Ultraxime)


## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
