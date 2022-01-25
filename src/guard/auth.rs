use rocket::{
    http::{Cookie, CookieJar, Status},
    outcome::Outcome,
    request::{self, FromRequest, Request},
    State,
};

use crate::{
    form::LoginForm,
    state::config::{Config, Protection},
};

const AUTH_KEY: &'static str = "auth";

#[derive(Debug)]
pub struct Auth;

#[derive(Debug)]
pub enum AuthError {
    BadConfigOutcome,
}

impl Auth {
    pub fn login(form: &LoginForm, cookiejar: &CookieJar, config: &Config) -> bool {
        let password = match &config.protection {
            Protection::Protected(password_config) => password_config,
            Protection::None => return true,
        };

        if password.matches_password(form.password) {
            cookiejar.add_private(Cookie::new(AUTH_KEY, password.key_str()));
            true
        } else {
            false
        }
    }
}

#[rocket::async_trait]
impl<'r> FromRequest<'r> for Auth {
    type Error = AuthError;

    async fn from_request(req: &'r Request<'_>) -> request::Outcome<Self, Self::Error> {
        let config_outcome = req.guard::<&State<Config>>().await;
        let config = match config_outcome {
            Outcome::Success(config) => config,
            _ => return Outcome::Failure((Status::Conflict, AuthError::BadConfigOutcome)),
        };

        let password = match &config.protection {
            Protection::Protected(password_config) => password_config,
            Protection::None => return Outcome::Success(Auth),
        };

        let cookie = match req.cookies().get_private(AUTH_KEY) {
            Some(cookie) => cookie,
            None => return Outcome::Forward(()),
        };

        if password.matches_key(cookie.value()) {
            Outcome::Success(Auth)
        } else {
            Outcome::Forward(())
        }
    }
}
