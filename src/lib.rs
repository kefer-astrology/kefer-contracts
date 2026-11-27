//! Public chart-result contracts for Kefer Astrology.

/// Package version, also recorded in the contract manifest.
pub const VERSION: &str = env!("CARGO_PKG_VERSION");
/// SHA-256 manifest for the public contract files.
pub const MANIFEST: &str = include_str!("../contracts/manifest.json");
/// Examples of accepted and rejected event times.
pub const EVENT_TIME: &str = include_str!("../contracts/event-time.json");
/// JSON Schema for public chart-result fields.
pub const CHART_RESULT_SCHEMA: &str = include_str!("../contracts/schemas/api/chart-result.schema.json");
/// Synthetic chart-result example.
pub const CHART_RESULT_EXAMPLE: &str = include_str!("../contracts/examples/chart-result.json");

#[cfg(test)]
mod tests {
    #[test]
    fn manifest_version_matches_crate_version() {
        let needle = format!("\"version\": \"{}\"", super::VERSION);
        assert!(super::MANIFEST.contains(&needle));
        assert_eq!(include_str!("../VERSION").trim(), super::VERSION);
    }
}
