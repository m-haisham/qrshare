use std::{path::PathBuf, sync::MutexGuard};

use rocket_dyn_templates::Template;
use serde::Serialize;

use crate::{
    filesystem::{SharedPath, SharedPathState, SharedType},
    state::SharedPathMutex,
};
use rocket::State;

#[derive(Serialize)]
struct PathContext<'a> {
    relative: &'a PathBuf,
    path: &'a SharedType,
}

#[get("/")]
pub fn index(path_state: &State<SharedPathMutex>) -> Template {
    let lock = path_state.lock().expect("lock shared data");
    let path = lock.paths.get(&PathBuf::from(""));

    render_path(path.unwrap(), &lock)
}

#[get("/shared/<path..>")]
pub fn path(path: PathBuf, path_state: &State<SharedPathMutex>) -> Template {
    let lock = path_state.lock().expect("lock shared data");
    let path = lock.paths.get(&path);

    render_path(path.unwrap(), &lock)
}

fn render_path(path: &SharedPath, state: &MutexGuard<SharedPathState>) -> Template {
    println!("{:#?}", state);

    let context = PathContext {
        relative: &path.relative,
        path: &path.shared,
    };

    Template::render("path", &context)
}
