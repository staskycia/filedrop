<div align="center">
  <img src="./.github/light.png#gh-light-mode-only" alt="FileDrop Anything Light" />
  <img src="./.github/dark.png#gh-dark-mode-only" alt="FileDrop Anything Dark" />
  <h3>
    <a href="https://github.com/staskycia/filedrop">FileDrop</a>
  </h3>
    <p>An easy way to share files between all your devices</p>
    <br/>
    <a href="https://vimeo.com/1101557107?ts=0&share=copy">View Demo</a>
    &middot;
    <a href="https://github.com/staskycia/filedrop/issues/new?labels=bug&template=bug_report.md">Report Bug</a>
    &middot;
    <a href="https://github.com/staskycia/filedrop/issues/new?labels=enhancement&template=feature_request.md">Request Feature</a>
</div>

<details>
    <summary>Table of Contents</summary>
    <ol>
      <li><a href="#about-the-project">About The Project</a></li>
      <li><a href="#running">Running</a></li>
      <li><a href="#getting-started">Getting Started</a></li>
      <li><a href="#usage">Usage</a></li>
      <li><a href="#contact">Contact</a></li>
    </ol>
</details>

## About The Project

FileDrop is a web app you can run, to receive files from any other device in the same Wi-Fi network, across all platforms.

### Build With

- [![Flask][flask]][flask-url]
- [![Tailwind CSS][tailwind]][tailwind-url]
- [![Dropzone.js][dropzone]][dropzone-url]

## Getting Started

On Windows, you may need to use `py` instead of `python`, and ensure Python is added to your PATH during installation.

On MacOS, use `python3` and `pip3` instead of `python` and `pip` or run this commands after installation of Python and pip:
```sh
alias python=python3
alias pip=pip3
```

### Prerequisites

Before you begin, make sure you have the following installed on your system:

- **Python** (version 3.8 or higher)  
  Download from [python.org](https://www.python.org/downloads/)

- **pip** (Python package manager)  
  Comes bundled with Python 3.4+  
  Check with: `pip --version`

- **Git** (for cloning the repository)  
  Installation guide: [github.com](https://github.com/git-guides/install-git)

To verify installation:

```sh
python --version
pip --version
git --version
```

### Installation

1. Clone the repo

```sh
git clone https://github.com/staskycia/filedrop.git
cd filedrop
```

2. Virtual Environment (optional, but recommended)

```sh
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

3. Install packages

```sh
pip install -r requirements.txt
```

## Running

Before the first launch, initialize the database

```sh
python init_db.py
```

Start a Waitress WSGI

```sh
waitress-serve --host 0.0.0.0 --call app:create_app
```

Now you should be able to open FileDrop at http://127.0.0.1:8080

## Usage

### Admin Panel

The first thing you should do after installing FileDrop is logging in to the Admin Panel.

Navigate to http://127.0.0.1:8080/panel and log in

#### Password

Default Admin Panel password is `admin` but you should change it as soon as possible. To do so, after logging in open `Security` tab and fill the form.

If you ever happen to forget the password, you may reset it at http://127.0.0.1:8080/recovery

_Note: Password recovery is only available on the host computer and when using `127.0.0.1` (not any other IP of your machine)_

#### Configuration

##### Files Receiving

You can enable or disable files receiving at any time with this button

##### Allowed Extensions

Here you can select all extensions that FileDrop will accept. By default `pdf, txt, zip, csv, gif, jpg, jpeg, HEIC, png, svg, pptx, docx, xlsx, mp4` are allowed.

#### Add/Delete Extension

This allows you to add and remove extensions from the above list.

#### Upload folder

This is the directory where all received files will be saved. By default, it's set to `.../filedrop/uploads`

### Security

#### Security Mode

This option allows you to choose one of 3 available restrictions:

- **None** (default) - any device can share files
- **Whitelist** - only devices that are on the whitelist can share files
- **Blacklist** - all devices that are not on the blacklist can share files

_Note: IPs are different in different Wi-Fi networks_

#### IP Whitelist/Blacklist

Here you can select IPs for corresponding lists.

#### Add/Delete IP

This allows you to add or remove IPs from above lists.

### Logs

All available log files are shown here.

### Sharing manual

Here you can find a guide on how to share files, that you can show others.

## Contact

If you found this project useful in any way, I would appreciate your opinion and suggestions. Feel free to contact me via [email](mailto:stanislaw.stask@gmail.com)

[flask]: https://img.shields.io/badge/flask-000000?style=for-the-badge&logo=flask&logoColor=white
[flask-url]: https://flask.palletsprojects.com/en/stable/$0
[tailwind]: https://img.shields.io/badge/Tailwind%20CSS-62baf3?style=for-the-badge&logo=tailwindcss&logoColor=white
[tailwind-url]: https://tailwindcss.com/
[dropzone]: https://img.shields.io/badge/Dropzone.js-4230f5?style=for-the-badge
[dropzone-url]: https://dropzone.dev
