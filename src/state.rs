use std::sync::Mutex;

use crate::filesystem::SharedPathState;

pub type SharedPathMutex = Mutex<SharedPathState>;
