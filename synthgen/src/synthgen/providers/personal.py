"""
Personal & Demographic Data Provider.

Generates realistic personal information including:
- Names (first, last, full)
- Email addresses
- Phone numbers
- Addresses
- Dates of birth
- Gender
- IDs (SSN, passport, etc.)
- Avatars/Profile images (URLs)
"""

from __future__ import annotations

import string
from typing import Any
from datetime import date, timedelta

from synthgen.core.base import BaseProvider
from synthgen.core.seed_manager import SeedManager


# First names by gender
FIRST_NAMES_MALE = [
    "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph",
    "Thomas", "Charles", "Christopher", "Daniel", "Matthew", "Anthony", "Donald",
    "Mark", "Paul", "Steven", "Andrew", "Kenneth", "Joshua", "Kevin", "Brian",
    "George", "Edward", "Ronald", "Timothy", "Jason", "Jeffrey", "Ryan", "Jacob"
]

FIRST_NAMES_FEMALE = [
    "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan",
    "Jessica", "Sarah", "Karen", "Nancy", "Lisa", "Betty", "Margaret", "Sandra",
    "Ashley", "Dorothy", "Kimberly", "Emily", "Donna", "Michelle", "Carol",
    "Amanda", "Melissa", "Deborah", "Stephanie", "Rebecca", "Sharon", "Laura",
    "Cynthia", "Kathleen", "Amy", "Angela", "Anna", "Brenda", "Emma"
]

FIRST_NAMES_UNISEX = [
    "Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Avery", "Quinn",
    "Skyler", "Dakota", "Reese", "Hayden", "Emerson", "Finley", "Rowan"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
    "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
    "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
    "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
    "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker",
    "Cruz", "Edwards", "Collins", "Reyes", "Stewart", "Morris", "Morales", "Murphy"
]

DOMAINS = [
    "gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "aol.com",
    "icloud.com", "protonmail.com", "mail.com", "zoho.com", "yandex.com"
]

STREET_SUFFIXES = [
    "Street", "Avenue", "Boulevard", "Drive", "Lane", "Road", "Way", "Court",
    "Place", "Circle", "Parkway", "Trail", "Square", "Terrace", "Heights"
]

CITY_PREFIXES = [
    "North", "South", "East", "West", "New", "Old", "Lake", "Fort", "Port", "San"
]

CITIES = [
    "Springfield", "Franklin", "Clinton", "Madison", "Georgetown", "Fairview",
    "Bristol", "Salem", "Marion", "Milford", "Auburn", "Lexington", "Warren",
    "Dayton", "Akron", "Toledo", "Columbus", "Indianapolis", "Louisville",
    "Nashville", "Memphis", "Atlanta", "Charlotte", "Richmond", "Raleigh"
]

STATES = [
    ("Alabama", "AL"), ("Alaska", "AK"), ("Arizona", "AZ"), ("Arkansas", "AR"),
    ("California", "CA"), ("Colorado", "CO"), ("Connecticut", "CT"), ("Delaware", "DE"),
    ("Florida", "FL"), ("Georgia", "GA"), ("Hawaii", "HI"), ("Idaho", "ID"),
    ("Illinois", "IL"), ("Indiana", "IN"), ("Iowa", "IA"), ("Kansas", "KS"),
    ("Kentucky", "KY"), ("Louisiana", "LA"), ("Maine", "ME"), ("Maryland", "MD"),
    ("Massachusetts", "MA"), ("Michigan", "MI"), ("Minnesota", "MN"), ("Mississippi", "MS"),
    ("Missouri", "MO"), ("Montana", "MT"), ("Nebraska", "NE"), ("Nevada", "NV"),
    ("New Hampshire", "NH"), ("New Jersey", "NJ"), ("New Mexico", "NM"), ("New York", "NY"),
    ("North Carolina", "NC"), ("North Dakota", "ND"), ("Ohio", "OH"), ("Oklahoma", "OK"),
    ("Oregon", "OR"), ("Pennsylvania", "PA"), ("Rhode Island", "RI"), ("South Carolina", "SC"),
    ("South Dakota", "SD"), ("Tennessee", "TN"), ("Texas", "TX"), ("Utah", "UT"),
    ("Vermont", "VT"), ("Virginia", "VA"), ("Washington", "WA"), ("West Virginia", "WV"),
    ("Wisconsin", "WI"), ("Wyoming", "WY")
]

