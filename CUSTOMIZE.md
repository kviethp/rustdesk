# Build script

python .\build.py --portable --flutter --hwcodec --vram

# Change server
Line 117-123 file hbb_common/src/config.rs
```
pub const RENDEZVOUS_SERVERS: &[&str] = &["rs-ny.rustdesk.com"]; => đổi sang IP/host private
pub const RS_PUB_KEY: &str = "OeVuKk5nlHiXp+APNn0Y3pC1Iwpwn44JGqrQCsWqmBw="; => Đổi sang public key của private server

pub const RENDEZVOUS_PORT: i32 = 21116;
pub const RELAY_PORT: i32 = 21117;
pub const WS_RENDEZVOUS_PORT: i32 = 21118;
pub const WS_RELAY_PORT: i32 = 21119;
```