use std::{collections::HashMap, path::PathBuf, sync::MutexGuard};

use rocket_dyn_templates::Template;
use serde::Serialize;

use crate::{
    auth::Auth,
    config::Config,
    filesystem::{PathType, SharedPath, SharedPathState},
    forms::LoginForm,
    state::SharedPathMutex,
};
use rocket::{
    form::Form,
    fs::NamedFile,
    http::CookieJar,
    response::{status::NotFound, Redirect},
    State,
};

#[derive(Serialize)]
struct PathContext<'a> {
    parent: Option<&'a SharedPath>,
    path: &'a SharedPath,
    children: Option<Vec<&'a SharedPath>>,
}

#[get("/")]
pub fn index(
    path_state: &State<SharedPathMutex>,
    _auth: Auth,
) -> Result<Template, NotFound<String>> {
    let lock = path_state.lock().expect("lock shared data");
    let path = PathBuf::from("");
    println!("{_auth:?}");

    render_path(&path, &lock)
}

#[get("/", rank = 2)]
pub fn index_redirect_login() -> Redirect {
    Redirect::to(uri!(login))
}

#[get("/login")]
pub fn login() -> Template {
    let context: HashMap<String, String> = HashMap::new();
    Template::render("login", context)
}

#[post("/login", data = "<login_form>")]
pub fn login_post(
    config: &State<Config>,
    cookiejar: &CookieJar<'_>,
    login_form: Form<LoginForm<'_>>,
) -> Redirect {
    if Auth::login(&login_form, cookiejar, config) {
        Redirect::to(uri!(index))
    } else {
        Redirect::to(uri!(login))
    }
}

#[get("/shared/<path..>")]
pub fn path(
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
pub fn path_redirect_login(path: PathBuf) -> Redirect {
    Redirect::to(uri!(login))
}

fn render_path(
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

#[get("/file/<path..>")]
pub async fn file(
    path: PathBuf,
    path_state: &State<SharedPathMutex>,
    _auth: Auth,
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

#[get("/file/<path..>", rank = 2)]
#[allow(unused_variables)]
pub fn file_redirect_login(path: PathBuf) -> Redirect {
    Redirect::to(uri!(login))
}
