use std::{fs::File, path::PathBuf, sync::MutexGuard};

use rocket_dyn_templates::Template;
use serde::Serialize;

use crate::{
    filesystem::{SharedPath, SharedPathState, SharedType},
    state::SharedPathMutex,
};
use rocket::{fs::NamedFile, response::status::NotFound, State};

#[derive(Serialize)]
struct PathContext<'a> {
    parent: Option<&'a SharedPath>,
    path: &'a SharedPath,
    children: Option<Vec<&'a SharedPath>>,
}

#[get("/")]
pub fn index(path_state: &State<SharedPathMutex>) -> Template {
    let lock = path_state.lock().expect("lock shared data");
    let path = lock.paths.get(&PathBuf::from(""));

    render_path(path.unwrap(), &lock)
}

#[get("/shared/<path..>")]
pub fn path(path: PathBuf, path_state: &State<SharedPathMutex>) -> Template {
    let mut lock = path_state.lock().expect("lock shared data");
    lock.visit(&path).unwrap();

    let path = lock.paths.get(&path).unwrap();

    render_path(path, &lock)
}

fn render_path(path: &SharedPath, state: &MutexGuard<SharedPathState>) -> Template {
    println!("{:#?}", state);

    let parent = path.parent.as_ref().map(|p| state.paths.get(p).unwrap());

    let children: Option<Vec<&SharedPath>> = {
        if let SharedType::Dir(shared) = &path.shared {
            if let Some(paths) = &shared.children {
                let children = paths.iter().map(|p| state.paths.get(p).unwrap()).collect();
                Some(children)
            } else {
                None
            }
        } else {
            None
        }
    };

    let context = PathContext {
        parent,
        path: &path,
        children,
    };

    Template::render("path", &context)
}

#[get("/file/<path..>")]
pub async fn file(
    path: PathBuf,
    path_state: &State<SharedPathMutex>,
) -> Result<NamedFile, NotFound<String>> {
    let file_path: Option<PathBuf> = {
        let lock = path_state.lock().expect("lock shared data");
        let path = lock.paths.get(&path).unwrap();

        if let SharedType::File(file) = &path.shared {
            Some(file.path.clone())
        } else {
            None
        }
    };

    if let Some(fp) = file_path {
        NamedFile::open(fp)
            .await
            .map_err(|e| NotFound(e.to_string()))
    } else {
        Err(NotFound(String::from("File not found")))
    }
}
