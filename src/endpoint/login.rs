use rocket::{
    form::Form,
    http::CookieJar,
    request::FlashMessage,
    response::{Flash, Redirect},
    State,
};
use rocket_dyn_templates::Template;

use crate::{
    context::LoginContext,
    form::LoginForm,
    guard::auth::{Auth, NotLoggedIn},
    state::config::Config,
};

use super::home::rocket_uri_macro_home_view;

#[get("/login")]
pub fn login_view(_not: NotLoggedIn, flash: Option<FlashMessage<'_>>) -> Template {
    let context = LoginContext::with(flash.as_ref().map(|m| m.message()));
    Template::render("login", context)
}

#[get("/login", rank = 2)]
pub fn logged_in() -> Redirect {
    Redirect::to(uri!(home_view))
}

#[post("/login", data = "<login_form>")]
pub fn login_form_submit(
    config: &State<Config>,
    cookiejar: &CookieJar<'_>,
    login_form: Form<LoginForm<'_>>,
) -> Flash<Redirect> {
    if Auth::login(&login_form, cookiejar, config) {
        Flash::success(Redirect::to(uri!(home_view)), "Login successful!")
    } else {
        Flash::error(
            Redirect::to(uri!(login_view)),
            "Password provided does not match, try again.",
        )
    }
}
