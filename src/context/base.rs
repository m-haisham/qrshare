use local_ip_address::local_ip;
use serde::Serialize;


#[derive(Serialize)]
pub struct BaseContext<'a, T: Serialize> {
    ipaddress: IpAddress,
    data: &'a T,
}

#[derive(Serialize)]
#[serde(tag = "tag", content = "content")]
pub enum IpAddress {
    Available(String),
    Error(String),
}

impl<'a, T: Serialize> BaseContext<'a, T> {
    pub fn from(data: &'a T) -> Self {
        let ipaddress = match local_ip() {
            Ok(i) => IpAddress::Available(i.to_string()),
            Err(e) => IpAddress::Error(e.to_string()),
        };

        Self { ipaddress, data }
    }
}
