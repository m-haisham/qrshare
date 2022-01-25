use std::{path::PathBuf, sync::MutexGuard};

use rocket_dyn_templates::Template;
use serde::Serialize;

use crate::{
    filesystem::{PathType, SharedPath, SharedPathState},
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
pub fn index(path_state: &State<SharedPathMutex>) -> Result<Template, NotFound<String>> {
    let lock = path_state.lock().expect("lock shared data");
    let path = PathBuf::from("");

    render_path(&path, &lock)
}

#[get("/shared/<path..>")]
pub fn path(
    path: PathBuf,
    path_state: &State<SharedPathMutex>,
) -> Result<Template, NotFound<String>> {
    let mut lock = path_state.lock().expect("lock shared data");
    lock.visit(&path).unwrap();

    render_path(&path, &lock)
}

fn render_path(
    pathbuf: &PathBuf,
    state: &MutexGuard<SharedPathState>,
) -> Result<Template, NotFound<String>> {
    let path = match state.paths.get(pathbuf) {
        Some(path) => path,
        None => return Err(NotFound(String::from("Not found or not cached"))),
    };

    println!("{:#?}", state);

    let parent = path
        .parent
        .as_ref()
        .map(|p| state.paths.get(&p.key).unwrap());

    let children: Option<Vec<&SharedPath>> = {
        if let PathType::Dir(children) = &path.specific {
            children.as_ref().map(|paths| {
                paths
                    .iter()
                    .map(|p| state.paths.get(&p.key).unwrap())
                    .collect()
            })
        } else {
            None
        }
    };

    let context = PathContext {
        parent,
        path: &path,
        children,
    };

    Ok(Template::render("path", &context))
}

#[get("/file/<path..>")]
pub async fn file(
    path: PathBuf,
    path_state: &State<SharedPathMutex>,
) -> Result<NamedFile, NotFound<String>> {
    let file_path: Option<PathBuf> = {
        let lock = path_state.lock().expect("lock shared data");
        let shared = lock.paths.get(&path).unwrap();

        if let PathType::File = shared.specific {
            Some(shared.path.clone())
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