COUNTRIES = [
    "United States", "Canada", "United Kingdom", "Australia", "Germany",
    "France", "Italy", "Spain", "Japan", "China", "India", "Brazil",
    "Mexico", "Argentina", "South Africa", "Nigeria", "Egypt", "Russia"
]


class PersonalProvider(BaseProvider):
    """
    Provider for personal and demographic data.

    Generates realistic synthetic personal information suitable for
    testing, mocking, and development purposes.

    Example:
        >>> provider = PersonalProvider(seed_manager)
        >>> provider.name()
        'John Smith'
        >>> provider.email()
        'john.smith@gmail.com'
    """

    def __init__(self, seed_manager: SeedManager | None = None) -> None:
        """
        Initialize the personal data provider.

        Args:
            seed_manager: Seed manager for reproducibility.
        """
        super().__init__(seed_manager)
        self._sm = seed_manager

    def _get_sm(self) -> SeedManager:
        """Get seed manager or raise error if not set."""
        if self._sm is None:
            raise RuntimeError("SeedManager not initialized")
        return self._sm

    def first_name(self, gender: str | None = None) -> str:
        """
        Generate a random first name.

        Args:
            gender: Optional gender ('male', 'female', or None for any).

        Returns:
            A random first name.
        """
        sm = self._get_sm()
        if gender == "male":
            return sm.random_choice(FIRST_NAMES_MALE)
        elif gender == "female":
            return sm.random_choice(FIRST_NAMES_FEMALE)
        else:
            all_names = FIRST_NAMES_MALE + FIRST_NAMES_FEMALE + FIRST_NAMES_UNISEX
            return sm.random_choice(all_names)

    def last_name(self) -> str:
        """
        Generate a random last name.

        Returns:
            A random last name.
        """
        sm = self._get_sm()
        return sm.random_choice(LAST_NAMES)

    def name(self, gender: str | None = None, include_middle: bool = False) -> str:
        """
        Generate a full name.

        Args:
            gender: Optional gender specification.
            include_middle: Whether to include a middle name/initial.

        Returns:
            A full name string.
        """
        sm = self._get_sm()
        first = self.first_name(gender)
        last = self.last_name()

        if include_middle:
            if sm.random_bool(0.5):
                # Middle initial
                middle = sm.random_choice(string.ascii_uppercase) + "."
                return f"{first} {middle} {last}"
            else:
                # Full middle name
                middle = self.first_name()
                return f"{first} {middle} {last}"

        return f"{first} {last}"

    def email(self, name: str | None = None, domain: str | None = None) -> str:
        """
        Generate an email address.

        Args:
            name: Optional name to base the email on.
            domain: Optional domain (random if not specified).

        Returns:
            An email address.
        """
        sm = self._get_sm()
        if name is None:
            first = self.first_name().lower()
            last = self.last_name().lower()
            name_part = f"{first}.{last}"
        else:
            # Extract from provided name
            parts = name.lower().split()
            if len(parts) >= 2:
                name_part = f"{parts[0]}.{parts[-1]}"
            else:
                name_part = parts[0] if parts else "user"

        # Add random numbers occasionally
        if sm.random_bool(0.3):
            name_part += str(sm.random_int(1, 999))

        chosen_domain = domain or sm.random_choice(DOMAINS)
        return f"{name_part}@{chosen_domain}"

    def phone_number(self, country_code: str = "+1") -> str:
        """
        Generate a phone number.

        Args:
            country_code: International country code prefix.

        Returns:
            A formatted phone number.
        """
        sm = self._get_sm()
        area = sm.random_int(200, 999)
        exchange = sm.random_int(200, 999)
        subscriber = sm.random_int(1000, 9999)
        return f"{country_code} ({area}) {exchange}-{subscriber}"

    def address(self) -> dict[str, str]:
        """
        Generate a complete address.

        Returns:
            Dictionary with street, city, state, zip, country.
        """
        sm = self._get_sm()
        street_num = sm.random_int(100, 9999)
        street_name = self._generate_street_name()
        city = self._generate_city()
        state_full, state_abbr = sm.random_choice(STATES)
        zip_code = sm.random_int(10000, 99999)
        country = sm.random_choice(COUNTRIES)

        return {
            "street": f"{street_num} {street_name}",
            "city": city,
            "state": state_full,
            "state_abbr": state_abbr,
            "zip": str(zip_code),
            "country": country,
        }

    def _generate_street_name(self) -> str:
        """Generate a street name."""
        sm = self._get_sm()
        suffix = sm.random_choice(STREET_SUFFIXES)
        # Use a last name or nature word as street name
        name_options = LAST_NAMES + ["Oak", "Maple", "Cedar", "Pine", "Elm", "Willow"]
        name = sm.random_choice(name_options)
        return f"{name} {suffix}"

    def _generate_city(self) -> str:
        """Generate a city name."""
        sm = self._get_sm()
        if sm.random_bool(0.4):
            # Prefix + city
            prefix = sm.random_choice(CITY_PREFIXES)
            city = sm.random_choice(CITIES)
            return f"{prefix} {city}"
        else:
            return sm.random_choice(CITIES)

    def date_of_birth(
        self, min_age: int = 18, max_age: int = 80
    ) -> date:
        """
        Generate a date of birth.

        Args:
            min_age: Minimum age in years.
            max_age: Maximum age in years.

        Returns:
            A date object representing DOB.
        """
        sm = self._get_sm()
        today = date.today()
        days_in_year = 365

        # Calculate date range
        max_days = max_age * days_in_year
        min_days = min_age * days_in_year

        days_ago = sm.random_int(min_days, max_days)
        dob = today - timedelta(days=days_ago)
        return dob

    def gender(self, include_other: bool = False) -> str:
        """
        Generate a gender value.

        Args:
            include_other: Whether to include non-binary options.

        Returns:
            Gender string.
        """
        sm = self._get_sm()
        options = ["male", "female"]
        if include_other:
            options.extend(["non-binary", "other", "prefer not to say"])
        return sm.random_choice(options)

    def ssn(self) -> str:
        """
        Generate a fake Social Security Number (US format).

        NOTE: This generates synthetic data that follows the SSN format
        but is NOT a real SSN. Safe for testing only.

        Returns:
            Fake SSN in XXX-XX-XXXX format.
        """
        sm = self._get_sm()
        area = sm.random_int(1, 899)
        group = sm.random_int(1, 99)
        serial = sm.random_int(1, 9999)
        return f"{area:03d}-{group:02d}-{serial:04d}"

    def passport_number(self, country: str = "US") -> str:
        """
        Generate a fake passport number.

        Args:
            country: Country code for passport format.

        Returns:
            Fake passport number.
        """
        sm = self._get_sm()
        if country.upper() == "US":
            # US format: 9 digits
            return str(sm.random_int(100000000, 999999999))
        else:
            # Generic format: 2 letters + 6 digits
            letters = "".join(sm.random_sample(list(string.ascii_uppercase), 2))
            digits = sm.random_int(100000, 999999)
            return f"{letters}{digits:06d}"

    def avatar_url(self, size: int = 200) -> str:
        """
        Generate a placeholder avatar URL.

        Args:
            size: Image size in pixels.

        Returns:
            URL to a placeholder avatar service.
        """
        sm = self._get_sm()
        # Using ui-avatars.com for deterministic avatars based on name
        name = self.name()
        initials = "".join(n[0].upper() for n in name.split()[:2])
        return f"https://ui-avatars.com/api/?name={initials}&size={size}"

    def generate(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """
        Generate a complete personal profile.

        Args:
            *args: Unused positional arguments.
            **kwargs: Options like 'gender', 'include_middle', etc.

        Returns:
            Dictionary with all personal data fields.
        """
        gender = kwargs.get("gender")
        include_middle = kwargs.get("include_middle", False)

        name = self.name(gender=gender, include_middle=include_middle)

        return {
            "name": name,
            "first_name": name.split()[0],
            "last_name": name.split()[-1],
            "gender": gender or self.gender(),
            "email": self.email(name),
            "phone": self.phone_number(),
            "address": self.address(),
            "date_of_birth": self.date_of_birth().isoformat(),
            "ssn": self.ssn(),
            "passport": self.passport_number(),
            "avatar": self.avatar_url(),
        }
