use std::collections::HashMap;

use rocket::{form::Form, http::CookieJar, response::Redirect, State};
use rocket_dyn_templates::Template;

use crate::{form::LoginForm, guard::auth::Auth, state::config::Config};

use super::home::rocket_uri_macro_home_view;

#[get("/login")]
pub fn login_view() -> Template {
    let context: HashMap<String, String> = HashMap::new();
    Template::render("login", context)
}

#[post("/login", data = "<login_form>")]
pub fn login_form_submit(
    config: &State<Config>,
    cookiejar: &CookieJar<'_>,
    login_form: Form<LoginForm<'_>>,
) -> Redirect {
    if Auth::login(&login_form, cookiejar, config) {
        Redirect::to(uri!(home_view))
    } else {
        Redirect::to(uri!(login_view))
    }
}
