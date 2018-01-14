# IP / ICMP Verification Tool

The goal of this project was to create a easy to use validation script for ICMP traffic based on a CSV import

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Netmiko (https://github.com/ktbyers/netmiko)
You can install this with pip via "pip install netmiko"

## Deployment

Just execute the script and answer the questions

## Built With

* Netmiko (https://github.com/ktbyers/netmiko) - Thanks Kyle Byers for the excellent library

## Features
- CSV file import for ICMP check (see template for examples)
- Export of CSV

## *Caveats
- Supported Devices (The following devices, I have not validated anything more)
Cisco ASA
Cisco IOS	 (Use IOS for Type)
Cisco IOS-XE (Use XE for Type)
Cisco IOS-XR (Use XR for Type)
Cisco NX-OS  (Use NXOS for Type)
HP Comware7  (Use Comware for Type)
HP ProCurve  (Use ProCurve for Type)

## Versioning

Version 1.1 - Added multithreaded version

## Authors

* **Matt Cross** - [RouteAllThings](https://github.com/routeallthings)

See also the list of [contributors](https://github.com/routeallthings/IP_Ping_Verification/contributors) who participated in this project.

## License

This project is licensed under the GNU - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments
