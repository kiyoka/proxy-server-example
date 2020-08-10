# Sample Python implementation of an HTTP/HTTPS forward proxy server

This project is a sample proxy server prototype to give you an idea of how a forward proxy server is implemented.

## http-proxy.py

### Usage.

startup command

```bash.
python3 http-proxy.py
```

Proxy settings to the OS

| hostname  | port |
| --------- | ---- |
| localhost | 8080 |

### Supported Features.

* HTTP protocol

* Multiple connections (multi-threaded)

* Bandwidth limitation

### Unsupported Features.

* 302 Redirect.

* HTTPS protocol (CONNECT method not implemented)

* Multiple connections (multi-threaded)

* Bandwidth limitation

* Change proxy settings

## https-proxy.py

### Usage.

startup command

```bash.
python3 https-proxy.py
```

Proxy settings to the OS

| hostname  | port |
| --------- | ---- |
| localhost | 8080 |

### Supported Features.

* 302 Redirect.

* HTTP protocol

* HTTPS protocol (CONNECT method implemented)

* Multiple connections (multi-threaded)

* Bandwidth limitation

### Unsupported Features.

* Change proxy settings
