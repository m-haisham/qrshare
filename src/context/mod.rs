use serde::Serialize;

use crate::state::filesystem::SharedPath;

#[derive(Serialize)]
pub struct PathContext<'a> {
    pub parent: Option<&'a SharedPath>,
    pub path: &'a SharedPath,
    pub children: Option<Vec<&'a SharedPath>>,
}
