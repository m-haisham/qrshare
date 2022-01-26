use std::{path::PathBuf, sync::MutexGuard};

use rocket_dyn_templates::Template;

use crate::{
    context::PathContext,
    guard::auth::Auth,
    state::{
        filesystem::{PathType, SharedPath, SharedPathState},
        SharedPathMutex,
    },
};
use rocket::{
    response::{status::NotFound, Redirect},
    State,
};

use super::login::rocket_uri_macro_login_view;

#[get("/shared/<path..>")]
pub fn path_view(
    path: PathBuf,
    path_state: &State<SharedPathMutex>,
    _auth: Auth,
) -> Result<Template, NotFound<String>> {
    let mut lock = path_state.lock().expect("lock shared data");
    lock.visit(&path).unwrap();

    render_path(&path, &lock)
}

#[get("/shared/<path..>", rank = 2)]
#[allow(unused_variables)]
pub fn path_login_redirect(path: PathBuf) -> Redirect {
    Redirect::to(uri!(login_view))
}

pub fn render_path(
    pathbuf: &PathBuf,
    state: &MutexGuard<SharedPathState>,
) -> Result<Template, NotFound<String>> {
    let path = match state.paths.get(pathbuf) {
        Some(path) => path,
        None => return Err(NotFound(String::from("Not found or not cached"))),
    };

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
