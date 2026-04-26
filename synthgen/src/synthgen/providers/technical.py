"""
Technical & Network Data Provider.

Generates technical data including:
- URLs and domains
- UUIDs
- Hashes
- JWT tokens
- API keys
- Ports and protocols
- Headers
- User agents
"""

from __future__ import annotations

import hashlib
import base64
import string
from typing import Any
from datetime import datetime, timedelta

from synthgen.core.base import BaseProvider
from synthgen.core.seed_manager import SeedManager


DOMAIN_SUFFIXES = [".com", ".org", ".net", ".io", ".dev", ".app", ".co", ".ai"]
PROTOCOLS = ["http", "https", "ftp", "ftps", "ssh", "mailto"]
HTTP_METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]
STATUS_CODES = [200, 201, 204, 301, 302, 400, 401, 403, 404, 500, 502, 503]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148",
    "Mozilla/5.0 (Android 11; Mobile; rv:68.0) Gecko/68.0 Firefox/88.0",
]

COMMON_PORTS = {
    "http": 80,
    "https": 443,
    "ssh": 22,
    "ftp": 21,
    "smtp": 25,
    "dns": 53,
    "mysql": 3306,
    "postgresql": 5432,
    "redis": 6379,
    "mongodb": 27017,
}


class TechnicalProvider(BaseProvider):
    """Provider for technical and network data."""

    def __init__(self, seed_manager: SeedManager | None = None) -> None:
        super().__init__(seed_manager)
        self._sm = seed_manager

    def _get_sm(self) -> SeedManager:
        if self._sm is None:
            raise RuntimeError("SeedManager not initialized")
        return self._sm

    def uuid(self) -> str:
        """Generate a UUID v4."""
        import uuid as uuid_module
        sm = self._get_sm()
        # Use seed manager to create deterministic UUID
        random_bytes = sm.random_bytes(16)
        # Set version to 4
        random_bytes = random_bytes[:6] + bytes([0x40 | (random_bytes[6] & 0x0F)]) + random_bytes[7:]
        # Set variant
        random_bytes = random_bytes[:8] + bytes([0x80 | (random_bytes[8] & 0x3F)]) + random_bytes[9:]
        
        hex_str = random_bytes.hex()
        return f"{hex_str[:8]}-{hex_str[8:12]}-{hex_str[12:16]}-{hex_str[16:20]}-{hex_str[20:32]}"

    def domain_name(self) -> str:
        """Generate a domain name."""
        sm = self._get_sm()
        words = ["tech", "data", "cloud", "web", "app", "net", "sys", "info", "digital", "smart"]
        name = sm.random_choice(words) + str(sm.random_int(1, 999))
        suffix = sm.random_choice(DOMAIN_SUFFIXES)
        return name + suffix

    def url(self, include_path: bool = True) -> str:
        """Generate a URL."""
        sm = self._get_sm()
        protocol = sm.random_choice(["http", "https"])
        domain = self.domain_name()
        
        if include_path:
            paths = ["api", "v1", "users", "data", "files", "images", "docs"]
            path = "/".join(sm.random_sample(paths, sm.random_int(1, 3)))
            return f"{protocol}://{domain}/{path}"
        return f"{protocol}://{domain}"

    def hash_value(self, algorithm: str = "sha256", data: str | None = None) -> str:
        """Generate a hash value."""
        sm = self._get_sm()
        if data is None:
            data = "".join(str(sm.random_int(0, 9)) for _ in range(32))
        
        if algorithm.lower() == "md5":
            return hashlib.md5(data.encode()).hexdigest()
        elif algorithm.lower() == "sha1":
            return hashlib.sha1(data.encode()).hexdigest()
        elif algorithm.lower() == "sha256":
            return hashlib.sha256(data.encode()).hexdigest()
        elif algorithm.lower() == "sha512":
            return hashlib.sha512(data.encode()).hexdigest()
        else:
            return hashlib.sha256(data.encode()).hexdigest()

    def api_key(self, prefix: str = "sk", length: int = 32) -> str:
        """Generate an API key."""
        sm = self._get_sm()
        chars = string.ascii_letters + string.digits
        key = "".join(sm.random_sample(list(chars), length))
        return f"{prefix}_{key}"

    def jwt_token(self, payload: dict[str, Any] | None = None) -> str:
        """Generate a fake JWT token."""
        sm = self._get_sm()
        import json
        
        header = {"alg": "HS256", "typ": "JWT"}
        if payload is None:
            payload = {
                "sub": self.uuid(),
                "iat": int(datetime.now().timestamp()),
                "exp": int((datetime.now() + timedelta(hours=1)).timestamp()),
            }
        
        def b64encode(data: dict) -> str:
            return base64.urlsafe_b64encode(json.dumps(data).encode()).rstrip(b"=").decode()
        
        header_b64 = b64encode(header)
        payload_b64 = b64encode(payload)
        signature = self.hash_value("sha256", f"{header_b64}.{payload_b64}")[:43]
        
        return f"{header_b64}.{payload_b64}.{signature}"

    def port(self, service: str | None = None) -> int:
        """Generate a port number."""
        sm = self._get_sm()
        if service and service.lower() in COMMON_PORTS:
            return COMMON_PORTS[service.lower()]
        # Well-known ports (0-1023) or registered ports (1024-49151)
        return sm.random_int(1024, 49151)

    def user_agent(self) -> str:
        """Generate a User-Agent string."""
        sm = self._get_sm()
        return sm.random_choice(USER_AGENTS)

    def http_header(self) -> dict[str, str]:
        """Generate HTTP headers."""
        sm = self._get_sm()
        return {
            "Content-Type": sm.random_choice(["application/json", "text/html", "application/xml"]),
            "Authorization": f"Bearer {self.api_key(length=24)}",
            "User-Agent": self.user_agent(),
            "Accept": "application/json",
            "X-Request-ID": self.uuid(),
        }

    def ip_address(self, version: str = "v4") -> str:
        """Generate an IP address."""
        sm = self._get_sm()
        if version.lower() == "v4":
            return ".".join(str(sm.random_int(0, 255)) for _ in range(4))
        else:
            groups = [f"{sm.random_int(0, 65535):04x}" for _ in range(8)]
            return ":".join(groups)

    def mac_address(self) -> str:
        """Generate a MAC address."""
        sm = self._get_sm()
        octets = [f"{sm.random_int(0, 255):02x}" for _ in range(6)]
        return ":".join(octets)

    def generate(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """Generate complete technical profile."""
        return {
            "uuid": self.uuid(),
            "domain": self.domain_name(),
            "url": self.url(),
            "api_key": self.api_key(),
            "jwt": self.jwt_token(),
            "hash_sha256": self.hash_value(),
            "port": self.port(),
            "user_agent": self.user_agent(),
            "headers": self.http_header(),
            "ip_v4": self.ip_address("v4"),
            "mac_address": self.mac_address(),
        }
