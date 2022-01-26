use std::path::PathBuf;

use rocket_dyn_templates::Template;

use crate::{guard::auth::Auth, state::SharedPathMutex};
use rocket::{
    response::{status::NotFound, Redirect},
    State,
};

use super::{login::rocket_uri_macro_login_view, path::render_path};

#[get("/")]
pub fn home_view(
    path_state: &State<SharedPathMutex>,
    _auth: Auth,
) -> Result<Template, NotFound<String>> {
    let lock = path_state.lock().expect("lock shared data");
    let path = PathBuf::from("");

    render_path(&path, &lock)
}

#[get("/", rank = 2)]
pub fn home_login_redirect() -> Redirect {
    Redirect::to(uri!(login_view))
}
