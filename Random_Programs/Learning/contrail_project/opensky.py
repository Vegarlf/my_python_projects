from __future__ import annotations

import logging
import math
import os
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Final
import numpy as np
import requests
from pycontrails.models import issr as pycontrails_issr
from pycontrails.models import sac as pycontrails_sac


AVIATIONSTACK_BASE_URL: Final[str] = "https://api.aviationstack.com/v1/flights"
OPEN_METEO_GFS_URL: Final[str] = "https://api.open-meteo.com/v1/gfs"
REQUEST_TIMEOUT_SECONDS: Final[float] = 15.0

PRESSURE_LEVELS_HPA: Final[tuple[int, ...]] = (400, 350, 300, 250, 200)

JET_A_Q_FUEL_J_PER_KG: Final[float] = 43_130_000.0
JET_A_EI_H2O_KG_PER_KG: Final[float] = 1.23
DEFAULT_ENGINE_EFFICIENCY: Final[float] = 0.30

EPSILON: Final[float] = 0.622


logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class FlightPosition:
    source: str
    flight_label: str
    latitude: float
    longitude: float
    altitude_m: float
    timestamp_utc: str | None


@dataclass(frozen=True)
class WeatherAtLevel:
    pressure_level_hpa: int
    geopotential_height_m: float
    temperature_c: float
    dew_point_c: float
    relative_humidity_percent: float | None
    time_utc: str


@dataclass(frozen=True)
class SacAssessment:
    can_form: bool
    air_temperature_c: float
    air_pressure_pa: float
    rh_liquid_percent: float
    rh_critical_percent: float
    specific_humidity_kgkg: float
    mixing_line_slope_g: float
    t_sat_liquid_c: float
    reason: str


@dataclass(frozen=True)
class PersistenceAssessment:
    rh_ice_percent: float
    severity: int
    is_issr: bool
    reason: str


@dataclass(frozen=True)
class ContrailAssessment:
    position: FlightPosition
    weather: WeatherAtLevel
    sac: SacAssessment
    persistence: PersistenceAssessment


class ContrailMVPError(RuntimeError):
    pass


def prompt_menu_choice() -> str:
    print("\n=== CONTRAIL MVP ===")
    print("1) Manual mode (lat/lon/alt)")
    print("2) Flight mode (flight number / IATA / ICAO)")
    print("3) Exit")

    choice: str = input("Choose an option [1/2/3]: ").strip()
    return choice


def prompt_float(prompt_text: str) -> float:
    while True:
        raw: str = input(prompt_text).strip()
        try:
            return float(raw)
        except ValueError:
            print("Invalid number. Try again.")


def prompt_nonempty(prompt_text: str) -> str:
    while True:
        raw: str = input(prompt_text).strip()
        if raw:
            return raw
        print("Input cannot be empty. Try again.")


def prompt_flight_lookup_mode() -> tuple[str | None, str | None, str | None]:
    print("\nChoose flight identifier type:")
    print("1) Flight number only (e.g. 171)")
    print("2) Flight IATA (e.g. AA171)")
    print("3) Flight ICAO (e.g. AAL171)")

    while True:
        choice: str = input("Choose [1/2/3]: ").strip()
        if choice == "1":
            return prompt_nonempty("Enter flight number: "), None, None
        if choice == "2":
            return None, prompt_nonempty("Enter flight IATA: "), None
        if choice == "3":
            return None, None, prompt_nonempty("Enter flight ICAO: ")
        print("Invalid choice. Try again.")


def get_aviationstack_api_key() -> str:
    api_key: str | None = os.getenv("AVIATIONSTACK_API_KEY")
    if not api_key:
        raise ContrailMVPError("Missing AVIATIONSTACK_API_KEY environment variable.")
    return api_key


