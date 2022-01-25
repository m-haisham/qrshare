pub mod config;
pub mod filesystem;

use std::sync::Mutex;

use self::filesystem::SharedPathState;

pub type SharedPathMutex = Mutex<SharedPathState>;
