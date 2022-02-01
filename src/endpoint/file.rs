use std::path::PathBuf;

use crate::{
    guard::{auth::Auth, RelativePath},
    state::{filesystem::PathType, SharedPathMutex},
};
use rocket::{
    fs::NamedFile,
    response::{status::NotFound, Redirect},
    State,
};

use super::login::rocket_uri_macro_login_view;

#[get("/file/<path..>")]
pub async fn file_serve(
    path: RelativePath,
    path_state: &State<SharedPathMutex>,
    _auth: Auth,
) -> Result<NamedFile, NotFound<String>> {
    let file_path: Option<PathBuf> = {
        let lock = path_state.lock().expect("lock shared data");
        let shared = lock.paths.get(&PathBuf::from(path)).unwrap();

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
pub fn file_login_redirect(path: RelativePath) -> Redirect {
    Redirect::to(uri!(login_view))
}