def fetch_live_flight_position(
    *,
    flight_number: str | None,
    flight_iata: str | None,
    flight_icao: str | None,
) -> FlightPosition:
    api_key: str = get_aviationstack_api_key()

    params: dict[str, str] = {"access_key": api_key}
    if flight_number:
        params["flight_number"] = flight_number
    if flight_iata:
        params["flight_iata"] = flight_iata
    if flight_icao:
        params["flight_icao"] = flight_icao

    logger.info("[flight] Requesting live flight data")

    response: requests.Response = requests.get(
        AVIATIONSTACK_BASE_URL,
        params=params,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()

    payload: dict[str, Any] = response.json()

    if "error" in payload:
        raise ContrailMVPError(f"Aviationstack error: {payload['error']}")

    candidates: list[dict[str, Any]] = payload.get("data", [])
    if not candidates:
        raise ContrailMVPError("No matching flights returned by Aviationstack.")

    best: dict[str, Any] | None = None
    for flight in candidates:
        live: dict[str, Any] | None = flight.get("live")
        if not live:
            continue
        if live.get("is_ground") is True:
            continue
        if live.get("latitude") is None or live.get("longitude") is None:
            continue
        if live.get("altitude") is None:
            continue
        best = flight
        break

    if best is None:
        raise ContrailMVPError(
            "Found flights, but none had usable airborne lat/lon/altitude."
        )

    live_data: dict[str, Any] = best["live"]
    flight_info: dict[str, Any] = best.get("flight", {})
    airline_info: dict[str, Any] = best.get("airline", {})

    label_parts: list[str] = []
    airline_name: str | None = airline_info.get("name")
    iata_code: str | None = flight_info.get("iata")
    icao_code: str | None = flight_info.get("icao")
    number_code: str | None = flight_info.get("number")

    if airline_name:
        label_parts.append(str(airline_name))
    if iata_code:
        label_parts.append(str(iata_code))
    elif icao_code:
        label_parts.append(str(icao_code))
    elif number_code:
        label_parts.append(str(number_code))

    label: str = " ".join(label_parts).strip() or "Unknown flight"

    logger.info("[flight] Live flight data received")

    return FlightPosition(
        source="aviationstack",
        flight_label=label,
        latitude=float(live_data["latitude"]),
        longitude=float(live_data["longitude"]),
        altitude_m=float(live_data["altitude"]),
        timestamp_utc=(
            str(live_data.get("updated")) if live_data.get("updated") else None
        ),
    )


def build_manual_position(
    *,
    latitude: float,
    longitude: float,
    altitude_m: float,
) -> FlightPosition:
    return FlightPosition(
        source="manual",
        flight_label="manual-input",
        latitude=latitude,
        longitude=longitude,
        altitude_m=altitude_m,
        timestamp_utc=datetime.now(timezone.utc).isoformat(),
    )


def build_open_meteo_hourly_fields() -> list[str]:
    fields: list[str] = []
    for level in PRESSURE_LEVELS_HPA:
        fields.extend(
            [
                f"temperature_{level}hPa",
                f"dew_point_{level}hPa",
                f"relative_humidity_{level}hPa",
                f"geopotential_height_{level}hPa",
            ]
        )
    return fields


def fetch_weather_profile(
    *,
    latitude: float,
    longitude: float,
) -> dict[str, Any]:
    hourly_fields: list[str] = build_open_meteo_hourly_fields()

    params: dict[str, str] = {
        "latitude": str(latitude),
        "longitude": str(longitude),
        "hourly": ",".join(hourly_fields),
        "forecast_days": "1",
        "timezone": "UTC",
    }

    logger.info(
        "[weather] Requesting Open-Meteo for lat=%.5f lon=%.5f",
        latitude,
        longitude,
    )

    response: requests.Response = requests.get(
        OPEN_METEO_GFS_URL,
        params=params,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()

    logger.info("[weather] Open-Meteo response received successfully")

    payload: dict[str, Any] = response.json()
    if "hourly" not in payload or "time" not in payload["hourly"]:
        raise ContrailMVPError("Open-Meteo response missing hourly weather data.")

    return payload


def parse_iso_utc(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    dt: datetime = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def choose_nearest_time_index(times: list[str], target_utc: datetime) -> int:
    best_index: int = 0
    best_delta: float = float("inf")

    for index, raw_time in enumerate(times):
        candidate: datetime = parse_iso_utc(raw_time)
        delta_seconds: float = abs((candidate - target_utc).total_seconds())
        if delta_seconds < best_delta:
            best_delta = delta_seconds
            best_index = index

    return best_index


def nearest_weather_level_for_altitude(
    *,
    weather_payload: dict[str, Any],
    altitude_m: float,
    target_time_utc: datetime,
) -> WeatherAtLevel:
    hourly: dict[str, Any] = weather_payload["hourly"]
    times: list[str] = hourly["time"]
    time_index: int = choose_nearest_time_index(times, target_time_utc)

    best_level: int | None = None
    best_height_diff: float = float("inf")

    for level in PRESSURE_LEVELS_HPA:
        gh_key: str = f"geopotential_height_{level}hPa"
        heights: list[float | None] = hourly.get(gh_key, [])
        if time_index >= len(heights):
            continue
        gh_value: float | None = heights[time_index]
        if gh_value is None:
            continue

        diff: float = abs(float(gh_value) - altitude_m)
        if diff < best_height_diff:
            best_height_diff = diff
            best_level = level

    if best_level is None:
        raise ContrailMVPError(
            "Could not match aircraft altitude to any pressure level."
        )

    def read_value(field_name: str) -> float:
        values: list[float | None] = hourly.get(field_name, [])
        if time_index >= len(values):
            raise ContrailMVPError(
                f"Weather field {field_name} missing target time index."
            )
        value: float | None = values[time_index]
        if value is None:
            raise ContrailMVPError(
                f"Weather field {field_name} is null at target time."
            )
        return float(value)

    rh_values: list[float | None] = hourly.get(f"relative_humidity_{best_level}hPa", [])
    humidity_value: float | None
    if time_index < len(rh_values) and rh_values[time_index] is not None:
        humidity_value = float(rh_values[time_index])
    else:
        humidity_value = None

    return WeatherAtLevel(
        pressure_level_hpa=best_level,
        geopotential_height_m=read_value(f"geopotential_height_{best_level}hPa"),
        temperature_c=read_value(f"temperature_{best_level}hPa"),
        dew_point_c=read_value(f"dew_point_{best_level}hPa"),
        relative_humidity_percent=humidity_value,
        time_utc=times[time_index],
    )


def saturation_vapor_pressure_over_water_pa(temp_k: float) -> float:
    return math.exp(
        54.842763
        - 6763.22 / temp_k
        - 4.210 * math.log(temp_k)
        + 0.000367 * temp_k
        + math.tanh(0.0415 * (temp_k - 218.8))
        * (53.878 - 1331.22 / temp_k - 9.44523 * math.log(temp_k) + 0.014025 * temp_k)
    )


def actual_vapor_pressure_from_dewpoint_pa(dew_point_c: float) -> float:
    dew_k: float = dew_point_c + 273.15
    return saturation_vapor_pressure_over_water_pa(dew_k)


def specific_humidity_from_vapor_pressure(
    *,
    air_pressure_pa: float,
    vapor_pressure_pa: float,
) -> float:
    return (
        EPSILON
        * vapor_pressure_pa
        / (air_pressure_pa - (1.0 - EPSILON) * vapor_pressure_pa)
    )


def relative_humidity_liquid_percent(
    *,
    temperature_c: float,
    dew_point_c: float,
) -> float:
    temp_k: float = temperature_c + 273.15
    e_actual_pa: float = actual_vapor_pressure_from_dewpoint_pa(dew_point_c)
    e_sat_liquid_pa: float = saturation_vapor_pressure_over_water_pa(temp_k)
    return 100.0 * e_actual_pa / e_sat_liquid_pa


def as_1d_array(value: float) -> np.ndarray:
    return np.asarray([value], dtype=np.float64)


def scalar_from_array(value: Any) -> float:
    arr = np.asarray(value, dtype=np.float64)
    return float(arr.reshape(-1)[0])


def bool_from_array(value: Any) -> bool:
    arr = np.asarray(value)
    return bool(arr.reshape(-1)[0])


def assess_sac_binary(weather: WeatherAtLevel) -> SacAssessment:
    air_pressure_pa: float = float(weather.pressure_level_hpa) * 100.0
    air_temperature_k: float = weather.temperature_c + 273.15

    e_actual_pa: float = actual_vapor_pressure_from_dewpoint_pa(weather.dew_point_c)
    q_specific: float = specific_humidity_from_vapor_pressure(
        air_pressure_pa=air_pressure_pa,
        vapor_pressure_pa=e_actual_pa,
    )

    rh_liquid_percent: float = relative_humidity_liquid_percent(
        temperature_c=weather.temperature_c,
        dew_point_c=weather.dew_point_c,
    )
    rh_liquid_fraction: float = rh_liquid_percent / 100.0

    q_arr = as_1d_array(q_specific)
    p_arr = as_1d_array(air_pressure_pa)
    t_arr = as_1d_array(air_temperature_k)
    rh_arr = as_1d_array(rh_liquid_fraction)

    mixing_line_slope_g: float = scalar_from_array(
        pycontrails_sac.slope_mixing_line(
            specific_humidity=q_arr,
            air_pressure=p_arr,
            engine_efficiency=DEFAULT_ENGINE_EFFICIENCY,
            ei_h2o=JET_A_EI_H2O_KG_PER_KG,
            q_fuel=JET_A_Q_FUEL_J_PER_KG,
        )
    )

    g_arr = as_1d_array(mixing_line_slope_g)

    t_sat_liquid_k: float = scalar_from_array(pycontrails_sac.T_sat_liquid(g_arr))

    t_sat_arr = as_1d_array(t_sat_liquid_k)

    rh_critical_fraction: float = scalar_from_array(
        pycontrails_sac.rh_critical_sac(
            t_arr,
            t_sat_arr,
            g_arr,
        )
    )

    rh_crit_arr = as_1d_array(rh_critical_fraction)

    can_form: bool = bool_from_array(
        pycontrails_sac.sac(
            rh_arr,
            rh_crit_arr,
        )
    )

    reason: str = (
        f"SAC used T={weather.temperature_c:.2f}°C, "
        f"p={air_pressure_pa:.0f} Pa, RH_liquid={rh_liquid_percent:.1f}%, "
        f"RH_crit={rh_critical_fraction * 100.0:.1f}%, "
        f"T_sat_liquid={t_sat_liquid_k - 273.15:.2f}°C, "
        f"G={mixing_line_slope_g:.2f} Pa/K."
    )

    return SacAssessment(
        can_form=can_form,
        air_temperature_c=weather.temperature_c,
        air_pressure_pa=air_pressure_pa,
        rh_liquid_percent=rh_liquid_percent,
        rh_critical_percent=rh_critical_fraction * 100.0,
        specific_humidity_kgkg=q_specific,
        mixing_line_slope_g=mixing_line_slope_g,
        t_sat_liquid_c=t_sat_liquid_k - 273.15,
        reason=reason,
    )


def assess_persistence(
    *,
    sac: SacAssessment,
    weather: WeatherAtLevel,
) -> PersistenceAssessment:
    air_pressure_pa: float = float(weather.pressure_level_hpa) * 100.0
    air_temperature_k: float = weather.temperature_c + 273.15

    e_actual_pa: float = actual_vapor_pressure_from_dewpoint_pa(weather.dew_point_c)
    q_specific: float = specific_humidity_from_vapor_pressure(
        air_pressure_pa=air_pressure_pa,
        vapor_pressure_pa=e_actual_pa,
    )

    is_issr: bool = bool_from_array(
        pycontrails_issr.issr(
            air_temperature=as_1d_array(air_temperature_k),
            specific_humidity=as_1d_array(q_specific),
            air_pressure=as_1d_array(air_pressure_pa),
        )
    )

    rh_ice_percent: float = 100.0 * float(
        e_actual_pa / pycontrails_issr.thermo.e_sat_ice(air_temperature_k)
    )

    if not sac.can_form:
        return PersistenceAssessment(
            rh_ice_percent=rh_ice_percent,
            severity=0,
            is_issr=is_issr,
            reason="SAC gate failed, so persistence severity is forced to 0.",
        )

    if rh_ice_percent < 100.0:
        severity: int = 0
        reason: str = (
            f"RHice = {rh_ice_percent:.1f}% < 100%, so the air is not ice-supersaturated."
        )
    elif rh_ice_percent <= 120.0:
        severity = 1
        reason = f"RHice = {rh_ice_percent:.1f}% is in the moderate ice-supersaturated range."
    else:
        severity = 2
        reason = (
            f"RHice = {rh_ice_percent:.1f}% is in the severe ice-supersaturated range."
        )

    return PersistenceAssessment(
        rh_ice_percent=rh_ice_percent,
        severity=severity,
        is_issr=is_issr,
        reason=reason,
    )


def build_assessment(position: FlightPosition) -> ContrailAssessment:
    weather_payload: dict[str, Any] = fetch_weather_profile(
        latitude=position.latitude,
        longitude=position.longitude,
    )

    if position.timestamp_utc:
        target_time_utc: datetime = parse_iso_utc(position.timestamp_utc)
    else:
        target_time_utc = datetime.now(timezone.utc)

    weather: WeatherAtLevel = nearest_weather_level_for_altitude(
        weather_payload=weather_payload,
        altitude_m=position.altitude_m,
        target_time_utc=target_time_utc,
    )

    sac: SacAssessment = assess_sac_binary(weather)
    persistence: PersistenceAssessment = assess_persistence(
        sac=sac,
        weather=weather,
    )

    return ContrailAssessment(
        position=position,
        weather=weather,
        sac=sac,
        persistence=persistence,
    )


def print_assessment(result: ContrailAssessment) -> None:
    print("\n=== CONTRAIL RESULT ===")
    print(f"Source:                 {result.position.source}")
    print(f"Flight label:           {result.position.flight_label}")
    print(f"Position time UTC:      {result.position.timestamp_utc}")
    print(f"Latitude:               {result.position.latitude:.5f}")
    print(f"Longitude:              {result.position.longitude:.5f}")
    print(f"Aircraft altitude (m):  {result.position.altitude_m:.1f}")

    print("\n--- Matched Weather Layer ---")
    print(f"Weather time UTC:       {result.weather.time_utc}")
    print(f"Pressure level:         {result.weather.pressure_level_hpa} hPa")
    print(f"Layer geopotential ht:  {result.weather.geopotential_height_m:.1f} m")
    print(f"Temperature:            {result.weather.temperature_c:.2f} °C")
    print(f"Dew point:              {result.weather.dew_point_c:.2f} °C")
    if result.weather.relative_humidity_percent is not None:
        print(
            f"RH (reported):          {result.weather.relative_humidity_percent:.2f} %"
        )
    else:
        print("RH (reported):          None")

    print("\n--- Layer 1: pycontrails SAC Binary Gate ---")
    print(f"Can contrails form?     {result.sac.can_form}")
    print(f"Air pressure:           {result.sac.air_pressure_pa:.0f} Pa")
    print(f"RH liquid:              {result.sac.rh_liquid_percent:.2f} %")
    print(f"RH critical:            {result.sac.rh_critical_percent:.2f} %")
    print(f"Specific humidity:      {result.sac.specific_humidity_kgkg:.6f} kg/kg")
    print(f"Mixing-line slope G:    {result.sac.mixing_line_slope_g:.4f} Pa/K")
    print(f"T_sat_liquid:           {result.sac.t_sat_liquid_c:.2f} °C")
    print(f"SAC reason:             {result.sac.reason}")

    print("\n--- Layer 2: ISSR / Persistence Severity ---")
    print(f"ISSR boolean:           {result.persistence.is_issr}")
    print(f"RHice:                  {result.persistence.rh_ice_percent:.2f} %")
    print(f"Persistence severity:   {result.persistence.severity}")
    print(f"Persistence reason:     {result.persistence.reason}")
    print()


def run_manual_mode() -> None:
    print("\n--- Manual Mode ---")
    latitude: float = prompt_float("Enter latitude: ")
    longitude: float = prompt_float("Enter longitude: ")
    altitude_m: float = prompt_float("Enter altitude in meters: ")

    position: FlightPosition = build_manual_position(
        latitude=latitude,
        longitude=longitude,
        altitude_m=altitude_m,
    )

    result: ContrailAssessment = build_assessment(position)
    print_assessment(result)


def run_flight_mode() -> None:
    print("\n--- Flight Mode ---")
    flight_number, flight_iata, flight_icao = prompt_flight_lookup_mode()

    position: FlightPosition = fetch_live_flight_position(
        flight_number=flight_number,
        flight_iata=flight_iata,
        flight_icao=flight_icao,
    )

    result: ContrailAssessment = build_assessment(position)
    print_assessment(result)


def main() -> None:
    while True:
        try:
            choice: str = prompt_menu_choice()

            if choice == "1":
                run_manual_mode()
            elif choice == "2":
                run_flight_mode()
            elif choice == "3":
                print("Exiting.")
                break
            else:
                print("Invalid choice. Try again.")

        except requests.exceptions.RequestException as exc:
            print(f"\nNetwork/API error: {exc}\n", file=sys.stderr)
        except ContrailMVPError as exc:
            print(f"\nApplication error: {exc}\n", file=sys.stderr)
        except KeyboardInterrupt:
            print("\nInterrupted. Exiting.")
            break
        except Exception as exc:
            print(f"\nUnexpected error: {exc}\n", file=sys.stderr)


if __name__ == "__main__":
    main()
