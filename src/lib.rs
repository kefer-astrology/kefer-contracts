//! Shared contracts for the Kefer Astrology calculation implementations.
//!
//! Every contract file is embedded at compile time, so consumers stay fully
//! offline. Files under `contracts/points/` are third-party-derived data and
//! are **not** MIT-licensed; see `contracts/points/NOTICE.md`.

/// Package version; equals `contracts/manifest.json` `version`.
pub const VERSION: &str = env!("CARGO_PKG_VERSION");

macro_rules! contract {
    ($name:ident, $path:literal) => {
        #[doc = concat!("`contracts/", $path, "`")]
        pub const $name: &str = include_str!(concat!("../contracts/", $path));
    };
}

contract!(MANIFEST, "manifest.json");
contract!(EVENT_TIME, "event-time.json");
contract!(SETTINGS_RESOLUTION, "settings-resolution.json");
contract!(SUBSTITUTION_WARNINGS, "substitution-warnings.json");
contract!(ASPECT_CATALOG, "catalogs/aspects.json");
contract!(ASPECT_DETECTION, "aspects/detection.json");
contract!(HOUSE_CUSPS, "houses/cusps.json");
contract!(HOUSE_CUSPS_TRUE_EQUINOX, "houses/cusps-true-equinox.json");
contract!(CONVENTIONS, "conventions.json");
contract!(CAPABILITIES, "capabilities.json");
contract!(REFERENCE_POSITIONS_HORIZONS, "reference/positions-horizons.json");
contract!(REFERENCE_EARTH_ORIENTATION, "reference/earth-orientation-erfa.json");
contract!(REFERENCE_MOON_PHASES_2024, "reference/moon-phases-usno-2024.json");
contract!(REFERENCE_TOLERANCES, "reference/tolerances.json");
contract!(CHART_RESULT_SCHEMA, "schemas/api/chart-result.schema.json");
contract!(POINTS_ARABIC_LOTS, "points/arabic-lots.json");
contract!(POINTS_FIXED_STARS, "points/fixed-stars.json");
contract!(HYPOTHETICAL_BODIES_SCHEMA, "schemas/points/hypothetical-bodies.schema.json");

#[cfg(test)]
mod tests {
    #[test]
    fn manifest_version_matches_crate_version() {
        let needle = format!("\"version\": \"{}\"", super::VERSION);
        assert!(super::MANIFEST.contains(&needle), "manifest/version mismatch");
        assert_eq!(include_str!("../VERSION").trim(), super::VERSION);
    }
}
