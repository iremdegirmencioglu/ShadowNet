
import argparse
import ipaddress

DEFAULT_PORTS = [21, 22, 80, 443, 3306, 5432, 8080]
MAX_PORTS = 1024


def parse_ports(value):
    if not value:
        return DEFAULT_PORTS.copy()

    ports = set()

    for item in value.split(","):
        item = item.strip()

        if "-" in item:
            parts = item.split("-")

            if len(parts) != 2:
                raise ValueError("Gecersiz port araligi.")

            start, end = map(int, parts)

            if start > end:
                raise ValueError("Baslangic portu bitisten buyuk.")

            if end - start + 1 > MAX_PORTS:
                raise ValueError("Port araligi cok buyuk.")

            ports.update(range(start, end + 1))
        else:
            ports.add(int(item))

        if len(ports) > MAX_PORTS:
            raise ValueError("En fazla 1024 port taranabilir.")

    if not ports or any(p < 1 or p > 65535 for p in ports):
        raise ValueError("Portlar 1-65535 arasinda olmali.")

    return sorted(ports)


def parse_target(value):
    address = ipaddress.ip_address(value)

    if address.version != 4 or not address.is_loopback:
        raise ValueError(
            "Bu surumde yalnizca IPv4 localhost desteklenir."
        )

    return str(address)


def get_config():
    parser = argparse.ArgumentParser(
        description="ShadowNet v1.1 - Local Security Scanner"
    )

    parser.add_argument(
        "--target",
        default="127.0.0.1",
        help="Yerel IPv4 hedefi"
    )

    parser.add_argument(
        "--ports",
        default=None,
        help="Ornek: 22,80,443 veya 8000-8010"
    )

    parser.add_argument(
        "--timeout",
        type=float,
        default=1.0,
        help="Baglanti zaman asimi (saniye)"
    )

    args = parser.parse_args()

    args.target = parse_target(args.target)
    args.ports = parse_ports(args.ports)

    if not 0.1 <= args.timeout <= 10:
        raise ValueError("Timeout 0.1-10 saniye arasinda olmali.")

    return args
